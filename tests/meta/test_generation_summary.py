"""Reporting regressions; excluded from the three frozen comparator sets."""
import importlib.util
import json
from pathlib import Path

import pytest


@pytest.fixture
def summary(tmp_path, monkeypatch, capsys):
    path = Path(__file__).resolve().parents[2] / "tools/generation_summary.py"
    spec = importlib.util.spec_from_file_location("generation_summary_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    generated = tmp_path / "tests/generated"
    generated.mkdir(parents=True)
    (generated / "test_current.py").write_text(
        "def test_current_one(): pass\ndef test_current_two(): pass\n", encoding="utf-8"
    )
    reports = tmp_path / "reports"
    reports.mkdir()

    def run(result, fallback=False):
        data = {"modelUsage": {"recorded-model": {}}, "duration_ms": 12541,
                "total_cost_usd": 0.002638, "result": result}
        source = reports / "generation.json"
        source.write_text(json.dumps(data), encoding="utf-8")
        if fallback:
            (reports / "fallback-source.json").write_text(
                json.dumps({"kind": "fallback", "function_count": 2}), encoding="utf-8"
            )
        monkeypatch.setattr(module.sys, "argv", ["generation_summary.py", str(source)])
        assert module.main() == 0
        return capsys.readouterr().out

    return run


def test_summary_counts_recorded_code_instead_of_live_fallback(summary):
    code = "\n".join(f"def test_recorded_{i}(): pass" for i in range(10))
    assert "Функцій у записаному output: 10" in summary(code)


def test_summary_preserves_nonzero_small_cost(summary):
    assert "0.002638" in summary("def test_recorded(): pass")


def test_summary_labels_fallback_as_a_separate_artifact(summary):
    output = summary("def test_recorded(): pass", fallback=True)
    assert "Запасний набір: 2 функцій; модель, час і ціна створення невідомі" in output


def test_summary_does_not_infer_recorded_count_from_live_files(summary):
    output = summary("Finished writing the requested file.")
    assert "Функцій у записаному output: не встановлено" in output
