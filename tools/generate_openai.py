"""One isolated OpenAI request; explicit course-provider deviation, not Claude CLI.

Default is a free preflight. --run consumes the separately authorized single call.
Only the weak prompt and fx.py enter the message payload. No filesystem tools.
"""
import argparse
import ast
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
MODEL = "gpt-4.1-mini-2025-04-14"
PRICE_SOURCE = "https://developers.openai.com/api/docs/pricing"
RATES = {"input": 0.40, "cached_input": 0.10, "output": 1.60}
CAP = 0.05
MAX_OUTPUT = 6500
MANUAL_SHA = "14bd8d9f8bd83ec12d62bc78136295ae3e6a240c69978f3826fca10e1911e699"


def dump(path, data):
    with path.open("x", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--env-file", type=Path)
    args = ap.parse_args()
    source = ROOT / "app/engines/fx.py"
    prompt = ROOT / "prompts/generation-prompt.md"
    manual = ROOT / "tests/manual/test_fx_manual.py"
    assert hashlib.sha256(manual.read_bytes()).hexdigest() == MANUAL_SHA
    payload = {
        "model": MODEL,
        "instructions": "Return only the complete contents of the requested Python file, without Markdown fences.",
        "input": prompt.read_text(encoding="utf-8").strip()
        + "\n\nFile: app/engines/fx.py\n```python\n"
        + source.read_text(encoding="utf-8") + "\n```",
        "max_output_tokens": MAX_OUTPUT,
        "temperature": 0.7,
        "service_tier": "default",
        "store": False,
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    # Pessimistic byte-based ceiling plus generous protocol overhead; no tools.
    upper = (len(body) + 2048) * RATES["input"] / 1_000_000 + MAX_OUTPUT * RATES["output"] / 1_000_000
    assert upper < CAP, "request does not fit authorized cap"
    meta = {
        "provider": "openai", "model": MODEL,
        "payload_bytes": len(body), "max_output_tokens": MAX_OUTPUT,
        "authorized_cap_usd": CAP,
        "pessimistic_estimate_ceiling_usd": upper,
        "prices_usd_per_million": RATES, "price_source": PRICE_SOURCE,
        "price_verified_date": "2026-11-23",
        "manual_sha256": MANUAL_SHA,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "prompt_sha256": hashlib.sha256(prompt.read_bytes()).hexdigest(),
        "payload_sha256": hashlib.sha256(body).hexdigest(),
        "context_files": ["prompts/generation-prompt.md", "app/engines/fx.py"],
        "filesystem_tools": [], "retries": 0,
        "mentor_requested_claude": True, "literal_claude_compliance": False,
    }
    if not args.run:
        print(json.dumps(meta, ensure_ascii=False, indent=2))
        return 0
    for rel in ["tests/manual", "mutants.toml", "prompts", "protocol/forecast.md"]:
        assert not subprocess.check_output(
            ["git", "status", "--porcelain", "--", rel], cwd=ROOT
        ).strip(), f"uncommitted frozen input: {rel}"
    assert (ROOT / "protocol/forecast.md").is_file()
    target = ROOT / "tests/generated/test_fx_generated.py"
    assert not target.exists(), "never overwrite a generated comparator"
    reports = ROOT / "reports"
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key and args.env_file:
        for line in args.env_file.read_text(encoding="utf-8-sig").splitlines():
            name, sep, value = line.partition("=")
            if sep and name.strip() == "OPENAI_API_KEY":
                key = value.strip().strip('"').strip("'")
                break
    assert key, "OPENAI_API_KEY not configured; nothing sent"
    dump(reports / "generation-request.json", payload)
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    meta["started_utc"] = started
    meta["pre_generation_head"] = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    # Exclusive attempt marker prevents rerunning after failure or timeout.
    dump(reports / "generation-attempt.json", meta)
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses", data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    tick = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            raw = response.read()
            request_id = response.headers.get("x-request-id")
    except Exception as exc:
        # No error body/key/header dump and no retry.
        dump(reports / "generation-failure.json", {
            "error_type": type(exc).__name__,
            "http_status": getattr(exc, "code", None),
            "elapsed_seconds": time.perf_counter() - tick,
            "automatic_retry": False,
        })
        raise SystemExit("Generation failed; attempt retained, no automatic retry.") from None
    elapsed = time.perf_counter() - tick
    (reports / "generation-response.json").write_bytes(raw)
    data = json.loads(raw)
    usage = data.get("usage") or {}
    cached = (usage.get("input_tokens_details") or {}).get("cached_tokens", 0)
    cost = ((usage.get("input_tokens", 0) - cached) * RATES["input"]
            + cached * RATES["cached_input"]
            + usage.get("output_tokens", 0) * RATES["output"]) / 1_000_000
    output = "".join(c["text"] for item in data.get("output", [])
                     for c in item.get("content", []) if c.get("type") == "output_text")
    code = output.strip()
    extraction = "strip surrounding whitespace only"
    if code.startswith("```") and code.endswith("```"):
        code = code.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        extraction += "; remove single enclosing Markdown fence"
    summary = {
        **meta, "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "duration_ms": elapsed * 1000, "elapsed_seconds": elapsed,
        "num_turns": 1, "request_id": request_id, "response_id": data.get("id"),
        "response_model": data.get("model"), "response_status": data.get("status"),
        "usage": usage, "total_cost_usd": cost,
        "cost_is_usage_estimate_not_billing": True,
        "modelUsage": {data.get("model", MODEL): usage},
        "extraction": extraction, "result": output,
        "is_error": data.get("status") != "completed",
    }
    dump(reports / "generation.json", summary)
    if data.get("status") != "completed" or not code:
        raise SystemExit("Incomplete response retained; no replacement call authorized.")
    with target.open("x", encoding="utf-8", newline="\n") as fh:
        fh.write(code + "\n")
    tree = ast.parse(code)
    count = sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test_")
                for n in ast.walk(tree))
    print(json.dumps({"status": data.get("status"), "model": data.get("model"),
                      "test_functions": count, "elapsed_seconds": elapsed,
                      "usage_estimate_usd": cost, "request_id": request_id,
                      "tests_executed": False}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
