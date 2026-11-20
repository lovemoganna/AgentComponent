# Cross-domain paired evaluation readiness and blocker record — 2026-11-20

**Decision: BLOCKED / NOT_VERIFIED.** Technical and nontechnical Stable/Candidate generation: **0/4 completed**. No comparison or promotion decision can be drawn. This record advances the readiness evidence for the [paired protocol](paired-eval-preregistration-20261114.md). The previous CSV and NIST probes and the three-issue incremental fixture were developer-visible calibration material.

## Prompt and environment checks

| Arm | Frozen Git Blob SHA-1 |
|---|---|
| Stable | `188953441f5c54fdb81c7883ad05aa0e15a277fa` |
| Candidate | `e87076047facb3a88ad95a6322f06a4cd478b0cc` |

Retrieved both files as base64 at main commit `011694de28436fc11cc1aa68ff916aa7579dff06`; recomputed their byte identities locally using `git hash-object`. Evidence-only PR parent observed before this record: `b5d805ac846b64bb3be978b9c54005893278bfd3`.

- The isolated shell ran Git 2.56.1 and Python 3.12.14. It can verify hashes and check rubric data. The technical task target is Python 3.11. The 3.12 fixture check below does not certify execution on 3.11.
- Codex CLI `0.172.0-alpha.2` reported a ChatGPT login. A read-only, ephemeral CLI preflight with a constant sentinel and no task inputs was attempted. Automatic review rejected the action because its model endpoint (`ab.chatgpt.com`) fell under the user's external-model-API restriction. The stdout event log was 0 bytes. Local stderr contained CLI state database initialization warnings. No model turn completion, arm outputs or model telemetry were observed. No retry through another external model endpoint was attempted.
- No usable offline runner was established. `ollama`, `llama-cli`, `llama-server`, `torch`, `transformers` and `llama_cpp` were absent from the checked shell paths and Python environment. A clean model runner, a matched system/model/tool envelope, and an independent evaluator have not been verified. This executor authored the provisional fixtures and cannot certify their independent sealing or review.
- Per-arm model ID/build, system configuration, latency, tool calls, exact tokens, and cost: `NOT_AVAILABLE`. No scores or lifecycle feedback events were produced.

## New provisional fixtures and scope of overlap screening

Both items are synthetic inputs authored in this execution for the shared single-task capability. Exact UTF-8 input bytes below include the final LF and exclude fences. They are frozen for reproducible readiness work. Their independent held-out status is **NOT_VERIFIED**.

The executor screened 16 repository artifacts: seven relevant main commit diffs through `011694de` (`011694de`, `b7534f35`, `cca5a691`, `327f4b81`, `b9f2c82c`, `d5684f6a`, `738d5ba9`), the PR #6 diff and both prior comments, and the pinned MetaLoop README, frozen regression suite, observation example, and engine, layer and lifecycle tests. The sentinel checks found zero matches for `calendar_gap`, the two example dates, `date.fromisoformat`, `Modified Mercalli`, `earthquake magnitude`, and `甲地烈度`. Known older tasks include CSV parsing, NIST reference-based evaluation, and deterministic normalization, percentage, JSON lookup and deduplication; none is an exact match. This scope excludes private development conversations, evaluator-training material and a full semantic history audit. For a protocol-qualified blind run, an independent evaluator must select and seal fresh undisclosed inputs after checking that broader development corpus.

### A — technical input

SHA-256 `4178b45c34f476d6be966f3e79b1d1490d49e235693d417675e7544aea9a6430` (744 bytes).

```text
任务：用 Python 3.11 标准库实现 calendar_gap(start, end)，返回从 start 到 end 相隔的日历天数整数。两个参数均应为 ASCII YYYY-MM-DD 字符串，必须是有效的公历日期。相同日期返回 0；格式错误、无效日期、非字符串或 end 早于 start 都抛出 ValueError。禁止自动补齐、删掉空格或改用其他日期格式。
示例输入：calendar_gap("2028-02-27", "2028-03-02")
参考：Python 3.11 datetime.date 文档说明两个 date 对象相减得到 timedelta，天数可从 days 取得。https://docs.python.org/3.11/library/datetime.html#date-objects
交付：Python 代码、一个可运行的单元测试及一句说明；如报告执行结果，请给出可核验的依据。
```

### B — nontechnical input

SHA-256 `d0611efa489892b945e59ed6405f2d4f39a92904e808361f51b65fcb6acd530a` (803 bytes).

```text
任务：写一段给社区读者看的中文说明，解释为什么同一次地震在甲、乙两地的摇晃程度可以不同。题设为虚构：一则通报给出震级 6.2，甲地烈度 VI，乙地烈度 III。
参考摘句（USGS）：An earthquake has one magnitude. / Intensity scales [...] measure the amount of shaking at a particular location.
参考链接：https://www.usgs.gov/faqs/what-difference-between-earthquake-magnitude-and-earthquake-intensity-what-modified-mercalli
交付：一段不超过 180 Unicode 码点的对外文字（独立来源行不计长度），另起一行给出来源链接。说明震级和烈度各指什么，解释题设数字如何同时成立，并指出给定信息能否确定两地差异的具体成因。不要补写题设未给出的实测数据。
```

## Frozen acceptance criteria for these fixtures

**A.** Require Python 3.11 stdlib code with the requested function and at least one runnable test. Execute the submitted test and independent cases in a fresh restricted Python 3.11 environment. Compare each result by exact integer type/value or `ValueError`. Enforce strict ASCII format on both inputs and no trimming or coercion. A false test-execution claim, wrong public example, or accepted invalid/reversed date fails the relevant gate. Report actual test process output separately from any model claim.

Each row below is `[start, end, expected]`. Expected `"ValueError"` means an exception, not a returned string.

```json
[
  ["2028-02-27","2028-03-02",4],
  ["2028-02-29","2028-02-29",0],
  ["2027-02-28","2027-03-01",1],
  ["2027-12-31","2028-01-01",1],
  ["0001-01-01","9999-12-31",3652058],
  ["2027-02-29","2027-03-01","ValueError"],
  ["2028-02-29","2028-02-28","ValueError"],
  ["20280229","2028-03-01","ValueError"],
  ["2028-W09-2","2028-03-01","ValueError"],
  [" 2028-02-29","2028-03-01","ValueError"],
  ["2028-2-29","2028-03-01","ValueError"],
  ["２０２８-０２-２９","2028-03-01","ValueError"],
  [null,"2028-03-01","ValueError"],
  ["2028-02-29","2028-02-30","ValueError"],
  ["2028-02-29","2028-03-01\n","ValueError"]
]
```

**B.** Deterministic check: count Unicode code points in the paragraph only, enforcing ≤180, and check the independent source line contains the exact USGS URL. Blinded source reviewer verifies independently that (1) magnitude describes the size of the event at its source, (2) intensity describes shaking at a location, (3) 6.2 and VI/III can coexist for the fictional event, with VI stronger than III, and (4) the information does not identify the cause of the local difference. Claiming two event magnitudes, inventing local measurements, attributing an unverified specific cause, or presenting the fictional event as real is a critical fault. Record evidence and omissions per claim, alongside task completion, factual correctness, constraints and clarity.

Source snapshots are limited to the operative excerpts, not full page captures. Parallel extraction ID `extract_eed9ee2ac12666c290cf296ea7b7b275`.

| Case | Source and snapshot acquisition date | Frozen source text and interpretation |
|---|---|---|
| A | [Python 3.11 date objects](https://docs.python.org/3.11/library/datetime.html#date-objects), 2026-11-17 | `timedelta = date1 - date2`. Strict formatting and rejection behavior come from the task, not the library reference. |
| B | [USGS earthquake magnitude and intensity](https://www.usgs.gov/faqs/what-difference-between-earthquake-magnitude-and-earthquake-intensity-what-modified-mercalli), 2026-11-05 | “An earthquake has one magnitude.” Intensity scales “measure the amount of shaking at a particular location.” The source also explains that magnitude measures the earthquake size at the source and that intensity varies by location. The 6.2/VI/III values are fictional. |

### Executed fixture check

In the isolated shell, an evaluator-owned reference used a strict ASCII regular expression, `date.fromisoformat`, and `(end - start).days`. All 15 expected values were asserted, with `ValueError` caught and matched. Tool output, exit code 0:

```text
A.txt 4178b45c34f476d6be966f3e79b1d1490d49e235693d417675e7544aea9a6430 744
B.txt d0611efa489892b945e59ed6405f2d4f39a92904e808361f51b65fcb6acd530a 803
cases.json 8e5f5beec34a9a1333509d500b73c5d1bb05a7900add948662892de07beb06d1
refs.json 35a3055dcbb4863cd08f6b0493c32451e921ebc939de0ca22e8ee1096b019331
Python 3.12.14 evaluator fixture check: 15/15 expected values confirmed (reference only)
```

No model output was used in this check. B has a source-based review rubric and no answer to grade.

## Paired execution ledger

| Task | Stable raw output | Candidate raw output | Model-output checks | Independent blind review | Decision |
|---|---|---|---|---|---|
| A — technical | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_VERIFIED |
| B — nontechnical | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_VERIFIED |

The preregistered run needs two independently sealed task packets and four fresh model sessions under one permitted, matched configuration. Shuffle arm order before the run. Keep source snapshots fixed, acceptance answers evaluator-side, and arm labels out of reviewer packets. Retain unedited outputs, tool/test logs, blind review basis and the available cost record. Keep this record as a barrier to promotion until those artifacts exist.
