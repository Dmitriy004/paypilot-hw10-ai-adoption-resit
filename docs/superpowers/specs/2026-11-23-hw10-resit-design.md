# HW10 resit: clean setup and author-controlled first stage

The user chose step-by-step execution of the mentor's required new-repository resit. Start from course kit https://github.com/TarasFedorenkoFTV/paypilot-l11-eval at d6c471a79e3bb4da33756c6e1026d3366f98faf5 in a new local directory. No prior homework code, results or custom git history are imported. The upstream manual stub contains no test functions; generated and rewritten contain only placeholders.

## Approach

The user rejected simply copying the old baseline after clarification and chose the phased fresh-authoring route. Reusing old code or changing old history does not meet the supplied feedback; a mentor fallback is a different route requiring actual mentor authorization, not assumed here.

Assistant responsibilities now: create an isolated course checkout, install the pinned test dependencies in a separate venv, preserve this protocol and a not-started timer, and open the upstream empty manual stub in the IDE. The author writes the baseline independently. No tests, test-case suggestions, mutation list, custom generation prompt or generated comparator are supplied by the assistant during this stage.

## Boundaries

- Old repos/indexes unchanged. New branch codex/hw10-resit; only course-upstream remote during setup. Public origin is added only when the new work is ready.
- Timer begins only at an explicit author start message, not project creation/opening. All later timing events are real and preserved; no old writing/review minutes migrate here.
- Author baseline is frozen directly under tests/manual in its own commit before custom mutants.toml, prompts, forecast and claude -p generation. No late promotion or suite replacement.
- Later generation uses Claude Code as requested, only after access/context checks and current budget authorization. No paid call in setup.
- Prior exposure is disclosed; no claim of a new blinded participant or guaranteed mentor acceptance.
- Preparation is not completed homework. Stop for actual author participation; later stages follow the saved order.

## Acceptance of setup

Fresh upstream HEAD and no prior homework commits; separate pinned Python environment; zero collected baseline tests (pytest exit5 is expected, not a green baseline); no generated/rewritten implementations, custom mutants or prompts; unchanged upstream app and manual stub; timer fields null; IDE opened on the new path if UI access is available.
