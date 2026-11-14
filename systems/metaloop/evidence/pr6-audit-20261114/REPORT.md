# PR #6 frozen evidence audit — 2026-11-14

**Decision: NOT_VERIFIED / DO NOT PROMOTE.** No model-quality A/B took place. This evidence commit contains reproducible deterministic controls, an overlap-gate counterexample, frozen input envelopes and explicit missing-result records. It does not contain four fabricated model outputs.

## Identity and boundaries

PR: https://github.com/lovemoganna/AgentComponent/pull/6

| Item | Frozen identity |
|---|---|
| main / PR base | `011694de28436fc11cc1aa68ff916aa7579dff06` |
| PR head inspected | `13768da0d7e9655b481b1a01cd03754c6d24cfc9` |
| Stable Blob | `188953441f5c54fdb81c7883ad05aa0e15a277fa` |
| Candidate Blob | `e87076047facb3a88ad95a6322f06a4cd478b0cc` |

Git blob identity was recalculated from bytes and checked against both frozen commits. Registry agrees. Neither prompt differs between base and PR head; PR #6 adds a protocol and two probe records. Stable is a single-task loop; Candidate includes multi-task orchestration. A shared task measures only their common task scope.

No production prompt, Registry, test answer or implementation was changed. Only files under this evidence directory are submitted on a new experiment branch. No PR merge, review approval, lifecycle real event or deployment is performed.

## Results and attribution

| Experiment | Stable condition | Candidate condition | What is established |
|---|---|---|---|
| Technical CSV model task | NOT_VERIFIED | NOT_VERIFIED | No clean model invocation or raw code output available |
| Nontechnical model task | NOT_VERIFIED | NOT_VERIFIED | No clean model invocation or raw explanation available |
| Frozen repository unittest control | 46/46 | 46/46 | Same frozen code in fresh directories/processes; no prompt effect tested |
| Text adapter development examples | 5/6 vs 6/6 in each control | Same result | `normalize_ascii` vs `normalize_unicode`; NOT Stable vs Candidate prompts |
| Registry inventory | PASS, 14/14 | PASS, 14/14 | Path/SHA coverage only |
| Renamed-development overlap probe | Incorrect in-memory promotion | Same result | Gate accepts duplicated input/answers after changing IDs |

Raw stdout/stderr, command arguments, exit codes and wall-clock tool durations: `run-01/`. Those durations are code execution time, never model latency. The two directory labels identify repeated **control runs**, not two executed prompt conditions. They share an OS/kernel; filesystem/process separation is not a secure container boundary. Python is 3.12.14, so the preregistered Python 3.11 condition is NOT_VERIFIED. No CSV implementation produced by either prompt exists in this run to execute.

Four frozen input envelopes are prepared with identical A/B task bytes and version-specific full prompt bytes. They are **inputs only**. `model-ab-ledger.json` deliberately uses null raw-output fields and NOT_VERIFIED status. No isolated model worker was invoked; this run used the existing controller conversation, shell and retrieval tools. Exact deployed model ID, sampling settings, model token/cost/latency, context isolation and independent evaluator are NOT_VERIFIED. Same-conversation role play would not repair this gap.

## Development overlap

`overlap.json` records tracked-tree matches and reachable-history matches. The six-case adapter suite is explicitly a development suite, not held-out. PR #6 already publishes Task A's expected total/rejections and a prior CSV reference-run description; its Task B probe publishes a complete 142-character answer. Thus both public examples are exposed evaluation/development material and cannot now be called independently sealed blind held-out.

No exhaustive inventory of private development tasks, deleted/unfetched branches, other chats or model training exists here. Absence of a match would not prove novelty. Complete development non-overlap and independent task sealing remain NOT_VERIFIED. Public examples can still serve as transparent smoke tests after isolated execution, but cannot provide blind generalization evidence.

## Key defects, evidence and upgrade advice

1. **Confirmed gate defect, high priority.** `engine.py` checks whole-suite hash and overlapping IDs, but not per-case input/acceptance identity. `overlap-gate-probe.py.txt` deep-copies all six development cases and renames only IDs. In both processes `promoted_in_memory=true`. The synthetic reviewer fixture is visibly labelled and is not real approval. `disk_registry_unchanged=true`; no write path was invoked. Repair with canonical per-case task fingerprints excluding ID, order and incidental metadata, plus semantic review for paraphrases. Add a regression requiring renamed/reordered duplicates to be rejected. Do this in a separately authorized implementation change; this commit records evidence only.
2. **Confirmed evidence gap.** Prior technical probe reports six tests but PR #6 stores neither implementation nor raw test transcript. Its reported success is not independently replayable from that record. Preserve each future model's verbatim response, extracted code, extraction mapping and external test logs. Do not attribute the old reference probe to either frozen prompt.
3. **Confirmed missing experimental result.** Four isolated model runs, equal model/tool budget and independent review are absent. Therefore there is no valid win rate, quality delta or promotion claim. Configure a clean-session runner, seal replacement tasks through a separate evaluator, freeze model/system/tool/budget conditions, randomize order and retain every original run, including failures. Apply the same external tests to both code outputs and claim-by-claim review to both explanations. Candidate itself requests repeated paired runs; two tasks/one pair are only a smoke test.
4. **Known authentication limitation.** The gate accepts self-declared reviewer fields; the README already discloses this. A synthetic JSON review is not human verification. Require an independently attributable review artifact tied to the frozen inputs, outputs and artifact hashes. Do not create approval records automatically.

Candidate remains Candidate. Keep the current Stable. No prompt patch is justified by these controls because prompt effectiveness has not been measured.

## External verification basis

Sources were opened during this audit. These are external reference checks by the controller, **not independent reviewer signoff**. Frozen concise source notes are in `source-basis.json`; they provide URLs, claim locators and boundaries, not a complete archival snapshot or proof of the previous extraction IDs.

- Python 3.11 csv documentation: https://docs.python.org/3.11/library/csv.html — `DictReader` restkey/restval explain extra/missing fields; `Dialect.strict` governs malformed CSV. This supports evaluator design only; current runtime is 3.12.
- NIST: https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai — Description/Approach explain reference-corpus checks, audit trails and citation faithfulness/completeness/sufficiency. It does not supply measured accuracy for these prompt versions or independently approve their outputs. A source-grounding check cannot establish all underlying source facts; that limitation is an inference, not a quoted NIST conclusion.

## Replay

From a clone containing the frozen PR commit:

```sh
python3 systems/metaloop/evidence/pr6-audit-20261114/replay.py --out /tmp/pr6-replay
```

The script extracts the frozen Git archive into two fresh temporary directories, verifies blobs, preserves the exact preregistered task text, runs repository controls and the no-write synthetic counterexample, and hashes artifacts. Use Python 3.12 for the recorded control environment. No dependencies or external model API are used. Timings and collection timestamps vary; deterministic statuses and values should agree. The script does not run model A/B, independently review claims or authenticate a human reviewer. SHA256SUMS provides tamper detection relative to the evidence commit, not third-party attestation.
