# Setup verification — 23.11.2026

Scope: preparation only, before author baseline work. This is not a completed lab/homework or a passing baseline.

- Fresh clone of course main: d6c471a79e3bb4da33756c6e1026d3366f98faf5. New local branch codex/hw10-resit, remote course-upstream only; no origin/public resit repository yet.
- New separate .venv: Python3.12.14, pytest9.2.0, pytest-cov7.1.0, coverage7.17.5. Installation of requirements.txt completed successfully; requirements itself is unchanged from upstream.
- Import of app.engines.fx succeeded.
- Command `.venv/Scripts/python.exe -m pytest tests/manual --collect-only -q -p no:cacheprovider` returned **no tests collected in0.03s**, exit5 as expected for the upstream stub. This is not PASS.
- Diff against upstream for app, tests, .claude/settings.json and requirements.txt is empty. No baseline implementation was written by an assistant.
- reports/, tests/generated/ and tests/rewritten/ contain only their tracked .gitkeep placeholders. prompts/ has only its upstream README.md. No custom mutants.toml exists.
- protocol/baseline-timing.json is not_started; timestamps and durations are null, not zero completed minutes. No generation call has been made in this resit.
- The user supplied the mentor feedback preserved in mentor-feedback.md. Previous exposure is explicitly recorded, not claimed absent.
- IDE opening is a handoff step after this setup check; the timer starts only after an explicit author start message.

Handoff observed: PyCharm window titled paypilot-hw10-ai-adoption-resit, branch codex/hw10-resit, with tests/manual/test_fx_manual.py open and the project's .venv3.12.14 selected. No author start message or generation has occurred; the timer remains not_started. The previous homework window is a different project and must not be used for this baseline.
