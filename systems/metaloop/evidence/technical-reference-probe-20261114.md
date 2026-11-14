# Technical probe execution record — 2026-11-14

Scope: **reference implementation / deterministic check only**. This is NOT a stable-vs-candidate LLM A/B, NOT a blinded held-out result, and NOT independent review.

Protocol: [paired-eval-preregistration-20261114.md](paired-eval-preregistration-20261114.md), Task A (CSV parsing).
Execution: current ChatGPT session generated a reference implementation using Python 3 stdlib `csv.DictReader(restkey="__extra__", restval=None)` and ran six Python `unittest` assertions in the available Python execution environment. Model output was not generated in two separately isolated stable/candidate prompt conditions; do not attribute this result to either prompt.

## Observed result
- `Ran 6 tests in 0.009s`
- `OK`; failures 0; errors 0.
- Tested: sample total 5 with missing amount + extra column rejected; empty CSV; quoted ID; short row; non-integer amount; invalid header.
- Output captured in the originating ChatGPT tool execution, not an externally immutable CI artifact. Time shown is unittest-reported test duration, **not model latency**.
- Reference implementation and tests were executed in this chat; no separate GitHub CI was triggered for this Python code.
- No exact model token or cost telemetry available. No external human review. No verified held-out novelty.

## Attribution / limitations
This establishes only that a single reference solution passed six deterministic tests. It does not establish candidate improvement, real user reuse, an authenticated lifecycle feedback event, or a score for either prompt. Technical model A/B = NOT_RUN; nontechnical model A/B = NOT_RUN; comparative quality = NOT_VERIFIED. Production stable remains unchanged.

## Follow-up
Run stable and candidate with the same independently sealed, non-overlapping input in isolated sessions and preserve both raw outputs and tool logs; then independently verify against the frozen rubric.
