"""L11, крок 4: підсумок генерації для шаблону (час машини, вартість, кількість тестів).

    python tools/generation_summary.py reports/generation.json

Записана генерація та поточний (можливо запасний) набір — різні артефакти.
"""
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "reports" / "generation.json"
    if not path.exists():
        sys.exit(f"Немає файлу {path}. Запустіть генерацію з  --output-format json > {path}")
    raw = path.read_bytes()
    # Windows PowerShell 5.1 пише `>` в UTF-16; інші оболонки — в UTF-8
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        text = raw.decode("utf-16")
    else:
        text = raw.decode("utf-8-sig")
    data = json.loads(text)
    if data.get("is_error"):
        print(f"УВАГА: генерація завершилась помилкою: {data.get('result')}")
        print("Якщо файл тестів повний і pytest tests/generated зелений, набір можна брати; числа нижче — до моменту помилки.\n")

    tests = 0
    for f in (ROOT / "tests" / "generated").glob("test_*.py"):
        tests += len(re.findall(r"^\s*def test_", f.read_text(encoding="utf-8"), re.M))

    recorded_count = None
    recorded = data.get("result")
    if isinstance(recorded, str):
        code = recorded.strip()
        if code.startswith("```") and code.endswith("```"):
            code = code.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        try:
            tree = ast.parse(code)
        except SyntaxError:
            pass
        else:
            recorded_count = sum(
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name.startswith("test_") for node in ast.walk(tree)
            )
    models = ", ".join(data.get("modelUsage", {}) or []) or "?"
    minutes = (data.get("duration_ms") or 0) / 60000
    cost = data.get("total_cost_usd")
    cost_text = f"{cost:.6f}" if isinstance(cost, (int, float)) else "не встановлено"
    print(f"Модель записаного запиту: {models}")
    print(f"Час машини записаного запиту, хв: {minutes:.4f}")
    print(f"Кроків асистента:     {data.get('num_turns')}")
    print(f"Вартість записаного запиту, USD (оцінка): {cost_text}")
    print(f"Функцій у записаному output: {recorded_count if recorded_count is not None else 'не встановлено'}")
    print(f"Поточний каталог tests/generated/: {tests} функцій")
    manifest = ROOT / "reports" / "fallback-source.json"
    if manifest.exists():
        fallback = json.loads(manifest.read_text(encoding="utf-8-sig"))
        if fallback.get("kind") == "fallback":
            print(f"Запасний набір: {tests} функцій; модель, час і ціна створення невідомі")
            print("Метадані записаного запиту не описують запасний файл.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
