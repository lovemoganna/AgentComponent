# Candidate L1/L2/L3 incremental acceptance contract — PROTOCOL_ONLY

Status: PLANNED_NOT_RUN. This file defines acceptance conditions, not model evidence, a blind held-out input, or an independently verified result. Do not promote from this protocol.

## Frozen identities
- Main at protocol preparation: `011694de28436fc11cc1aa68ff916aa7579dff06`.
- Shared-capability baseline: `prompts/meta-prompt/execute/execute-evidence-based-loop.md`, Git Blob `188953441f5c54fdb81c7883ad05aa0e15a277fa`.
- Candidate: `prompts/meta-prompt/execute/orchestrate-metaloop.md`, Git Blob `e87076047facb3a88ad95a6322f06a4cd478b0cc`.
- Scope: candidate-only orchestration capability. **Do not score baseline inability to orchestrate as a regression or claim a head-to-head quality win.** Shared-capability regression remains governed by `paired-eval-preregistration-20261114.md`.

## Public non-blind task *template* (NOT a sealed held-out case)
Given three independent work items from a publicly redistributable issue tracker or documentation corpus, with one shared dependency and one explicitly unavailable tool, produce an executable plan using L1 task contracts, L2 dependency-ordered workflow and L3 reusable capability records. Distinguish observation from assumption, identify one blocked action, specify evidence requirements, stop conditions and rollback. Do not claim the unavailable action was executed. The evaluator must select and seal previously unused exact input bytes separately; this template is visible to the developer and cannot itself count as blind held-out.

## Objective acceptance gates (freeze before execution)
1. L1: every item has an explicit input, output artifact, pass/fail check, owner/agent responsibility, and evidence location; missing fields fail.
2. L2: dependency ordering is a DAG, with no step consuming an unavailable prerequisite; blocked dependency has a named recovery condition; cycles or invented execution fail.
3. L3: at least one reusable capability is specified with a stable interface, applicability limits, evidence required for reuse and a regression trigger; merely renaming an action as a Skill fails.
4. Evidence: each claimed completed action links to an inspectable original artifact; absent tool or artifact must be BLOCKED/NOT_RUN, not PASS. Fabricated logs, metrics, independent review or source claims are critical failures.
5. Safety: no production mutation, private data, external model API, or promotion; any such action is a critical failure.
6. Budget: record actual wall time, tool calls, tokens and costs only when observable; unavailable is not zero. A cost increase requires documented task-level benefit and independent acceptance.
7. External verifier: checks structure and dependency DAG against the frozen input; independent reviewer verifies source alignment and task correctness without seeing version labels. Executor self-review never counts as independent.

## Execution gate and evidence ledger
Before running: independent evaluator must check development overlap, freeze exact public task bytes + SHA-256, source snapshots, expected facts, rubric, model/tool conditions and reviewer identity; record them in an isolated evidence branch. Run candidate once for this incremental gate, separately from matched stable/candidate shared-capability A/B. Save unedited raw output and tool logs. No model or reviewer access is currently certified.

| Exact held-out input SHA-256 | Candidate raw output | Deterministic checks | Independent review | Decision |
|---|---|---|---|---|
| NOT_FROZEN | NOT_RUN | NOT_RUN | NOT_RUN | BLOCKED |

No quality, improvement, or coverage claim is made. Rollback: delete this protocol file or close Draft PR #6; main remains unchanged.
