# Explicit provider deviation — before generation

The supplied mentor feedback explicitly requests generation through `claude -p`. The course kit uses Claude Code with `.claude/settings.json`. On 2026-11-23 the user instead explicitly requested OpenAI twice and authorized one new OpenAI request up to **USD0.05**. Claude authorization was not completed; a read-only `claude auth status` returned loggedIn:false.

Proceed with OpenAI only under this later user instruction. This is **not compliance with the literal Claude workflow**, not mentor-approved equivalence, and not a fallback artifact supplied by the mentor. The resit cannot be guaranteed to pass this requirement. Keep this deviation visible in the final report and declaration; never claim a Claude run occurred.

Use a fresh request, not old output. Provide only the literal weak prompt plus current `app/engines/fx.py`, with a minimal code-output transport instruction. Do not transmit policy.py, manual tests, mutants, criteria, forecasts, old generated suites, reports or this protocol. With a direct API request the model has no local filesystem tools, so context isolation is enforced by the explicit message payload rather than Claude deny settings; the course settings stay unchanged. Record exact input, output, model, token usage, elapsed time, request identifiers and price source. A usage estimate is not a reconciled provider bill. No retry for a better comparator.

Manual freeze: f0340dd66ddcb4702a0452cdf01012fe1ef0db2e. Mutant freeze: 717e6923b4be956db198ae1e203bb32b61488c49. Prior exposure/timing limitations stay in the protocol.
