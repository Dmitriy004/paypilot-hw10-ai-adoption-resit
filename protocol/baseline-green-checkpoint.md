# Corrected author baseline: original-green source checkpoint

The author reported “я починил”; the first clock reading on receipt was 2026-11-23T21:31:33Z, or 22:31:33 Europe/Warsaw. No correction-start event had been explicitly recorded. Its actual start and pauses have been requested from the author; correction duration and total author effort remain unknown, not estimated from the first attempt or git timestamps.

The assistant inspected the author diff and did not modify test implementation. Canonical file: `tests/manual/test_fx_manual.py`; SHA256 `14bd8d9f8bd83ec12d62bc78136295ae3e6a240c69978f3826fca10e1911e699`.

Verification on the unchanged original module: `.venv/Scripts/python.exe -m pytest tests/manual -q -p no:cacheprovider` — **6 passed in 0.03s**, exit 0, six functions and six cases. `git diff --check` passed.

This commit preserves the green author source before custom mutants, custom prompts or generation. The first red attempt remains in d59bd25e23e99439fc7ddce6b38fac157f849eaf. The initial uninterrupted interval was 1245 seconds; it is not the total writing-plus-correction time. The protocol is not declared fully satisfied while correction timing is unresolved. Do not generate or build the comparison until this gap is resolved or explicitly retained as a protocol limitation.

No generated comparator has been shown or executed in this resit. Prior exposure to the old rejected experiment remains disclosed. This checkpoint does not claim mentor acceptance or complete homework.
