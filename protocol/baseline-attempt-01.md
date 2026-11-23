# Initial author baseline attempt — not a green frozen baseline

23.11.2026, Europe/Warsaw. The author explicitly reported start at22:05:35 and finish at22:26:20; first clock readings on receipt correspond to21:05:35Z and21:26:20Z. Wall interval1245seconds=20minutes45seconds=20.75minutes, including communication latency. The author subsequently explicitly confirmed no pauses; this is not independently measured active-only work.

The author supplied six test functions directly in tests/manual/test_fx_manual.py. The assistant has not changed their implementation. SHA256 of the checked file:1e7648cf14b895849d9a3515748ac72e5dee3ddb3e624ef1cdca27fd7608c009.

Command: `.venv/Scripts/python.exe -m pytest tests/manual -q -p no:cacheprovider`.

Observed result on the original module: **3 passed,3 failed in0.10s**, exit1;6collected cases,6functions.

| Failed function | Observed failure |
| --- | --- |
| test_quote_returns_expected_fields | TypeError: argument of type 'FxQuote' is not iterable |
| test_quote_zero_amount | TypeError: 'FxQuote' object is not subscriptable |
| test_quote_negative_amount | Failed: DID NOT RAISE ValueError |

This checkpoint preserves the original attempt, not completion or acceptance. Before any custom mutants/prompts or generation, the author must correct the baseline independently and report the actual correction start/finish. The current source is not improved or pruned by the assistant. No generated comparator has been run or shown in this resit.

The initial source and timing checkpoint was committed as d59bd25e23e99439fc7ddce6b38fac157f849eaf at22:27:38+01:00,78seconds after the reported finish. That preserves the submitted attempt promptly; it does not convert three original-module failures into a green baseline. This later documentation update only records the author's no-pause confirmation.
