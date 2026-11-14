# MetaLoop cross-domain paired evaluation — preregistration (NOT RUN)

Date: 2026-11-14. This is a proposed evaluation contract, **not** a verified held-out run or a model-quality result. Public references were retrieved during protocol design; this file and its examples are therefore visible to the designer and must not be represented as independently blind. An independent evaluator must check overlap against the development set and seal the final task inputs before a run.

## Frozen prompt identities
- Stable: `prompts/meta-prompt/execute/execute-evidence-based-loop.md`, Git Blob `188953441f5c54fdb81c7883ad05aa0e15a277fa`.
- Candidate: `prompts/meta-prompt/execute/orchestrate-metaloop.md`, Git Blob `e87076047facb3a88ad95a6322f06a4cd478b0cc`.
- Repository main at protocol creation: `011694de28436fc11cc1aa68ff916aa7579dff06`.
- These prompts are not semantically identical: the stable focuses on a single-task execution loop and candidate on cross-task orchestration. Compare only on a shared task contract; report scope differences rather than assuming all differences are quality gains.

## Task A — technical, public reference, PROPOSED_NOT_RUN
Reference: https://docs.python.org/3.11/library/csv.html
Input contract: Given a CSV with header `id,amount` and rows `a,2`, `b,3`, `c,` and `d,5,extra`, produce a Python 3.11 stdlib function returning the sum of valid integer amounts and a structured list of rejected rows. Reject missing values and extra columns; do not silently coerce invalid records. Include a runnable unit test. Expected valid sum: 5, with two rejected records (c, d). No external packages or network.
Check: run actual code in a fresh environment; assert total, rejection reasons, empty input, quoted CSV and malformed row. Compare to official DictReader restkey/restval semantics. Do not count generated code as tested unless execution logs are saved.

## Task B — nontechnical, public reference, PROPOSED_NOT_RUN
Reference: https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai
Input contract: Explain in <=220 Chinese characters why a model's self-evaluation does not establish independently verified factual accuracy; identify one concrete evidence trail and one limitation of reference-based probes. Attribute only claims supported by the reference, separate source assertions from our inference, and do not invent measured accuracy or independent human review.
Check: claim-by-claim source alignment, required elements, character limit, unsupported numerical claims, clear expression. Independent reviewer must mark each unsupported claim and omitted required element.

## Paired execution and isolation
1. Independent evaluator first checks that A/B inputs and their variants have not been used in prior development, previous prompt edits or evaluator training; replace overlapping examples. Freeze input bytes and SHA-256, reference snapshots, rubric and environment before first model invocation.
2. Run each task once with the stable prompt and once with candidate, in separate clean conversations, identical GPT model/version, system instructions, tool permissions, tool state, temperature where controllable, and fixed resource budget. Randomize prompt order. If isolation cannot be guaranteed, label NOT_COMPARABLE; do not fabricate an A/B.
3. Save original prompt input, outputs, tool invocation logs, external test output, model identifier, observed elapsed time, and exact token/cost records **only if available**. If absent, set unavailable, never estimate.
4. Deterministic tests (code/length/schema), external reference verification, model-generated results, and independent reviewer decisions must be separate columns. Same executor's opinion is not independent review.
5. Scoring per task: task completion, factual correctness, constraint compliance, critical errors; document qualitative clarity separately. Any critical regression, no substantive improvement, missing independent review, incomparable environment or unverifiable cost => do not promote.
6. No user chats, personal identifiers, API keys, private inputs or raw private tool results may be committed. Use safe public evidence pointers and redacted identifiers. Events are only recorded with lifecycle.py allowlisted fields after authenticating evidence.

## Evidence ledger (empty by design)
| Task | Stable raw output | Candidate raw output | Deterministic checks | External check | Independent review | Model/time/cost | Decision |
|---|---|---|---|---|---|---|---|
| A technical | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_AVAILABLE | NOT_VERIFIED |
| B nontechnical | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_AVAILABLE | NOT_VERIFIED |

No model run, win rate, authenticated real event, or quality improvement is asserted by this document. Existing Registry status and production prompt content remain unchanged. Rollback: close this draft PR or delete this isolated branch; no production change is required.
