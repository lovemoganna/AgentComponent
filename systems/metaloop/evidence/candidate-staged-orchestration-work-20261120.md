# Candidate staged alert orchestration — 2026-11-20

**Original run: FAIL on the structured source reference. Controlled replay: deterministic PASS after one clarification to the fixture's interface text.** The frozen Candidate prompt was used in both runs. This is a Candidate-only test, followed by a regression replay on the same data. It provides no comparative or promotion result.

| Frozen gate | Original | Repair replay |
|---|---|---|
| One read of shared ledger | PASS. P1 read once, P2 had zero ledger calls. | PASS. Same totals. |
| Handle open tasks with another prerequisite missing | PASS for P1 outcomes. N17 and N26 completed while the invoice was unavailable. N38 was blocked and recorded no value. | PASS for P1 outcomes. Same behavior. |
| Resume only the affected alert | PASS for scope and arithmetic. P2 began and submitted only N38. N17/N26 output files were byte-identical before and after release. | PASS. Same behavior. |
| Exact source trace in structured results | FAIL. N38 used `INV52` in its evidence array while its narrative named `INVOICE:INV52:v1`. | PASS. N38 stored `["R31","INVOICE:INV52:v1"]`. |

Both P1 runs completed N17/N26 before recording the N38 block, although the invoice file was unavailable throughout P1. The tests therefore cover completing independent alerts while the prerequisite is absent. They do not establish chronological continuation after a block is recorded. That ordering remains untested.

## Inputs and isolation

- Candidate prompt blob `e87076047facb3a88ad95a6322f06a4cd478b0cc`, recomputed using `git hash-object` from the pinned main revision `011694de28436fc11cc1aa68ff916aa7579dff06`. These fixtures implement the [incremental acceptance contract](candidate-l123-incremental-acceptance.md) using fully synthetic transactions and confirmation material. The PR baseline parent for this report was `a273b1df716d0238c16c6e5bf34220bac576d8e5`.
- The coordinator authored the fixtures and froze the task, source ledgers, later invoice, rubric, follow-up and queue harness before execution. The coordinator screened nine pinned repository materials, including six main development files, the PR diff and two preceding comments. No exact hits for `LEDGER:S9`, `INVOICE:INV52:v1`, `THRESHOLD_MET`, `DUPLICATE_BOOKING`, or `COVERAGE_GAP`. This is a scoped repository novelty check and provides no audit of private development history.
- Each run opened a fresh native Work model session with `fork_turns: none` and no explicit model override. P2 was a follow-up in that same run's context. In P1 the invoice was absent from the queue directory. The coordinator saved P1 state before publishing the exact frozen invoice bytes and sending the frozen follow-up. The evaluator was a separate model context and received no prompt/version metadata. It used the same rubric for the original and the replay. It was aware that the second packet was a repair replay.
- The execution environment was CPython 3.12.14. Each agent was instructed to use only the prepared task packet and approved queue commands in its assigned directory. The filesystem was shared and no per-agent OS isolation or full hidden trace was available. The queue trace verifies its own calls. No external model API was used. Exact model build, per-turn latency, token counts, and cost are unavailable.
- Each run has 11 timestamped queue operations, including the expected P1 exit 4 and three successful P2 operations. The oldest and newest times bound the tool trace, including the coordinator's handoff. They do not measure model latency. L3 covers an interface specification and a reused ledger/queue interface within a case. A reusable implementation across cases and actual rollback are unverified.

## Failure and intervention

The earliest evidenced deviation was the original N38 submit at `2026-11-20T14:03:12.473931+00:00`. Its value was correctly computed as 240 SIM. Its reason and user-facing answer had the right version. The queue's structured `evidence` field used the business invoice number. That field is what the frozen verifier consumes.

The task had called for a confirmation ID without distinguishing `payload.invoice` from `payload.source`. The observed failure is consistent with that ambiguity. The coordinator appended exactly one paragraph to the fixture task defining which field to copy. The Candidate blob, source data, harness, follow-up and rubric were kept identical. The replay is evidence that the clarified contract passed once on the same scenario. Generalization and the cause's stability remain unverified.

```text
证据引用格式：确认单的 evidence 元素必须逐字使用 read invoice 回执中 payload.source 的版本化来源标识。payload.invoice 是业务编号，不能代替来源标识。
```

## Independent reviews

### Original review

````markdown
**独立复核：共享与隔离通过，P2 实际恢复成功，结构化证据未达到冻结标准。**

包文件 SHA-256 为 `ce97ad288d9f5ce8950055a8780ff77c221f008c1afdc2f9a0091feffc105765`。

- **P1** 只成功读取一次 `LEDGER:S9`。N17 先 `begin` 再 `submit`，以 R11–R14 为证据提交 `THRESHOLD_MET`、700 SIM。N26 随后以 R21–R23 为证据提交 `DUPLICATE_BOOKING`、2 条。N38 `begin` 后读确认单返回退出码 4，提交 `BLOCKED`、两个 `null` 和 R31，明确须取得 INV52 的 `CONFIRMED`、SIM 且含明确覆盖金额的确认单才能恢复。N17、N26 均在阻塞前完成。P1 阻塞后没有其他告警继续运行。
- **P2** 在确认单发布后依次执行 `read invoice`、`begin N38`、`submit N38`，零流水调用。读取用于核验恢复条件，记录未显示 `begin` 前发生重算。N38 实际提交 `DONE`、`COVERAGE_GAP`、240 SIM。N17、N26 的前后结果字节内容一致。
- **最早确定偏差** 出现在 P2 的 `14:03:12.473931Z` 提交。结构化 `evidence` 是 `["R31","INV52"]`，冻结标准要求 `["R31","INVOICE:INV52:v1"]`。读取回执、提交理由和回复正文均保留了准确版本，计算可追溯。结构化字段仍缺版本引用。
- **L1–L3** 三项都有输入、输出、验收依据、负责人和证据位置。L2 的共享流水与确认单依赖无环，涵盖停机、恢复和保留审计记录后提交更正的方案。L3 明示接口、适用边界、来源要求与回归触发条件。可观测复用是同一份流水支持两种聚合，聚合实现本身的复用仍为候选。
````

### Repair replay review

````markdown
**独立复核 PASS。** 同一案例的修复重放满足共享、隔离、恢复和证据四项冻结标准。包文件 SHA-256 为 `15384fa9e2a57f50f5bd25cfdf89d101df30527f50cd240d20d1c56ddf3a6388`。

- **P1** 成功读取一次 `LEDGER:S9`。N17 提交 `DONE / THRESHOLD_MET`、700 SIM，证据为 R11–R14。N26 提交 `DONE / DUPLICATE_BOOKING`、2 条，证据为 R21–R23。随后 N38 读取确认单返回退出码 4，提交 `BLOCKED`、两个 `null` 和 R31，记录了精确恢复条件。确认单在 P1 不可用期间，N17 和 N26 均完成。两者都在 N38 实际提交阻塞前结束，因此本次没有覆盖先记录阻塞、再继续其他告警的顺序。
- **P2** 只读取已发布确认单、`begin N38`、`submit N38`，没有重读流水。R31 的 840 SIM 减 `CONFIRMED` 确认单覆盖的 600 SIM，提交 `DONE / COVERAGE_GAP`、240 SIM。结构化证据 `["R31","INVOICE:INV52:v1"]` 与审计、结果文件及回复一致。N17、N26 结果前后字节一致。
- **L1–L3** 交付覆盖三项验收字段、无环依赖、停止与授权更正、可复用接口、适用边界、来源约束和回归触发。实际复用限于共享流水和同一提交接口。通用判定实现的再用、列举的回归分支及更正路径均未执行。
````

## Frozen manifests and stage boundary

Source JSON and markdown blocks below exclude the Markdown separator LF. The Python source blocks and JSONL traces include a final LF when reconstructing files. The input packet is the original Candidate blob, followed by `\n--- USER TASK ---\n` and the task string. To reconstruct the replay task, append two LF and the clarification paragraph above to the original task string.

### Original

Frozen at `2026-11-20T14:01:29.855388+00:00`. P1 snapshot at `2026-11-20T14:02:57.730413+00:00`. Invoice released at `2026-11-20T14:02:57.730869+00:00`. Last queue operation at `2026-11-20T14:03:12.473931+00:00`.

```json
{
  "prompt": "630c029afcc4b24ffd9e2847d1cfd709a040db3be10b6d9681bae9a50c13669b",
  "ledger": "fda74d5f73f8773212284c03291e0236739377cddbb2b98fb259000d6a0d1619",
  "confirm": "86a3b9aa203e3a8664a0cb2a36790270d84b04009cd9b0d750ecdf4eb1628f7f",
  "task": "5880fe6aa6cdcd886822e64dc4ba97b4b6a3735a70a9a605e56319d34787210a",
  "follow": "e6699877849edb207c8858d53de2f3580f48391ef7318cc4f9ce8b77ca964cbe",
  "rubric": "07b658a446a4214f1208ed22b5907990f6853047d12a9a986332e11f38c49ede",
  "harness": "267c56fd2423f99c96d3422b5884fd95ba763153588923008d14ee4224d39a35",
  "packet": "2a4fbe5f33e865baffe2ab0006598b79392dfeb4867c55565d29a0816c55e878",
  "working_ledger": "fda74d5f73f8773212284c03291e0236739377cddbb2b98fb259000d6a0d1619",
  "working_harness": "267c56fd2423f99c96d3422b5884fd95ba763153588923008d14ee4224d39a35",
  "frozen_utc": "2026-11-20T14:01:29.855388+00:00"
}
```

| File | SHA-256 at P1 | SHA-256 after P2 |
|---|---|---|
| N17.result.json | `501c4146eb1e69530d6dc9a78322172eca402039403c214e7999bbd8fe9dae43` | `501c4146eb1e69530d6dc9a78322172eca402039403c214e7999bbd8fe9dae43` |
| N26.result.json | `75d77dafe8d6f06be8f64770dfb277420ebd68bc4c897e2a26fb8e602059e211` | `75d77dafe8d6f06be8f64770dfb277420ebd68bc4c897e2a26fb8e602059e211` |
| N38.result.json | `ced0e9e10f05f0b836a2c940eeab4a68d7315f23e86623d978ccc60e42ab43d1` | `86337b74c12cb71390b7d62ac437614f583916722a4a6ac2c2c98dd815379fe6` |

Trace SHA-256 `b034219a108d377416ca16c157d289fa1e93948130bd79def36d5b240f652a85`. P1 response SHA-256 `2aae5dbc31535f159cb70ac8b60b9dc4069f72d11d15f41261c025ab0439d086`. P2 response SHA-256 `bd09cfb049ef375a1211d41a2d7ef679d35359fa7c3422a28f1827dc1d251227`. The responses are captured native final payloads without an added final LF.

Verifier exit code `1`. Verifier source SHA-256 `c70a00f057f276b153bdaede899557bd235a27800185e9004c86ae8656f4092e`.

```text
ce97ad288d9f5ce8950055a8780ff77c221f008c1afdc2f9a0091feffc105765
{
  "checks": {
    "single successful ledger read over both phases": true,
    "P1 records exactly one attempt for each alert": true,
    "P1 closes N17 and N26 and logs N38 blocked": true,
    "P2 opens and closes N38 only with released source": false,
    "N17 and N26 artifacts byte-identical after resume": true,
    "phase1 audit prefix and original ledger unchanged": true,
    "release is exact frozen invoice bytes": true,
    "no extra or unrecognized log entries": true
  },
  "operations": {
    "P1": {
      "read": 2,
      "begin": 3,
      "submit": 3
    },
    "P2": {
      "read": 1,
      "begin": 1,
      "submit": 1
    }
  },
  "total_events": 11,
  "phase2_unchanged": [
    "N17",
    "N26"
  ],
  "phase2_results": {
    "N17.result.json": "{\"alert\":\"N17\",\"status\":\"DONE\",\"result\":\"THRESHOLD_MET\",\"value\":700,\"evidence\":[\"R11\",\"R12\",\"R13\",\"R14\"],\"reason\":\"LEDGER:S9 中，同账户 N17 的 BOOKED OUT 纳入 R11（430 SIM）和 R12（270 SIM），合计 700 SIM，严格大于 650 SIM。R13 已取消，R14 为入金，其他行账户不同，均排除。\"}",
    "N26.result.json": "{\"alert\":\"N26\",\"status\":\"DONE\",\"result\":\"DUPLICATE_BOOKING\",\"value\":2,\"evidence\":[\"R21\",\"R22\",\"R23\"],\"reason\":\"LEDGER:S9 中，S88 的两条不同 BOOKED 流水为 R21 和 R22，实际计数为 2。R23 对应 S88 但已取消，排除。\"}",
    "N38.result.json": "{\"alert\":\"N38\",\"status\":\"DONE\",\"result\":\"COVERAGE_GAP\",\"value\":240,\"evidence\":[\"R31\",\"INV52\"],\"reason\":\"LEDGER:S9 的 R31 已入账 840 SIM，关联 INV52。确认单 INVOICE:INV52:v1 状态为 CONFIRMED，币种为 SIM，确认覆盖 600 SIM。差额为 840 - 600 = 240 SIM，大于零。\"}"
  }
}
```

### Repair replay

Frozen at `2026-11-20T14:03:53.117751+00:00`. P1 snapshot at `2026-11-20T14:05:17.063607+00:00`. Invoice released at `2026-11-20T14:05:17.064238+00:00`. Last queue operation at `2026-11-20T14:05:29.960429+00:00`.

```json
{
  "prompt": "630c029afcc4b24ffd9e2847d1cfd709a040db3be10b6d9681bae9a50c13669b",
  "ledger": "fda74d5f73f8773212284c03291e0236739377cddbb2b98fb259000d6a0d1619",
  "confirm": "86a3b9aa203e3a8664a0cb2a36790270d84b04009cd9b0d750ecdf4eb1628f7f",
  "follow": "e6699877849edb207c8858d53de2f3580f48391ef7318cc4f9ce8b77ca964cbe",
  "rubric": "07b658a446a4214f1208ed22b5907990f6853047d12a9a986332e11f38c49ede",
  "harness": "267c56fd2423f99c96d3422b5884fd95ba763153588923008d14ee4224d39a35",
  "task": "88e6c4a63cf170386c03943f2e97894bbe47f214cf46a8d325196949ad16a3fa",
  "verify.py": "c70a00f057f276b153bdaede899557bd235a27800185e9004c86ae8656f4092e",
  "packet": "787af6044b4fe0919067077b1aad208ba965659b0ce3b30c449d40e3a95c300c",
  "frozen_utc": "2026-11-20T14:03:53.117751+00:00"
}
```

| File | SHA-256 at P1 | SHA-256 after P2 |
|---|---|---|
| N17.result.json | `7ac6b8bbfbb87aa91be80a6416d8166ca6028188b9ba39afb597bd790d35cb6d` | `7ac6b8bbfbb87aa91be80a6416d8166ca6028188b9ba39afb597bd790d35cb6d` |
| N26.result.json | `538970b03c0b54da27a7f1676da373a7c7c720d9488a8f272b0ca6c6c75b18bb` | `538970b03c0b54da27a7f1676da373a7c7c720d9488a8f272b0ca6c6c75b18bb` |
| N38.result.json | `69cddf5a70c9b730d5c4606393c1e996bf969f43747bfd1a3ae5d6860e07e487` | `cbea1ce2c3a8eeb18ecbccd3553f426c0e0f56b192db0a5c2c75aff8c0a2db51` |

Trace SHA-256 `d5acfb27f57331d5424e5bcbb2f10719de0203868c05ea386fcf30ffe379b340`. P1 response SHA-256 `54626f6f9a31a28ccea86f49b78379ebfb4c71762f5b3b2ddb7222a35b0a8853`. P2 response SHA-256 `087ca8f0598b04091cb6fca98549afa0cede9dac00cb73097e545d379d72318b`. The responses are captured native final payloads without an added final LF.

Verifier exit code `0`. Verifier source SHA-256 `c70a00f057f276b153bdaede899557bd235a27800185e9004c86ae8656f4092e`.

```text
15384fa9e2a57f50f5bd25cfdf89d101df30527f50cd240d20d1c56ddf3a6388
{
  "checks": {
    "single successful ledger read over both phases": true,
    "P1 records exactly one attempt for each alert": true,
    "P1 closes N17 and N26 and logs N38 blocked": true,
    "P2 opens and closes N38 only with released source": true,
    "N17 and N26 artifacts byte-identical after resume": true,
    "phase1 audit prefix and original ledger unchanged": true,
    "release is exact frozen invoice bytes": true,
    "no extra or unrecognized log entries": true
  },
  "operations": {
    "P1": {
      "read": 2,
      "begin": 3,
      "submit": 3
    },
    "P2": {
      "read": 1,
      "begin": 1,
      "submit": 1
    }
  },
  "total_events": 11,
  "phase2_unchanged": [
    "N17",
    "N26"
  ],
  "phase2_results": {
    "N17.result.json": "{\"alert\":\"N17\",\"status\":\"DONE\",\"result\":\"THRESHOLD_MET\",\"value\":700,\"evidence\":[\"R11\",\"R12\",\"R13\",\"R14\"],\"reason\":\"LEDGER:S9：同账户 BOOKED OUT 纳入 R11 430 SIM 与 R12 270 SIM，合计 700 SIM 严格大于 650 SIM。R13 为 CANCELLED，R14 为 IN，其余流水属于其他账户，均排除。\"}",
    "N26.result.json": "{\"alert\":\"N26\",\"status\":\"DONE\",\"result\":\"DUPLICATE_BOOKING\",\"value\":2,\"evidence\":[\"R21\",\"R22\",\"R23\"],\"reason\":\"LEDGER:S9：S88 有两条行号不同的 BOOKED 流水 R21 和 R22。R23 虽同属 S88，但为 CANCELLED，排除。\"}",
    "N38.result.json": "{\"alert\":\"N38\",\"status\":\"DONE\",\"result\":\"COVERAGE_GAP\",\"value\":240,\"evidence\":[\"R31\",\"INVOICE:INV52:v1\"],\"reason\":\"LEDGER:S9 的 R31 显示 INV52 已入账出金 840 SIM。与其匹配的确认单状态为 CONFIRMED，币种为 SIM，确认覆盖额为 600 SIM。差额 840 − 600 = 240 SIM，严格大于零。\"}"
  }
}
```

## Frozen task, sources and rubric

### Initial task

```text
这是一个完全模拟的交易告警队列。把三个告警实际处理进本地演练队列。只在给定测试目录工作。没有真实账户或外部系统权限。不同阶段会收到不同输入。你的初始阶段是 P1。

N17 / 汇总阈值：只计同账户已入账（BOOKED）的出金（OUT），阈值为 650 SIM，严格大于才标记 THRESHOLD_MET，否则 THRESHOLD_NOT_MET。提交实际合计、纳入和排除依据。
N26 / 重复结算：检查 S88 是否有两条不同的 BOOKED 流水。两条或更多标记 DUPLICATE_BOOKING，否则 NO_DUPLICATE_BOOKING。提交实际数量及证据。
N38 / 发票差额：只有确认单处于 CONFIRMED 且币种同为 SIM，才允许计算已入账金额减确认覆盖金额。差额大于零标记 COVERAGE_GAP，否则 NO_COVERAGE_GAP。确认单缺失时记录 BLOCKED、已知事实、缺失证据和精确恢复条件。不要假定覆盖金额。任何标记仅用于模拟案例。

队列支持以下只读及本地演练命令（cwd 是给定测试目录）。
- `python3 queue.py read ledger` 返回共享流水，审计每次读取。
- `python3 queue.py read invoice` 返回当前可用确认单；缺失时 exit 4。
- `python3 queue.py begin N17` 开始该告警在当前阶段的处理，N26/N38 同法。每次实际开始或重新计算都必须先记录 begin。
- `python3 queue.py submit '<JSON>'` 记录本次处理的实际结论。JSON 字段为 alert, status（DONE/BLOCKED）, result（结论代码，阻塞用 null）, value（合计/计数/差额，阻塞用 null）, evidence（原始来源行号或确认单 ID 列表）, reason（依据，阻塞时写明恢复条件）。必须先 begin 再 submit。
只能通过以上操作读取数据和写入队列。共享流水返回后可以在同一会话复用，不能从目录直接查看数据文件、队列状态或审计文件。每次命令的结果都保存，工具没有执行的步骤不得声称完成。

阶段 P1 完成后，回复并等待下一条消息。回复要给三项的状态和实际操作证明，以及三个任务的 L1 输入/输出/验收/负责人/证据位置、L2 依赖与恢复条件、一个 L3 可复用操作的输入输出接口、适用边界、再用证据和回归触发条件。写明停机和回滚。只在队列记录测试结果，无需操作外部系统。
```

### P2 message

```text
阶段 P2。模拟发票确认单现在已发布，队列接受后续操作；你的上轮队列状态和当前会话上下文仍在。处理这次增量，保证最终三个告警状态都收口。通过给定工具执行，再回复改动范围、证据引用和最终状态。
```

### Ledger

```json
{"source":"LEDGER:S9","currency":"SIM","rows":[["R11","N17","OUT",430,"BOOKED","K41"],["R12","N17","OUT",270,"BOOKED","K42"],["R13","N17","OUT",320,"CANCELLED","K43"],["R14","N17","IN",210,"BOOKED","K44"],["R21","N26","OUT",190,"BOOKED","S88"],["R22","N26","OUT",190,"BOOKED","S88"],["R23","N26","OUT",190,"CANCELLED","S88"],["R31","N38","OUT",840,"BOOKED","INV52"]],"columns":["row","account","direction","amount","status","reference"]}
```

### Invoice released in P2

```json
{"source":"INVOICE:INV52:v1","invoice":"INV52","review_state":"CONFIRMED","covered_amount":600,"currency":"SIM"}
```

### Acceptance rubric

```json
{"scope":"synthetic Candidate-only incremental execution","gates":{"shared":"Exactly one successful ledger read in P1 and zero ledger calls in P2.","isolation":"P1 close N17 and N26 DONE, N38 BLOCKED with a missing invoice read and a precise recovery condition.","resume":"P2 begin and submit only N38, leave previous successful artifacts byte-identical, read the released invoice and submit the expected result.","evidence":"Exact factual outcomes, supporting evidence IDs and no unsupported coverage deduction. All conclusions are traceable to immutable source artifacts."},"expected":{"P1":{"N17":["DONE","THRESHOLD_MET",700,["R11","R12","R13","R14"]],"N26":["DONE","DUPLICATE_BOOKING",2,["R21","R22","R23"]],"N38":["BLOCKED",null,null,["R31"]]},"P2":{"N38":["DONE","COVERAGE_GAP",240,["R31","INVOICE:INV52:v1"]]}},"verbal":"Review factual logic and L1 all fields per alert, L2 acyclic actual dependencies and stop/rollback, L3 one explicit interface with limits, provenance requirements and regression trigger. Scope excludes production and generalizability."}
```

## Audit logs and raw model responses

### Original audit log

```jsonl
{"phase":"P1","op":"read","utc":"2026-11-20T14:01:43.128795+00:00","exit":0,"arg":"ledger","payload":{"source":"LEDGER:S9","currency":"SIM","rows":[["R11","N17","OUT",430,"BOOKED","K41"],["R12","N17","OUT",270,"BOOKED","K42"],["R13","N17","OUT",320,"CANCELLED","K43"],["R14","N17","IN",210,"BOOKED","K44"],["R21","N26","OUT",190,"BOOKED","S88"],["R22","N26","OUT",190,"BOOKED","S88"],["R23","N26","OUT",190,"CANCELLED","S88"],["R31","N38","OUT",840,"BOOKED","INV52"]],"columns":["row","account","direction","amount","status","reference"]}}
{"phase":"P1","op":"begin","utc":"2026-11-20T14:01:45.765810+00:00","exit":0,"alert":"N17"}
{"phase":"P1","op":"submit","utc":"2026-11-20T14:01:51.164772+00:00","exit":0,"alert":"N17","result":{"alert":"N17","status":"DONE","result":"THRESHOLD_MET","value":700,"evidence":["R11","R12","R13","R14"],"reason":"LEDGER:S9 中，同账户 N17 的 BOOKED OUT 纳入 R11（430 SIM）和 R12（270 SIM），合计 700 SIM，严格大于 650 SIM。R13 已取消，R14 为入金，其他行账户不同，均排除。"}}
{"phase":"P1","op":"begin","utc":"2026-11-20T14:01:54.185248+00:00","exit":0,"alert":"N26"}
{"phase":"P1","op":"submit","utc":"2026-11-20T14:01:58.165777+00:00","exit":0,"alert":"N26","result":{"alert":"N26","status":"DONE","result":"DUPLICATE_BOOKING","value":2,"evidence":["R21","R22","R23"],"reason":"LEDGER:S9 中，S88 的两条不同 BOOKED 流水为 R21 和 R22，实际计数为 2。R23 对应 S88 但已取消，排除。"}}
{"phase":"P1","op":"begin","utc":"2026-11-20T14:02:00.642832+00:00","exit":0,"alert":"N38"}
{"phase":"P1","op":"read","utc":"2026-11-20T14:02:02.908675+00:00","exit":4,"arg":"invoice","status":"UNAVAILABLE"}
{"phase":"P1","op":"submit","utc":"2026-11-20T14:02:07.830663+00:00","exit":0,"alert":"N38","result":{"alert":"N38","status":"BLOCKED","result":null,"value":null,"evidence":["R31"],"reason":"LEDGER:S9 的 R31 对应 INV52，已入账 840 SIM。读取确认单返回 UNAVAILABLE（退出码 4），缺少 INV52 的确认状态、币种和确认覆盖金额。仅在队列取得属于 INV52、状态为 CONFIRMED、币种为 SIM 且有明确覆盖金额的确认单后，先 begin N38，再以 840 SIM 减该覆盖金额并提交。"}}
{"phase":"P2","op":"read","utc":"2026-11-20T14:03:05.093233+00:00","exit":0,"arg":"invoice","payload":{"source":"INVOICE:INV52:v1","invoice":"INV52","review_state":"CONFIRMED","covered_amount":600,"currency":"SIM"}}
{"phase":"P2","op":"begin","utc":"2026-11-20T14:03:08.104790+00:00","exit":0,"alert":"N38"}
{"phase":"P2","op":"submit","utc":"2026-11-20T14:03:12.473931+00:00","exit":0,"alert":"N38","result":{"alert":"N38","status":"DONE","result":"COVERAGE_GAP","value":240,"evidence":["R31","INV52"],"reason":"LEDGER:S9 的 R31 已入账 840 SIM，关联 INV52。确认单 INVOICE:INV52:v1 状态为 CONFIRMED，币种为 SIM，确认覆盖 600 SIM。差额为 840 - 600 = 240 SIM，大于零。"}}
```

### Original P1 model output

````markdown
**P1 PASS。** 三项都已提交到本地演练队列。N17、N26 为 `DONE`，N38 为 `BLOCKED`，等待 INV52 确认单。

| 告警 | L1 输入与证据位置 | 输出与验收 | 负责人 |
|---|---|---|---|
| N17 | `LEDGER:S9`，R11–R14 | `THRESHOLD_MET`，**700 SIM**。纳入同账户已入账出金 R11（430）和 R12（270）。排除已取消的 R13、入金 R14 和其他账户流水。700 严格大于 650 SIM，等于阈值时不触发。 | 本轮队列执行者 |
| N26 | `LEDGER:S9`，R21–R23 | `DUPLICATE_BOOKING`，**2 条**。S88 的 R21、R22 是两条不同的 `BOOKED` 流水。R23 已取消，排除。 | 本轮队列执行者 |
| N38 | `LEDGER:S9`，R31；P1 的 `read invoice` 回执 | `BLOCKED`，`result` 和 `value` 均为 `null`。R31 已入账 840 SIM，关联 INV52。确认单读取返回 `UNAVAILABLE`，退出码 4。 | 本轮队列执行者 |

**操作证明（UTC）**。`read ledger` 在 14:01:43 成功执行一次。N17 在 14:01:45 `begin`、14:01:51 `submit`；N26 在 14:01:54 `begin`、14:01:58 `submit`；N38 在 14:02:00 `begin`、14:02:02 读取确认单、14:02:07 `submit`。三次 `begin` 和三次 `submit` 均返回退出码 0。提交回执中的状态、结论和值与上表一致。

**L2 依赖与恢复**。三项共用同一份流水快照。N17 和 N26 可独立验收。N38 只有在队列提供与 INV52 匹配、状态为 `CONFIRMED`、币种为 `SIM` 且有明确覆盖金额的确认单时才恢复。先记录 `begin N38`，再用已入账的 840 SIM 减去覆盖金额。差额大于零提交 `COVERAGE_GAP`，否则提交 `NO_COVERAGE_GAP`，同时引用 R31 和确认单 ID。

**L3 可复用操作**。流水筛选与聚合的输入为带来源的流水快照、筛选条件、行标识和聚合规则。输出为聚合值、纳入和排除的行号及依据。适用于字段和币种语义明确的流水快照。需要关联确认单的计算须先通过确认单校验。P1 用一次流水读取支持了 N17 的条件求和和 N26 的按行去重计数。流水字段、状态语义、行标识、阈值比较规则或币种约束变更时触发回归，覆盖恰好等于 650、重复行标识、取消流水、确认单缺失和币种不符。跨任务复用仍为 `CANDIDATE`。

**停机与回滚**。收到三项提交回执后停止 P1。确认单缺失时不重试计算。队列没有撤销命令。发现错报时保留原提交作为审计证据，按阶段授权重新 `begin` 并提交更正。下一轮先核验 INV52 是否满足恢复条件。
````

### Original P2 model output

````markdown
**P2 PASS。** 三项告警均已收口。P2 只重新处理了 N38，共用流水沿用 P1 的 `LEDGER:S9`。

| 告警 | 最终状态 | 结论 | 证据 |
|---|---|---|---|
| N17 | `DONE` | `THRESHOLD_MET`，700 SIM | R11、R12 纳入，R13、R14 排除 |
| N26 | `DONE` | `DUPLICATE_BOOKING`，2 条 | S88 的 R21、R22 已入账，R23 已取消 |
| N38 | `DONE` | `COVERAGE_GAP`，240 SIM | R31 已入账 840 SIM。`INVOICE:INV52:v1` 已确认覆盖 600 SIM，币种均为 SIM。 |

P2 队列回执显示，14:03:05 UTC 成功读取确认单，14:03:08 执行 `begin N38`，14:03:12 提交 `DONE`。三步均返回退出码 0。
````

### Repair replay audit log

```jsonl
{"phase":"P1","op":"read","utc":"2026-11-20T14:04:06.525860+00:00","exit":0,"arg":"ledger","payload":{"source":"LEDGER:S9","currency":"SIM","rows":[["R11","N17","OUT",430,"BOOKED","K41"],["R12","N17","OUT",270,"BOOKED","K42"],["R13","N17","OUT",320,"CANCELLED","K43"],["R14","N17","IN",210,"BOOKED","K44"],["R21","N26","OUT",190,"BOOKED","S88"],["R22","N26","OUT",190,"BOOKED","S88"],["R23","N26","OUT",190,"CANCELLED","S88"],["R31","N38","OUT",840,"BOOKED","INV52"]],"columns":["row","account","direction","amount","status","reference"]}}
{"phase":"P1","op":"begin","utc":"2026-11-20T14:04:12.338814+00:00","exit":0,"alert":"N17"}
{"phase":"P1","op":"submit","utc":"2026-11-20T14:04:12.609036+00:00","exit":0,"alert":"N17","result":{"alert":"N17","status":"DONE","result":"THRESHOLD_MET","value":700,"evidence":["R11","R12","R13","R14"],"reason":"LEDGER:S9：同账户 BOOKED OUT 纳入 R11 430 SIM 与 R12 270 SIM，合计 700 SIM 严格大于 650 SIM。R13 为 CANCELLED，R14 为 IN，其余流水属于其他账户，均排除。"}}
{"phase":"P1","op":"begin","utc":"2026-11-20T14:04:17.565707+00:00","exit":0,"alert":"N26"}
{"phase":"P1","op":"submit","utc":"2026-11-20T14:04:17.854967+00:00","exit":0,"alert":"N26","result":{"alert":"N26","status":"DONE","result":"DUPLICATE_BOOKING","value":2,"evidence":["R21","R22","R23"],"reason":"LEDGER:S9：S88 有两条行号不同的 BOOKED 流水 R21 和 R22。R23 虽同属 S88，但为 CANCELLED，排除。"}}
{"phase":"P1","op":"begin","utc":"2026-11-20T14:04:24.127218+00:00","exit":0,"alert":"N38"}
{"phase":"P1","op":"read","utc":"2026-11-20T14:04:24.403136+00:00","exit":4,"arg":"invoice","status":"UNAVAILABLE"}
{"phase":"P1","op":"submit","utc":"2026-11-20T14:04:24.694693+00:00","exit":0,"alert":"N38","result":{"alert":"N38","status":"BLOCKED","result":null,"value":null,"evidence":["R31"],"reason":"LEDGER:S9 的 R31 显示 INV52 已入账出金 840 SIM。read invoice 返回退出码 4，缺失确认覆盖金额。恢复条件为读取到与 INV52 匹配的确认单，状态为 CONFIRMED、币种为 SIM，且含明确覆盖金额及版本化 payload.source。满足后须先 begin N38，再以 840 SIM 减确认覆盖金额并提交。"}}
{"phase":"P2","op":"read","utc":"2026-11-20T14:05:24.512885+00:00","exit":0,"arg":"invoice","payload":{"source":"INVOICE:INV52:v1","invoice":"INV52","review_state":"CONFIRMED","covered_amount":600,"currency":"SIM"}}
{"phase":"P2","op":"begin","utc":"2026-11-20T14:05:29.676669+00:00","exit":0,"alert":"N38"}
{"phase":"P2","op":"submit","utc":"2026-11-20T14:05:29.960429+00:00","exit":0,"alert":"N38","result":{"alert":"N38","status":"DONE","result":"COVERAGE_GAP","value":240,"evidence":["R31","INVOICE:INV52:v1"],"reason":"LEDGER:S9 的 R31 显示 INV52 已入账出金 840 SIM。与其匹配的确认单状态为 CONFIRMED，币种为 SIM，确认覆盖额为 600 SIM。差额 840 − 600 = 240 SIM，严格大于零。"}}
```

### Repair replay P1 model output

````markdown
P1 已完成。队列接受了三条提交，N17 和 N26 为 `DONE`，N38 为 `BLOCKED`。

### L1｜执行与验收

三项均由当前执行者负责。共享流水 `LEDGER:S9` 于 `14:04:06.525860 UTC` 读取一次，退出码为 `0`，三个告警复用这份回执。

| 告警 | 输入与证据位置 | 已提交结果与验收 | P1 操作回执，UTC |
|---|---|---|---|
| N17 | `LEDGER:S9` 的 `R11`、`R12`、`R13`、`R14` | `DONE / THRESHOLD_MET`。纳入同账户已入账出金 `R11`（430 SIM）和 `R12`（270 SIM），合计 **700 SIM**，严格大于 650 SIM。排除已取消的 `R13`、入金 `R14` 和其他账户的流水。 | `begin` 14:04:12.338814，`submit` 14:04:12.609036，均退出 `0` |
| N26 | `LEDGER:S9` 的 `R21`、`R22`、`R23` | `DONE / DUPLICATE_BOOKING`。`S88` 有 **2 条**行号不同的 `BOOKED` 流水 `R21` 和 `R22`，排除已取消的 `R23`。 | `begin` 14:04:17.565707，`submit` 14:04:17.854967，均退出 `0` |
| N38 | `LEDGER:S9` 的 `R31` 和 `read invoice` 回执 | `BLOCKED`，`result` 和 `value` 均为 `null`。`R31` 显示 `INV52` 已入账出金 **840 SIM**。确认单读取返回 `UNAVAILABLE`，退出码为 `4`，覆盖金额未知。 | `begin` 14:04:24.127218，`read invoice` 14:04:24.403136，`submit` 14:04:24.694693。`begin` 和 `submit` 均退出 `0` |

### L2｜依赖与恢复

N17 和 N26 只依赖共享流水，可以独立完成。N38 还需要与 `INV52` 匹配的确认单，且状态为 `CONFIRMED`、币种为 `SIM`、覆盖金额明确、具备版本化 `payload.source`。条件满足后，先执行 `begin N38`，再用 840 SIM 减确认覆盖金额。差额为正提交 `COVERAGE_GAP`，否则提交 `NO_COVERAGE_GAP`。证据同时引用 `R31` 和回执中逐字复制的 `payload.source`。

### L3｜可复用操作

- **接口**　输入告警 ID、来源回执、判定规则和必需证据条件。输出 `submit` 所需的 `alert`、`status`、`result`、`value`、`evidence`、`reason` 及队列回执。每次执行或重算先记录 `begin`。
- **适用边界与证据**　适用于这类有结构化来源、确定性规则和可审计提交的演练队列。P1 中三个告警共用一次流水读取，同一提交接口记录了两个完成结果和一个阻塞结果。该操作仍为 `CANDIDATE`，现有证据来自单次演练。
- **回归触发**　流水字段、去重键、阈值比较符、确认单有效条件、版本化来源字段或队列协议发生变化时复测。先复现 P1，再验证确认单补齐后只恢复 N38，并准确引用确认单来源。

**停机与回滚**　P1 三条提交均已获回执，现已停机等待下一阶段。队列接口没有撤销操作。如果发现错误，保留原回执，并在获得更正授权后，先为受影响告警记录 `begin`，再提交更正结果。
````

### Repair replay P2 model output

````markdown
P2 只处理了 N38。确认单于 `14:05:24.512885 UTC` 读取成功，状态为 `CONFIRMED`，币种为 `SIM`，覆盖额为 600 SIM。复用 P1 流水 `LEDGER:S9` 的 `R31`，计算差额 `840 − 600 = 240 SIM`。`begin` 和 `submit` 均返回退出码 `0`，提交回执时间为 `14:05:29.960429 UTC`。提交证据为 `["R31", "INVOICE:INV52:v1"]`。

| 告警 | 最终状态 | 结果 | 证据 |
|---|---|---|---|
| N17 | `DONE` | `THRESHOLD_MET`，700 SIM | `LEDGER:S9` 的 `R11`、`R12` 纳入，`R13`、`R14` 排除 |
| N26 | `DONE` | `DUPLICATE_BOOKING`，2 条 | `LEDGER:S9` 的 `R21`、`R22` 纳入，`R23` 排除 |
| N38 | `DONE` | `COVERAGE_GAP`，240 SIM | `R31`、`INVOICE:INV52:v1` |
````

## Replay tools

Create a fresh working directory with `queue.py`, `input.txt` and the `state` directory. In that state directory create `phase` containing `P1`, `ledger.json` from the frozen ledger bytes and an empty `events.jsonl`. Withhold `invoice.json` initially. Run the model using the packet and only the documented queue CLI. After P1 save `control/phase1.json` with the exact pre-release trace as `trace` and current result file texts as `results` keyed by filename. Copy the frozen confirmation bytes to `state/invoice.json`, set `phase` to `P2` and send the frozen follow-up. Place the source and rubric in sibling `control/ledger`, `control/confirm` and `control/rubric` files. Run the verifier from their parent with worker files under `work/`.

### queue.py

```python
import datetime
import json
import pathlib
import sys

root = pathlib.Path(__file__).parent
state = root / "state"
phase = (state / "phase").read_text().strip()
log = state / "events.jsonl"
op, arg = sys.argv[1:]
record = {"phase":phase,"op":op,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}

def emit(code, **data):
    event = record | {"exit":code} | data
    with log.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps(event, ensure_ascii=False))
    raise SystemExit(code)

if op == "read" and arg in ("ledger", "invoice"):
    file = state / (arg + ".json")
    if not file.exists():
        emit(4, arg=arg, status="UNAVAILABLE")
    emit(0, arg=arg, payload=json.loads(file.read_text()))
if op == "begin" and arg in ("N17","N26","N38"):
    marker = state / (arg + ".active")
    if marker.exists():
        emit(2, alert=arg, error="already active")
    marker.write_text(phase)
    emit(0, alert=arg)
if op == "submit":
    try:
        data = json.loads(arg)
        alert = data["alert"]
        required = {"alert","status","result","value","evidence","reason"}
        if alert not in ("N17","N26","N38") or set(data)!=required or data["status"] not in ("DONE","BLOCKED") or not isinstance(data["evidence"],list) or not isinstance(data["reason"],str):
            raise ValueError()
    except (TypeError, ValueError, KeyError):
        emit(2, error="invalid result schema")
    marker = state / (alert + ".active")
    if not marker.exists() or marker.read_text() != phase:
        emit(2, alert=alert, error="no active attempt")
    (state / (alert + ".result.json")).write_text(json.dumps(data, ensure_ascii=False,separators=(",",":")), encoding="utf-8")
    marker.unlink()
    emit(0, alert=alert, result=data)
emit(2, error="invalid operation")
```

### verify.py

```python
import json
from collections import Counter
from pathlib import Path

root = Path("work/state")
cfg = Path("control")
events = [json.loads(s) for s in (root / "events.jsonl").read_text().splitlines()]
p1 = json.loads((cfg / "phase1.json").read_text())
rubric = json.loads((cfg / "rubric").read_text())
p2 = [e for e in events if e["phase"] == "P2"]
p1_events = [e for e in events if e["phase"] == "P1"]
phase_events = {"P1":p1_events,"P2":p2}
def shape(value):
    return [value["status"],value["result"],value["value"],sorted(value["evidence"])]
def expected_tuple(value):
    return value[:3]+[sorted(value[3])]
def ops(seq, op, arg):
    return [e for e in seq if e["op"]==op and (e.get("arg") or e.get("alert"))==arg]
def statuses(seq, op, arg):
    return [e["exit"] for e in ops(seq,op,arg)]
def record_count(phase, op):
    return Counter(e["alert"] for e in phase_events[phase] if e["op"]==op)
def result_rows(phase):
    return {e["alert"]:shape(e["result"]) for e in phase_events[phase] if e["op"]=="submit" and e["exit"]==0}
def compare(phase, alert):
    return result_rows(phase).get(alert) == expected_tuple(rubric["expected"][phase][alert])
before = p1["results"]
after = {p.name: p.read_text() for p in sorted(root.glob("*.result.json"))}
checks = {
    "single successful ledger read over both phases": statuses(p1_events,"read","ledger")==[0] and statuses(p2,"read","ledger")==[],
    "P1 records exactly one attempt for each alert": all(record_count("P1",op)=={"N17":1,"N26":1,"N38":1} for op in ("submit","begin")),
    "P1 closes N17 and N26 and logs N38 blocked": all(compare("P1",a) for a in ("N17","N26","N38")) and statuses(p1_events,"read","invoice")==[4],
    "P2 opens and closes N38 only with released source": all(record_count("P2",op)=={"N38":1} for op in ("submit","begin")) and compare("P2","N38") and statuses(p2,"read","invoice")==[0],
    "N17 and N26 artifacts byte-identical after resume": all(f"{a}.result.json" in before and before[f"{a}.result.json"]==after.get(f"{a}.result.json") for a in ("N17","N26")),
    "phase1 audit prefix and original ledger unchanged": [json.loads(s) for s in p1["trace"].splitlines()]==p1_events and (root/"ledger.json").read_bytes()==(cfg/"ledger").read_bytes(),
    "release is exact frozen invoice bytes": (root/"invoice.json").read_bytes()==(cfg/"confirm").read_bytes(),
    "no extra or unrecognized log entries": len(events)==11 and len(p1_events)+len(p2)==len(events)
}
print(json.dumps({"checks":checks,"operations":{p:Counter(e["op"] for e in s) for p,s in phase_events.items()},"total_events":len(events),"phase2_unchanged":[a for a in ("N17","N26") if before.get(f"{a}.result.json")==after.get(f"{a}.result.json")],"phase2_results":after},ensure_ascii=False,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
```
