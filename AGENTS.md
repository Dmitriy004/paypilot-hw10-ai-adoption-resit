# HW10 resit — experiment boundaries

- This is a fresh checkout of the course kit, not a continuation of the rejected homework history. Never copy old manual/generated/rewritten suites, reports, prompts or timers into it.
- The author must implement the new baseline without assistant-produced tests, snippets or test-case suggestions. Before the author reports completion, leave tests/manual/test_fx_manual.py as the upstream stub; no assistant may implement it or delegate its implementation.
- Start the author timer only after the author explicitly says they are starting. Record real timestamps and pauses. Never infer time from git timestamps or reuse an old timer.
- Freeze the completed author baseline directly at tests/manual/ in its own commit, before creating the new mutants.toml and custom prompts/. Verify original-green status and commit promptly within the course's five-minute tolerance after the final reported finish. If corrections are necessary, the author makes them and the actual timing events remain recorded.
- Only after that freeze: commit mutants.toml, then custom prompts/, then a separate forecast on the final mutant list, all before generation. Do not reveal generated comparators to the author before baseline freeze.
- The mentor requested claude -p. The later explicit user instruction on 23.11 instead requires OpenAI and authorizes one new request up to USD0.05; see protocol/provider-deviation.md. Do not claim literal mentor-protocol compliance or mentor approval. Preserve exact isolated context/model/usage/time and disclose the substitution. No extra request or retry is authorized.
- Commit the first complete raw generated suite at tests/generated/ before executing it. Preserve the response, usage and timing. Never replace or improve manual/generated after generation; only preserve and then remove original-red tests in a separate commit if the course permits.
- Review/rewrites must have real author records. Keep rewritten tests separate from manual/generated/all. Never change frozen inputs to obtain a better score.
- Old repositories and their indexes are read-only. Do not rewrite, squash, backdate or transplant their history.
- Stage explicit task-related paths after diff inspection; never stage .env, credentials, .idea, caches or incidental logs. Publication and LMS submission are later separate steps, not setup.
- Follow the user's mandatory aiq-final post-task checklist using immutable links only; record partial status honestly and do not mark a lab/homework complete while author work is missing.
