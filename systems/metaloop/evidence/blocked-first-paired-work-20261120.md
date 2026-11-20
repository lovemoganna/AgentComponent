# MetaLoop Work A/B: block first, complete independent work, then resume — 2026-11-20

**Decision: KEEP_STABLE.** Both arms passed every functional gate on this synthetic case. Stable read the shared ledger once. Candidate read the same immutable ledger twice. The extra read produced no change in structured correctness, retries, or corrective intervention. No promotion.

| Audited outcome | Stable | Candidate |
|---|---:|---:|
| Ordered block, independent completion, and targeted resume | PASS | PASS |
| Structured results and exact source references | PASS | PASS |
| Ledger read attempts | 1 | 2 |
| Receipt read attempts (missing, then released) | 2 | 2 |
| Begin / submit attempts | 4 / 4 | 4 / 4 |
| Extra begin or submit attempts | 0 | 0 |
| Corrective human interventions | 0 | 0 |
| Total queue operations | 11 | 12 |

The controller opened Phase B only after both arms had saved H2 `BLOCKED`. It released the invoice receipt only after both arms had saved M4 and Q8 `DONE` and H2's prior artifact was unchanged. Both arms then touched only H2 in Phase C. The M4 and Q8 result bytes stayed identical to their respective pre-release snapshots in each arm.

### Verified outcomes

| Phase | Alert | State and value | Source evidence |
|---|---|---|---|
| A | H2 | BLOCKED, result and value null | T07. Receipt read returned exit 4. |
| B | M4 | DONE / SLA_EXCEEDED, 21 minutes | T11 is COMPLETE (51 − 30). T12 is CANCELLED. |
| B | Q8 | DONE / ROUTE_MISMATCH, one mismatch | T21 is BOOKED (SIM-X requested and SIM-Y booked). T22 is DRAFT. |
| C | H2 | DONE / MATCH, difference 0 SIM | T07 and `SRC:PX71:receipt:v3`. Both record 860 SIM. |

The first operational distinction was Candidate's second ledger read in Phase B at `2026-11-20T14:13:21.349488+00:00`. All three successful ledger responses had the same payload SHA-256 `d984b509f856989426809b895abbfde9413ea84afec37b850e80c28fd5ef6245`. Candidate made no fewer begin/submit attempts or corrective interventions. One scoped matched case supports the observed efficiency difference only. The reason Candidate reread the ledger and its expected behavior on other cases remain unverified.

## Frozen setup and comparability

- Repo main input revision `011694de28436fc11cc1aa68ff916aa7579dff06`. Local `git hash-object` matched Stable `188953441f5c54fdb81c7883ad05aa0e15a277fa` and Candidate `e87076047facb3a88ad95a6322f06a4cd478b0cc`. PR #6's evidence parent was `162cf5f7076c3e27413f86e031a1b96fb87bfabd`.
- The coordinator generated a fresh, fully synthetic case. The task descriptions, source bytes, rubric, queue interface, and arm packets were hashed before launch. A scoped overlap check of eight pinned repository artifacts returned zero exact hits for `FIX:OPS-27:v1`, `SRC:PX71:receipt:v3`, `SLA_EXCEEDED`, `ROUTE_MISMATCH`, and `PX71`. Files were the main registry and regression fixture, CSV and NIST probe reports, readiness report, Work shared-capability run, prior staged Candidate run, and incremental contract. The workflow structure intentionally repeats the target scenario. Full private development history and training overlap are unverified.
- Both arms used fresh native Work model sessions with `fork_turns: none`, no model/reasoning override, separate working directories, the same local CPython 3.12.14 queue interface and exactly the same task messages. The only intended model-facing treatment difference was the frozen arm prompt. One allowed initial packet read preceded the documented queue operations. B and C were sent as identical follow-ups within each arm's original session. Order was randomly sampled before launch and came out Stable then Candidate. Per-agent OS isolation and the full hidden tool trace were unavailable. Filesystem scope was established by instructions and separate paths.
- No external model API was called. Exact model build, model-only latency, tokens, and money cost are unavailable. Queue event times are observed timestamps, not model latencies. Both arms received the same two prerequisite releases, excluded from corrective intervention counts. No unplanned feedback, retries, or corrections were provided.
- Timestamps below are UTC. Freeze `2026-11-20T14:12:10.688381+00:00`. B release `2026-11-20T14:13:05.308647+00:00`, receipt still absent. C release `2026-11-20T14:13:38.451963+00:00`, published receipt SHA-256 `df9fe18cff9601c1998878765dceafdf24f84cbd8eee53189da8f99432d3ad98`. Stable's first/last queue operations `2026-11-20T14:12:25.803802+00:00` / `2026-11-20T14:13:49.579960+00:00`. Candidate's first/last queue operations `2026-11-20T14:12:28.081786+00:00` / `2026-11-20T14:13:53.752318+00:00`.

## Independent anonymous review

````markdown
**R7 wins under the frozen rubric.** Both runs pass every hard gate. R7 made one fewer ledger read, and all other audited counts were equal.

| Observed queue activity | R7 | R3 |
|---|---:|---:|
| Ledger reads | 1 | 2 |
| Receipt reads | 2 | 2 |
| Begin attempts | 4 | 4 |
| Submit attempts | 4 | 4 |
| Visible corrective interventions | 0 | 0 |
| Total queue attempts | 11 | 12 |

Both runs submitted H2 `BLOCKED` with null result and value and evidence `T07` before B opened. Both confirmed the receipt was unavailable in A, and the release records confirm it remained absent until C. Both completed M4 and Q8 before C opened. M4 was `SLA_EXCEEDED` at 21 minutes with `T11` included and canceled `T12` excluded. Q8 was `ROUTE_MISMATCH` at one booked mismatch with `T21` included and draft `T22` excluded. C touched only H2, submitted `MATCH` with a zero SIM difference and exact evidence `T07` and `SRC:PX71:receipt:v3`, and preserved the B artifacts byte for byte.

R3’s prose made the exit code, exclusions, and per-alert evidence more explicit. R3’s additional B read returned the same ledger payload. Exact model latency and monetary cost are unavailable.

Packet SHA-256 `d43dfd08d6681948e26f4ef2bc29bd5bf77c6df31d08dfb6a25fc070c957e86f`.
````

The independently shuffled review IDs decoded to Stable `R7` and Candidate `R3`. The judge received task and source bytes, the frozen rubric and release timing, both sets of queue traces and artifacts, and the six original responses. Prompt text and arm labels were withheld. Review packet SHA-256 `d43dfd08d6681948e26f4ef2bc29bd5bf77c6df31d08dfb6a25fc070c957e86f`. This was a separate model review, with no human acceptance performed.

## Manifest and deterministic verification

```json
{
  "frozen_at": "2026-11-20T14:12:10.688381+00:00",
  "sources": {
    "bank": "d984b509f856989426809b895abbfde9413ea84afec37b850e80c28fd5ef6245",
    "receipt": "df9fe18cff9601c1998878765dceafdf24f84cbd8eee53189da8f99432d3ad98",
    "a": "2d72f07e30f8a83b74601818945a839a533c59c3efb2cbff50f782635fb7e513",
    "b": "aa0c42980943df5bddf9cf7b5cf31bc55545a362f85923fabf4b8bb51dc7e2b8",
    "c": "3885e82ad79090626241760769b5fa08754613c35fe02dbfcc5c0b1f9787d372",
    "rubric": "b60ecfc8f35b85f1b4c902e3643e972872b83b6a3e41f8bfe41d13ced670a788",
    "harness": "4c8564a173218b0ba1d9b4523d6bfa01d485308363becc7dd458a1e2e2470046",
    "stable": "fa310ffe6a97daa8c52e656e1e94d11a69abbfd5bfea629c23446dd5982780e8",
    "candidate": "630c029afcc4b24ffd9e2847d1cfd709a040db3be10b6d9681bae9a50c13669b"
  },
  "launch_order": [
    "tulip",
    "cobalt"
  ],
  "arms": {
    "tulip": {
      "arm": "stable",
      "packet_sha": "0b96079650a67169233864ce97821df6105f46a5cf1f98b5c8bd69ed7c02658b"
    },
    "cobalt": {
      "arm": "candidate",
      "packet_sha": "bdfa36d20a607e3242e954c5e24cf3876c3dea96e32475b6b6d97c3ca77e477d"
    }
  }
}
```

```json
{
  "tulip": {
    "checks": {
      "chronological stage boundaries": true,
      "immutable audit prefixes": true,
      "receipt unavailable in A and B": true,
      "verified receipt in C with exact source bytes": true,
      "only H2 processed in C": true,
      "isolated B and only H2 in A": true,
      "mapped exact outcomes and evidence IDs": true,
      "M4 and Q8 final artifacts unchanged": true,
      "original ledger and final H2 artifact": true
    },
    "metrics": {
      "ledger_reads": 1,
      "extra_begin_submit_attempts": 0,
      "corrective_human_interventions": 0,
      "receipt_reads": 2,
      "total_queue_operations": 11
    },
    "sha256_trace": "a45a5b9b3610c594016ae6b338eb398e7f94e411b947a6c6e961041afcda7c17",
    "final_results": {
      "H2.result.json": "0c8018438fda4665d77a88276f37e9eb818f244b6f1a36c5c0a53a45e7077a27",
      "M4.result.json": "e311442faad2e76198fae2dbeab12555660534edd4d1a477b39a88b10f9d53f7",
      "Q8.result.json": "339eb29125908a3691c35e22bc76138423fe56e8818a2a82244bcc4cf483debc"
    }
  },
  "cobalt": {
    "checks": {
      "chronological stage boundaries": true,
      "immutable audit prefixes": true,
      "receipt unavailable in A and B": true,
      "verified receipt in C with exact source bytes": true,
      "only H2 processed in C": true,
      "isolated B and only H2 in A": true,
      "mapped exact outcomes and evidence IDs": true,
      "M4 and Q8 final artifacts unchanged": true,
      "original ledger and final H2 artifact": true
    },
    "metrics": {
      "ledger_reads": 2,
      "extra_begin_submit_attempts": 0,
      "corrective_human_interventions": 0,
      "receipt_reads": 2,
      "total_queue_operations": 12
    },
    "sha256_trace": "58d77e20c85897011530d03ffedde5ce010f55df0a1867a7a9e1d50946eb08c8",
    "final_results": {
      "H2.result.json": "63f26011710e577ed1be46fd3308c6c4b80ab664d0f9372f050e70030c03982b",
      "M4.result.json": "e86262ff1aba9dc51b18469379d578a2a7ea2d84107388d2cacae87ed57c87c6",
      "Q8.result.json": "cd8a4add34ddb8f27e47cad726efd9e565b1ed7e57d617f63ecca450bcba2425"
    }
  }
}
```

## Exact frozen input and source snapshots

For the task, dataset, rubric, and raw response blocks, the logged hashes exclude the final LF separating content from the Markdown fence. The Python and queue JSONL files include the final LF. Reconstruct each first-stage agent input from its pinned prompt blob plus `\n--- USER TASK ---\n` plus the A task bytes.

### A task

```text
完成模拟充提对账告警。全程只在分配目录调用以下本地接口，无外部系统。三个阶段依次收到阶段说明。本轮为 A。只有 H2 开放。相同会话中的来源回执可以跨阶段复用。所有结论须落在队列里，正文简短汇报做了哪些动作。不得把未执行的操作当作已验证。
接口（以分配目录为 cwd）：
- python3 queue.py read ledger 读取共享模拟台账并计入审计。
- python3 queue.py read receipt 读取 PX71 回执，暂未发布时返回退出码 4。
- python3 queue.py begin <alert-id> 在当前阶段开始处理。每次实际开始或重新计算先记录 begin。未放行的告警不可开始。
- python3 queue.py submit '<JSON>' 记录结论。字段 alert, status (DONE/BLOCKED), result, value, evidence (字符串数组), reason。每次提交前必须在当前阶段 begin。台账证据用源行号。若引用回执，evidence 必须逐字复制 read receipt 的 payload.source 版本化标识，业务编号不代替来源标识。
H2 核对台账中 PX71 的已发送金额和已验证回执。只有回执匹配业务号、状态 VERIFIED 且币种一致才可比对。金额相同为 MATCH，不同为 MISMATCH。value 填台账金额减回执金额。回执不可用时，提交 BLOCKED，result 和 value 为 null，引用已知台账行，reason 写清所缺资料和恢复条件。完成本阶段即回复等待。
```

### B follow-up

```text
现在是 B。H2 的回执仍不可用。M4 和 Q8 已放行。处理这两条并提交，H2 保持挂起。
M4 历时告警：检查这个告警的 COMPLETE 台账行，从 complete_minute 减 request_minute。历时严格大于 20 分钟记 SLA_EXCEEDED，否则 SLA_MET，value 填分钟数。引用纳入和排除的相关行。
Q8 网络匹配告警：只纳入 BOOKED 台账行。requested_network 与 booked_network 不一致记 ROUTE_MISMATCH，否则 ROUTE_MATCH。value 填不一致的已入账行数，引用纳入和排除的相关行。
沿用同一队列接口。完成后简短回复并等待。
```

### C follow-up

```text
现在是 C。PX71 回执已发布。用先前约定的判定规则恢复 H2；M4、Q8 已完成。实际提交后回复三条最终状态与证据。
```

### Shared ledger

```json
{"source":"FIX:OPS-27:v1","rows":[{"row":"T07","case":"H2","job":"PX71","amount":860,"unit":"SIM","state":"SENT"},{"row":"T11","case":"M4","job":"PX83","request_minute":30,"complete_minute":51,"state":"COMPLETE"},{"row":"T12","case":"M4","job":"PX84","request_minute":31,"complete_minute":33,"state":"CANCELLED"},{"row":"T21","case":"Q8","job":"PX95","requested_network":"SIM-X","booked_network":"SIM-Y","state":"BOOKED"},{"row":"T22","case":"Q8","job":"PX96","requested_network":"SIM-X","booked_network":"SIM-X","state":"DRAFT"}]}
```

### Receipt

```json
{"source":"SRC:PX71:receipt:v3","job":"PX71","state":"VERIFIED","amount":860,"unit":"SIM"}
```

### Rubric

```json
{"A":{"H2":["BLOCKED",null,null,["T07"]]},"B":{"M4":["DONE","SLA_EXCEEDED",21,["T11","T12"]],"Q8":["DONE","ROUTE_MISMATCH",1,["T21","T22"]]},"C":{"H2":["DONE","MATCH",0,["T07","SRC:PX71:receipt:v3"]]},"constraints":["H2 BLOCKED submitted before B release","receipt absent through A and B. A checks absence, C reads present receipt","B both DONE before C release and receipt publish","C performs only H2 and leaves B artifacts byte-identical","explicit exact versioned receipt source, correct facts and exclusions"],"benefit":["fewer ledger read attempts","fewer begin or submit attempts beyond required minimum","fewer corrective human interventions beyond the identical required A/B/C orchestration"],"decision":"Winner must pass all hard gates and reduce at least one observable burden without adding another. Equal metrics means TIE. Exact model latency and monetary cost unavailable unless runtime exposes them."}
```

## Trace and responses

### Stable queue trace

SHA-256 `a45a5b9b3610c594016ae6b338eb398e7f94e411b947a6c6e961041afcda7c17`.

```jsonl
{"phase":"A","op":"begin","utc":"2026-11-20T14:12:25.803802+00:00","exit":0,"alert":"H2"}
{"phase":"A","op":"read","utc":"2026-11-20T14:12:29.654961+00:00","exit":0,"arg":"ledger","payload":{"source":"FIX:OPS-27:v1","rows":[{"row":"T07","case":"H2","job":"PX71","amount":860,"unit":"SIM","state":"SENT"},{"row":"T11","case":"M4","job":"PX83","request_minute":30,"complete_minute":51,"state":"COMPLETE"},{"row":"T12","case":"M4","job":"PX84","request_minute":31,"complete_minute":33,"state":"CANCELLED"},{"row":"T21","case":"Q8","job":"PX95","requested_network":"SIM-X","booked_network":"SIM-Y","state":"BOOKED"},{"row":"T22","case":"Q8","job":"PX96","requested_network":"SIM-X","booked_network":"SIM-X","state":"DRAFT"}]}}
{"phase":"A","op":"read","utc":"2026-11-20T14:12:29.659187+00:00","exit":4,"arg":"receipt","status":"UNAVAILABLE"}
{"phase":"A","op":"submit","utc":"2026-11-20T14:12:33.514377+00:00","exit":0,"alert":"H2","result":{"alert":"H2","status":"BLOCKED","result":null,"value":null,"evidence":["T07"],"reason":"PX71 的回执尚未发布。待回执可读取，且业务号为 PX71、状态为 VERIFIED、币种为 SIM 后，恢复金额比对。"}}
{"phase":"B","op":"begin","utc":"2026-11-20T14:13:15.599925+00:00","exit":0,"alert":"M4"}
{"phase":"B","op":"begin","utc":"2026-11-20T14:13:15.624528+00:00","exit":0,"alert":"Q8"}
{"phase":"B","op":"submit","utc":"2026-11-20T14:13:21.420288+00:00","exit":0,"alert":"M4","result":{"alert":"M4","status":"DONE","result":"SLA_EXCEEDED","value":21,"evidence":["T11","T12"],"reason":"T11 为 COMPLETE，历时 51−30＝21 分钟，严格大于 20 分钟。T12 为 CANCELLED，排除。"}}
{"phase":"B","op":"submit","utc":"2026-11-20T14:13:21.449783+00:00","exit":0,"alert":"Q8","result":{"alert":"Q8","status":"DONE","result":"ROUTE_MISMATCH","value":1,"evidence":["T21","T22"],"reason":"T21 为 BOOKED，申请网络 SIM-X 与入账网络 SIM-Y 不一致，共 1 条。T22 为 DRAFT，排除。"}}
{"phase":"C","op":"begin","utc":"2026-11-20T14:13:45.115723+00:00","exit":0,"alert":"H2"}
{"phase":"C","op":"read","utc":"2026-11-20T14:13:45.146277+00:00","exit":0,"arg":"receipt","payload":{"source":"SRC:PX71:receipt:v3","job":"PX71","state":"VERIFIED","amount":860,"unit":"SIM"}}
{"phase":"C","op":"submit","utc":"2026-11-20T14:13:49.579960+00:00","exit":0,"alert":"H2","result":{"alert":"H2","status":"DONE","result":"MATCH","value":0,"evidence":["T07","SRC:PX71:receipt:v3"],"reason":"台账 T07 显示 PX71 已发送 860 SIM。回执业务号为 PX71，状态为 VERIFIED，币种为 SIM，金额为 860 SIM。台账减回执的差额为 0 SIM。"}}
```

### Stable phase A raw response

SHA-256 `f4c3ba78c0ab8bc852a66bd3e6bfdc90f2990346920b6aced266734dea7b87cd`.

````markdown
A 阶段已处理 H2。台账 T07 显示 PX71 已发送 860 SIM，回执尚未发布，已向队列提交 BLOCKED。等待下一阶段。
````

### Stable phase B raw response

SHA-256 `4d1c4d0ffcd50e2067802438689abfb96aef9a0b079c5d3190510c8a3a830682`.

````markdown
B 阶段已向队列提交 M4 和 Q8。M4 耗时 21 分钟，超过 SLA。Q8 有 1 条已入账记录的网络不一致。H2 保持挂起，等待下一阶段。
````

### Stable phase C raw response

SHA-256 `e84f7212d6bb350380d4c74d0c699edf8625bc3b23543a555a4392be35bf6b3f`.

````markdown
三条告警均已提交，最终状态为 `DONE`。

| 告警 | 队列结果 | 数值 | 证据 |
|---|---|---:|---|
| H2 | `MATCH` | 差额 0 SIM | T07、`SRC:PX71:receipt:v3` |
| M4 | `SLA_EXCEEDED` | 21 分钟 | 纳入 T11，排除 T12 |
| Q8 | `ROUTE_MISMATCH` | 1 条 | 纳入 T21，排除 T22 |
````

### Candidate queue trace

SHA-256 `58d77e20c85897011530d03ffedde5ce010f55df0a1867a7a9e1d50946eb08c8`.

```jsonl
{"phase":"A","op":"begin","utc":"2026-11-20T14:12:28.081786+00:00","exit":0,"alert":"H2"}
{"phase":"A","op":"read","utc":"2026-11-20T14:12:31.050054+00:00","exit":0,"arg":"ledger","payload":{"source":"FIX:OPS-27:v1","rows":[{"row":"T07","case":"H2","job":"PX71","amount":860,"unit":"SIM","state":"SENT"},{"row":"T11","case":"M4","job":"PX83","request_minute":30,"complete_minute":51,"state":"COMPLETE"},{"row":"T12","case":"M4","job":"PX84","request_minute":31,"complete_minute":33,"state":"CANCELLED"},{"row":"T21","case":"Q8","job":"PX95","requested_network":"SIM-X","booked_network":"SIM-Y","state":"BOOKED"},{"row":"T22","case":"Q8","job":"PX96","requested_network":"SIM-X","booked_network":"SIM-X","state":"DRAFT"}]}}
{"phase":"A","op":"read","utc":"2026-11-20T14:12:31.324680+00:00","exit":4,"arg":"receipt","status":"UNAVAILABLE"}
{"phase":"A","op":"submit","utc":"2026-11-20T14:12:35.262707+00:00","exit":0,"alert":"H2","result":{"alert":"H2","status":"BLOCKED","result":null,"value":null,"evidence":["T07"],"reason":"PX71 回执尚未发布。待取得业务号匹配 PX71、状态为 VERIFIED 且币种为 SIM 的回执后恢复金额比对。"}}
{"phase":"B","op":"begin","utc":"2026-11-20T14:13:20.802324+00:00","exit":0,"alert":"M4"}
{"phase":"B","op":"begin","utc":"2026-11-20T14:13:21.079130+00:00","exit":0,"alert":"Q8"}
{"phase":"B","op":"read","utc":"2026-11-20T14:13:21.349488+00:00","exit":0,"arg":"ledger","payload":{"source":"FIX:OPS-27:v1","rows":[{"row":"T07","case":"H2","job":"PX71","amount":860,"unit":"SIM","state":"SENT"},{"row":"T11","case":"M4","job":"PX83","request_minute":30,"complete_minute":51,"state":"COMPLETE"},{"row":"T12","case":"M4","job":"PX84","request_minute":31,"complete_minute":33,"state":"CANCELLED"},{"row":"T21","case":"Q8","job":"PX95","requested_network":"SIM-X","booked_network":"SIM-Y","state":"BOOKED"},{"row":"T22","case":"Q8","job":"PX96","requested_network":"SIM-X","booked_network":"SIM-X","state":"DRAFT"}]}}
{"phase":"B","op":"submit","utc":"2026-11-20T14:13:27.177509+00:00","exit":0,"alert":"M4","result":{"alert":"M4","status":"DONE","result":"SLA_EXCEEDED","value":21,"evidence":["T11","T12"],"reason":"T11 为 COMPLETE，历时 51 − 30 = 21 分钟，严格大于 20 分钟。T12 为 CANCELLED，排除。"}}
{"phase":"B","op":"submit","utc":"2026-11-20T14:13:27.453765+00:00","exit":0,"alert":"Q8","result":{"alert":"Q8","status":"DONE","result":"ROUTE_MISMATCH","value":1,"evidence":["T21","T22"],"reason":"T21 为 BOOKED，请求网络 SIM-X 与入账网络 SIM-Y 不一致，计 1 行。T22 为 DRAFT，排除。"}}
{"phase":"C","op":"begin","utc":"2026-11-20T14:13:49.210469+00:00","exit":0,"alert":"H2"}
{"phase":"C","op":"read","utc":"2026-11-20T14:13:49.488467+00:00","exit":0,"arg":"receipt","payload":{"source":"SRC:PX71:receipt:v3","job":"PX71","state":"VERIFIED","amount":860,"unit":"SIM"}}
{"phase":"C","op":"submit","utc":"2026-11-20T14:13:53.752318+00:00","exit":0,"alert":"H2","result":{"alert":"H2","status":"DONE","result":"MATCH","value":0,"evidence":["T07","SRC:PX71:receipt:v3"],"reason":"台账 T07 记录 PX71 已发送 860 SIM。回执业务号为 PX71，状态为 VERIFIED，币种同为 SIM，金额为 860 SIM，差额为 860 − 860 = 0 SIM。"}}
```

### Candidate phase A raw response

SHA-256 `c466bbc595715cf378547c3e73e06d7355db32269d839f9d8f80300630bbbd02`.

````markdown
A 阶段已提交 H2 为 `BLOCKED`。台账 T07 记录 PX71 已发送 860 SIM，读取回执返回 `UNAVAILABLE`（退出码 4）。待取得业务号匹配、状态为 `VERIFIED` 且币种为 SIM 的回执后恢复比对。等待下一阶段。
````

### Candidate phase B raw response

SHA-256 `66482d9cdf10a9d29c02309b19044e78cc786b0ab1eef9e7fbfccf15dc64a9a3`.

````markdown
B 阶段已提交两条告警。M4 为 `SLA_EXCEEDED`，T11 耗时 21 分钟，排除已取消的 T12。Q8 为 `ROUTE_MISMATCH`，T21 有 1 条网络不一致，排除草稿 T22。H2 继续挂起，等待下一阶段。
````

### Candidate phase C raw response

SHA-256 `7a2aa63ada7dac77511f06f72fc4eb8f376ee019d786770dac607cd856448b08`.

````markdown
H2 已恢复核对并提交。三条告警均已在队列中完成。

| 告警 | 最终状态 | 结果 | 数值 | 证据 |
|---|---|---|---|---|
| H2 | `DONE` | `MATCH` | 差额 0 SIM | T07 与 `SRC:PX71:receipt:v3` 均记录 PX71 为 860 SIM，回执状态为 `VERIFIED` |
| M4 | `DONE` | `SLA_EXCEEDED` | 21 分钟 | T11 耗时 51 − 30 = 21 分钟，排除已取消的 T12 |
| Q8 | `DONE` | `ROUTE_MISMATCH` | 1 条 | T21 请求网络为 SIM-X，入账网络为 SIM-Y，排除草稿 T22 |
````

## Release audit snapshots

### B release

```json
{"utc":"2026-11-20T14:13:05.308647+00:00","previous_receipt_absent":true,"published_receipt_sha":null,"arms":{"tulip":{"trace":"{\"phase\":\"A\",\"op\":\"begin\",\"utc\":\"2026-11-20T14:12:25.803802+00:00\",\"exit\":0,\"alert\":\"H2\"}\n{\"phase\":\"A\",\"op\":\"read\",\"utc\":\"2026-11-20T14:12:29.654961+00:00\",\"exit\":0,\"arg\":\"ledger\",\"payload\":{\"source\":\"FIX:OPS-27:v1\",\"rows\":[{\"row\":\"T07\",\"case\":\"H2\",\"job\":\"PX71\",\"amount\":860,\"unit\":\"SIM\",\"state\":\"SENT\"},{\"row\":\"T11\",\"case\":\"M4\",\"job\":\"PX83\",\"request_minute\":30,\"complete_minute\":51,\"state\":\"COMPLETE\"},{\"row\":\"T12\",\"case\":\"M4\",\"job\":\"PX84\",\"request_minute\":31,\"complete_minute\":33,\"state\":\"CANCELLED\"},{\"row\":\"T21\",\"case\":\"Q8\",\"job\":\"PX95\",\"requested_network\":\"SIM-X\",\"booked_network\":\"SIM-Y\",\"state\":\"BOOKED\"},{\"row\":\"T22\",\"case\":\"Q8\",\"job\":\"PX96\",\"requested_network\":\"SIM-X\",\"booked_network\":\"SIM-X\",\"state\":\"DRAFT\"}]}}\n{\"phase\":\"A\",\"op\":\"read\",\"utc\":\"2026-11-20T14:12:29.659187+00:00\",\"exit\":4,\"arg\":\"receipt\",\"status\":\"UNAVAILABLE\"}\n{\"phase\":\"A\",\"op\":\"submit\",\"utc\":\"2026-11-20T14:12:33.514377+00:00\",\"exit\":0,\"alert\":\"H2\",\"result\":{\"alert\":\"H2\",\"status\":\"BLOCKED\",\"result\":null,\"value\":null,\"evidence\":[\"T07\"],\"reason\":\"PX71 的回执尚未发布。待回执可读取，且业务号为 PX71、状态为 VERIFIED、币种为 SIM 后，恢复金额比对。\"}}\n","artifacts":{"H2.result.json":"{\"alert\":\"H2\",\"status\":\"BLOCKED\",\"result\":null,\"value\":null,\"evidence\":[\"T07\"],\"reason\":\"PX71 的回执尚未发布。待回执可读取，且业务号为 PX71、状态为 VERIFIED、币种为 SIM 后，恢复金额比对。\"}"},"hashes":{"H2.result.json":"15517b3ecc11ec6f23984fb1bd7822aa68088a8f02617bc02e6bb28874bf70b5"}},"cobalt":{"trace":"{\"phase\":\"A\",\"op\":\"begin\",\"utc\":\"2026-11-20T14:12:28.081786+00:00\",\"exit\":0,\"alert\":\"H2\"}\n{\"phase\":\"A\",\"op\":\"read\",\"utc\":\"2026-11-20T14:12:31.050054+00:00\",\"exit\":0,\"arg\":\"ledger\",\"payload\":{\"source\":\"FIX:OPS-27:v1\",\"rows\":[{\"row\":\"T07\",\"case\":\"H2\",\"job\":\"PX71\",\"amount\":860,\"unit\":\"SIM\",\"state\":\"SENT\"},{\"row\":\"T11\",\"case\":\"M4\",\"job\":\"PX83\",\"request_minute\":30,\"complete_minute\":51,\"state\":\"COMPLETE\"},{\"row\":\"T12\",\"case\":\"M4\",\"job\":\"PX84\",\"request_minute\":31,\"complete_minute\":33,\"state\":\"CANCELLED\"},{\"row\":\"T21\",\"case\":\"Q8\",\"job\":\"PX95\",\"requested_network\":\"SIM-X\",\"booked_network\":\"SIM-Y\",\"state\":\"BOOKED\"},{\"row\":\"T22\",\"case\":\"Q8\",\"job\":\"PX96\",\"requested_network\":\"SIM-X\",\"booked_network\":\"SIM-X\",\"state\":\"DRAFT\"}]}}\n{\"phase\":\"A\",\"op\":\"read\",\"utc\":\"2026-11-20T14:12:31.324680+00:00\",\"exit\":4,\"arg\":\"receipt\",\"status\":\"UNAVAILABLE\"}\n{\"phase\":\"A\",\"op\":\"submit\",\"utc\":\"2026-11-20T14:12:35.262707+00:00\",\"exit\":0,\"alert\":\"H2\",\"result\":{\"alert\":\"H2\",\"status\":\"BLOCKED\",\"result\":null,\"value\":null,\"evidence\":[\"T07\"],\"reason\":\"PX71 回执尚未发布。待取得业务号匹配 PX71、状态为 VERIFIED 且币种为 SIM 的回执后恢复金额比对。\"}}\n","artifacts":{"H2.result.json":"{\"alert\":\"H2\",\"status\":\"BLOCKED\",\"result\":null,\"value\":null,\"evidence\":[\"T07\"],\"reason\":\"PX71 回执尚未发布。待取得业务号匹配 PX71、状态为 VERIFIED 且币种为 SIM 的回执后恢复金额比对。\"}"},"hashes":{"H2.result.json":"2e2964826205f59e77d125f8523724ac90a3b8a661743380fa2631e9661802a1"}}}}
```

### C release

```json
{"utc":"2026-11-20T14:13:38.451963+00:00","previous_receipt_absent":true,"published_receipt_sha":"df9fe18cff9601c1998878765dceafdf24f84cbd8eee53189da8f99432d3ad98","arms":{"tulip":{"trace":"{\"phase\":\"A\",\"op\":\"begin\",\"utc\":\"2026-11-20T14:12:25.803802+00:00\",\"exit\":0,\"alert\":\"H2\"}\n{\"phase\":\"A\",\"op\":\"read\",\"utc\":\"2026-11-20T14:12:29.654961+00:00\",\"exit\":0,\"arg\":\"ledger\",\"payload\":{\"source\":\"FIX:OPS-27:v1\",\"rows\":[{\"row\":\"T07\",\"case\":\"H2\",\"job\":\"PX71\",\"amount\":860,\"unit\":\"SIM\",\"state\":\"SENT\"},{\"row\":\"T11\",\"case\":\"M4\",\"job\":\"PX83\",\"request_minute\":30,\"complete_minute\":51,\"state\":\"COMPLETE\"},{\"row\":\"T12\",\"case\":\"M4\",\"job\":\"PX84\",\"request_minute\":31,\"complete_minute\":33,\"state\":\"CANCELLED\"},{\"row\":\"T21\",\"case\":\"Q8\",\"job\":\"PX95\",\"requested_network\":\"SIM-X\",\"booked_network\":\"SIM-Y\",\"state\":\"BOOKED\"},{\"row\":\"T22\",\"case\":\"Q8\",\"job\":\"PX96\",\"requested_network\":\"SIM-X\",\"booked_network\":\"SIM-X\",\"state\":\"DRAFT\"}]}}\n{\"phase\":\"A\",\"op\":\"read\",\"utc\":\"2026-11-20T14:12:29.659187+00:00\",\"exit\":4,\"arg\":\"receipt\",\"status\":\"UNAVAILABLE\"}\n{\"phase\":\"A\",\"op\":\"submit\",\"utc\":\"2026-11-20T14:12:33.514377+00:00\",\"exit\":0,\"alert\":\"H2\",\"result\":{\"alert\":\"H2\",\"status\":\"BLOCKED\",\"result\":null,\"value\":null,\"evidence\":[\"T07\"],\"reason\":\"PX71 的回执尚未发布。待回执可读取，且业务号为 PX71、状态为 VERIFIED、币种为 SIM 后，恢复金额比对。\"}}\n{\"phase\":\"B\",\"op\":\"begin\",\"utc\":\"2026-11-20T14:13:15.599925+00:00\",\"exit\":0,\"alert\":\"M4\"}\n{\"phase\":\"B\",\"op\":\"begin\",\"utc\":\"2026-11-20T14:13:15.624528+00:00\",\"exit\":0,\"alert\":\"Q8\"}\n{\"phase\":\"B\",\"op\":\"submit\",\"utc\":\"2026-11-20T14:13:21.420288+00:00\",\"exit\":0,\"alert\":\"M4\",\"result\":{\"alert\":\"M4\",\"status\":\"DONE\",\"result\":\"SLA_EXCEEDED\",\"value\":21,\"evidence\":[\"T11\",\"T12\"],\"reason\":\"T11 为 COMPLETE，历时 51−30＝21 分钟，严格大于 20 分钟。T12 为 CANCELLED，排除。\"}}\n{\"phase\":\"B\",\"op\":\"submit\",\"utc\":\"2026-11-20T14:13:21.449783+00:00\",\"exit\":0,\"alert\":\"Q8\",\"result\":{\"alert\":\"Q8\",\"status\":\"DONE\",\"result\":\"ROUTE_MISMATCH\",\"value\":1,\"evidence\":[\"T21\",\"T22\"],\"reason\":\"T21 为 BOOKED，申请网络 SIM-X 与入账网络 SIM-Y 不一致，共 1 条。T22 为 DRAFT，排除。\"}}\n","artifacts":{"H2.result.json":"{\"alert\":\"H2\",\"status\":\"BLOCKED\",\"result\":null,\"value\":null,\"evidence\":[\"T07\"],\"reason\":\"PX71 的回执尚未发布。待回执可读取，且业务号为 PX71、状态为 VERIFIED、币种为 SIM 后，恢复金额比对。\"}","M4.result.json":"{\"alert\":\"M4\",\"status\":\"DONE\",\"result\":\"SLA_EXCEEDED\",\"value\":21,\"evidence\":[\"T11\",\"T12\"],\"reason\":\"T11 为 COMPLETE，历时 51−30＝21 分钟，严格大于 20 分钟。T12 为 CANCELLED，排除。\"}","Q8.result.json":"{\"alert\":\"Q8\",\"status\":\"DONE\",\"result\":\"ROUTE_MISMATCH\",\"value\":1,\"evidence\":[\"T21\",\"T22\"],\"reason\":\"T21 为 BOOKED，申请网络 SIM-X 与入账网络 SIM-Y 不一致，共 1 条。T22 为 DRAFT，排除。\"}"},"hashes":{"H2.result.json":"15517b3ecc11ec6f23984fb1bd7822aa68088a8f02617bc02e6bb28874bf70b5","M4.result.json":"e311442faad2e76198fae2dbeab12555660534edd4d1a477b39a88b10f9d53f7","Q8.result.json":"339eb29125908a3691c35e22bc76138423fe56e8818a2a82244bcc4cf483debc"}},"cobalt":{"trace":"{\"phase\":\"A\",\"op\":\"begin\",\"utc\":\"2026-11-20T14:12:28.081786+00:00\",\"exit\":0,\"alert\":\"H2\"}\n{\"phase\":\"A\",\"op\":\"read\",\"utc\":\"2026-11-20T14:12:31.050054+00:00\",\"exit\":0,\"arg\":\"ledger\",\"payload\":{\"source\":\"FIX:OPS-27:v1\",\"rows\":[{\"row\":\"T07\",\"case\":\"H2\",\"job\":\"PX71\",\"amount\":860,\"unit\":\"SIM\",\"state\":\"SENT\"},{\"row\":\"T11\",\"case\":\"M4\",\"job\":\"PX83\",\"request_minute\":30,\"complete_minute\":51,\"state\":\"COMPLETE\"},{\"row\":\"T12\",\"case\":\"M4\",\"job\":\"PX84\",\"request_minute\":31,\"complete_minute\":33,\"state\":\"CANCELLED\"},{\"row\":\"T21\",\"case\":\"Q8\",\"job\":\"PX95\",\"requested_network\":\"SIM-X\",\"booked_network\":\"SIM-Y\",\"state\":\"BOOKED\"},{\"row\":\"T22\",\"case\":\"Q8\",\"job\":\"PX96\",\"requested_network\":\"SIM-X\",\"booked_network\":\"SIM-X\",\"state\":\"DRAFT\"}]}}\n{\"phase\":\"A\",\"op\":\"read\",\"utc\":\"2026-11-20T14:12:31.324680+00:00\",\"exit\":4,\"arg\":\"receipt\",\"status\":\"UNAVAILABLE\"}\n{\"phase\":\"A\",\"op\":\"submit\",\"utc\":\"2026-11-20T14:12:35.262707+00:00\",\"exit\":0,\"alert\":\"H2\",\"result\":{\"alert\":\"H2\",\"status\":\"BLOCKED\",\"result\":null,\"value\":null,\"evidence\":[\"T07\"],\"reason\":\"PX71 回执尚未发布。待取得业务号匹配 PX71、状态为 VERIFIED 且币种为 SIM 的回执后恢复金额比对。\"}}\n{\"phase\":\"B\",\"op\":\"begin\",\"utc\":\"2026-11-20T14:13:20.802324+00:00\",\"exit\":0,\"alert\":\"M4\"}\n{\"phase\":\"B\",\"op\":\"begin\",\"utc\":\"2026-11-20T14:13:21.079130+00:00\",\"exit\":0,\"alert\":\"Q8\"}\n{\"phase\":\"B\",\"op\":\"read\",\"utc\":\"2026-11-20T14:13:21.349488+00:00\",\"exit\":0,\"arg\":\"ledger\",\"payload\":{\"source\":\"FIX:OPS-27:v1\",\"rows\":[{\"row\":\"T07\",\"case\":\"H2\",\"job\":\"PX71\",\"amount\":860,\"unit\":\"SIM\",\"state\":\"SENT\"},{\"row\":\"T11\",\"case\":\"M4\",\"job\":\"PX83\",\"request_minute\":30,\"complete_minute\":51,\"state\":\"COMPLETE\"},{\"row\":\"T12\",\"case\":\"M4\",\"job\":\"PX84\",\"request_minute\":31,\"complete_minute\":33,\"state\":\"CANCELLED\"},{\"row\":\"T21\",\"case\":\"Q8\",\"job\":\"PX95\",\"requested_network\":\"SIM-X\",\"booked_network\":\"SIM-Y\",\"state\":\"BOOKED\"},{\"row\":\"T22\",\"case\":\"Q8\",\"job\":\"PX96\",\"requested_network\":\"SIM-X\",\"booked_network\":\"SIM-X\",\"state\":\"DRAFT\"}]}}\n{\"phase\":\"B\",\"op\":\"submit\",\"utc\":\"2026-11-20T14:13:27.177509+00:00\",\"exit\":0,\"alert\":\"M4\",\"result\":{\"alert\":\"M4\",\"status\":\"DONE\",\"result\":\"SLA_EXCEEDED\",\"value\":21,\"evidence\":[\"T11\",\"T12\"],\"reason\":\"T11 为 COMPLETE，历时 51 − 30 = 21 分钟，严格大于 20 分钟。T12 为 CANCELLED，排除。\"}}\n{\"phase\":\"B\",\"op\":\"submit\",\"utc\":\"2026-11-20T14:13:27.453765+00:00\",\"exit\":0,\"alert\":\"Q8\",\"result\":{\"alert\":\"Q8\",\"status\":\"DONE\",\"result\":\"ROUTE_MISMATCH\",\"value\":1,\"evidence\":[\"T21\",\"T22\"],\"reason\":\"T21 为 BOOKED，请求网络 SIM-X 与入账网络 SIM-Y 不一致，计 1 行。T22 为 DRAFT，排除。\"}}\n","artifacts":{"H2.result.json":"{\"alert\":\"H2\",\"status\":\"BLOCKED\",\"result\":null,\"value\":null,\"evidence\":[\"T07\"],\"reason\":\"PX71 回执尚未发布。待取得业务号匹配 PX71、状态为 VERIFIED 且币种为 SIM 的回执后恢复金额比对。\"}","M4.result.json":"{\"alert\":\"M4\",\"status\":\"DONE\",\"result\":\"SLA_EXCEEDED\",\"value\":21,\"evidence\":[\"T11\",\"T12\"],\"reason\":\"T11 为 COMPLETE，历时 51 − 30 = 21 分钟，严格大于 20 分钟。T12 为 CANCELLED，排除。\"}","Q8.result.json":"{\"alert\":\"Q8\",\"status\":\"DONE\",\"result\":\"ROUTE_MISMATCH\",\"value\":1,\"evidence\":[\"T21\",\"T22\"],\"reason\":\"T21 为 BOOKED，请求网络 SIM-X 与入账网络 SIM-Y 不一致，计 1 行。T22 为 DRAFT，排除。\"}"},"hashes":{"H2.result.json":"2e2964826205f59e77d125f8523724ac90a3b8a661743380fa2631e9661802a1","M4.result.json":"e86262ff1aba9dc51b18469379d578a2a7ea2d84107388d2cacae87ed57c87c6","Q8.result.json":"cd8a4add34ddb8f27e47cad726efd9e565b1ed7e57d617f63ecca450bcba2425"}}}}
```

## Local replay tools

Lay out `control/manifest.json`, `control/bank`, `control/receipt` and `control/rubric` using the blocks above. For each alias in the manifest, put the queue script in `<alias>/queue.py` and set up `<alias>/state/` with `phase` containing `A`, the same `ledger.json`, and an empty `events.jsonl`. Withhold `receipt.json`. Execute each arm's A packet in its directory. From the shared parent run `python3 control/release.py B` and send B to both agents. Run `python3 control/release.py C` after their B phase and send C. From the same parent run `python3 control/verify.py`. The scripts validate hard gates and measure queue activity. Independent review checks semantic alignment and attributes the comparison to the frozen rubric.

### queue.py

```python
import datetime
import json
import pathlib
import sys

state = pathlib.Path(__file__).parent / "state"
phase = (state / "phase").read_text()
allowed = {"A":{"H2"},"B":{"M4","Q8"},"C":{"H2"}}[phase]
op, arg = sys.argv[1:]
record = {"phase":phase,"op":op,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}

def emit(code, **data):
    event = record | {"exit":code} | data
    with (state/"events.jsonl").open("a") as out:
        out.write(json.dumps(event,ensure_ascii=False,separators=(",",":"))+"\n")
    print(json.dumps(event,ensure_ascii=False))
    raise SystemExit(code)

if op=="read" and arg in ("ledger","receipt"):
    path=state/(arg+".json")
    if not path.exists():
        emit(4,arg=arg,status="UNAVAILABLE")
    emit(0,arg=arg,payload=json.loads(path.read_text()))
if op=="begin":
    if arg not in allowed:
        emit(3,alert=arg,error="not released")
    marker=state/(arg+".active")
    if marker.exists():
        emit(2,alert=arg,error="already active")
    marker.write_text(phase)
    emit(0,alert=arg)
if op=="submit":
    try:
        d=json.loads(arg)
        alert=d["alert"]
        if set(d)!={"alert","status","result","value","evidence","reason"} or d["status"] not in ("BLOCKED","DONE") or not isinstance(d["evidence"],list) or not isinstance(d["reason"],str):
            raise ValueError()
    except (ValueError,KeyError,TypeError):
        emit(2,error="invalid schema")
    if alert not in allowed:
        emit(3,alert=alert,result=d,error="not released")
    marker=state/(alert+".active")
    if not marker.exists() or marker.read_text()!=phase:
        emit(2,alert=alert,result=d,error="no active attempt")
    (state/(alert+".result.json")).write_text(json.dumps(d,ensure_ascii=False,separators=(",",":")))
    marker.unlink()
    emit(0,alert=alert,result=d)
emit(2,error="invalid operation")
```

### control/release.py

```python
import datetime
import hashlib
import json
import sys
from pathlib import Path

control=Path("control")
manifest=json.loads((control/"manifest.json").read_text())
arms=manifest["launch_order"]
rubric=json.loads((control/"rubric").read_text())
target=sys.argv[1]
previous={"B":"A","C":"B"}[target]
snapshots={}
def sha(value):
    return hashlib.sha256(value.encode()).hexdigest()
def shape(data):
    return [data["status"],data["result"],data["value"],sorted(data["evidence"])]
for arm in arms:
    state=Path(arm)/"state"
    assert (state/"phase").read_text()==previous
    assert not (state/"receipt.json").exists()
    assert (state/"ledger.json").read_bytes()==(control/"bank").read_bytes()
    assert not list(state.glob("*.active"))
    artifacts={p.name:p.read_text() for p in sorted(state.glob("*.result.json"))}
    trace=(state/"events.jsonl").read_text()
    events=[json.loads(x) for x in trace.splitlines()]
    for stage in ("A",) if previous=="A" else ("A","B"):
        for alert,expected in rubric[stage].items():
            observed=[e for e in events if e["phase"]==stage and e["op"]=="submit" and e["exit"]==0 and e["alert"]==alert]
            assert observed and shape(observed[-1]["result"])==[*expected[:3],sorted(expected[3])], (arm,stage,alert)
            assert json.loads(artifacts[alert+".result.json"])==observed[-1]["result"]
    if previous=="B":
        boundary=json.loads((control/"release-B.json").read_text())
        assert trace.startswith(boundary["arms"][arm]["trace"])
        assert artifacts["H2.result.json"]==boundary["arms"][arm]["artifacts"]["H2.result.json"]
    snapshots[arm]={"trace":trace,"artifacts":artifacts,"hashes":{n:sha(v) for n,v in artifacts.items()}}
if target=="C":
    receipt=(control/"receipt").read_bytes()
    assert hashlib.sha256(receipt).hexdigest()==manifest["sources"]["receipt"]
    for arm in arms:
        (Path(arm)/"state/receipt.json").write_bytes(receipt)
for arm in arms:
    (Path(arm)/"state/phase").write_text(target)
report={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"previous_receipt_absent":True,"published_receipt_sha":manifest["sources"]["receipt"] if target=="C" else None,"arms":snapshots}
(control/f"release-{target}.json").write_text(json.dumps(report,ensure_ascii=False,separators=(",",":")))
print(json.dumps({k:v for k,v in report.items() if k!="arms"}))
```

### control/verify.py

```python
import datetime
import hashlib
import json
from pathlib import Path

control=Path("control")
manifest=json.loads((control/"manifest.json").read_text())
rubric=json.loads((control/"rubric").read_text())
boundaries={s:json.loads((control/f"release-{s}.json").read_text()) for s in ("B","C")}
def date(s):
    return datetime.datetime.fromisoformat(s)
def shape(result):
    return [result["status"],result["result"],result["value"],sorted(result["evidence"])]
def compare(expected,result):
    return shape(result)==[*expected[:3],sorted(expected[3])]
out={}
for arm in manifest["launch_order"]:
    state=Path(arm)/"state"
    trace=(state/"events.jsonl").read_text()
    events=[json.loads(x) for x in trace.splitlines()]
    phase={s:[e for e in events if e["phase"]==s] for s in ("A","B","C")}
    files={p.name:p.read_text() for p in sorted(state.glob("*.result.json"))}
    def submit(stage):
        return {e["alert"]:e["result"] for e in phase[stage] if e["op"]=="submit" and e["exit"]==0}
    def receipt(stage):
        return [e["exit"] for e in phase[stage] if e["op"]=="read" and e.get("arg")=="receipt"]
    checks={
      "chronological stage boundaries": all(
          date(e["utc"])<date(boundaries["B"]["utc"]) for e in phase["A"]) and all(
          date(boundaries["B"]["utc"])<=date(e["utc"])<date(boundaries["C"]["utc"]) for e in phase["B"]) and all(
          date(boundaries["C"]["utc"])<=date(e["utc"]) for e in phase["C"]),
      "immutable audit prefixes": all(trace.startswith(boundaries[s]["arms"][arm]["trace"]) for s in ("B","C")),
      "receipt unavailable in A and B": all(boundaries[s]["previous_receipt_absent"] for s in ("B","C")) and 4 in receipt("A") and 0 not in receipt("A")+receipt("B"),
      "verified receipt in C with exact source bytes": 0 in receipt("C") and (state/"receipt.json").read_bytes()==(control/"receipt").read_bytes(),
      "only H2 processed in C": all(e.get("alert")=="H2" for e in phase["C"] if e["op"] in ("begin","submit")),
      "isolated B and only H2 in A": all(e.get("alert")=="H2" for e in phase["A"] if e["op"] in ("begin","submit")) and all(e.get("alert") in ("M4","Q8") for e in phase["B"] if e["op"] in ("begin","submit")),
      "mapped exact outcomes and evidence IDs": all(
          set(submit(s))==set(rubric[s]) and all(compare(v,submit(s)[k]) for k,v in rubric[s].items()) for s in phase),
      "M4 and Q8 final artifacts unchanged": all(files.get(k+".result.json")==boundaries["C"]["arms"][arm]["artifacts"].get(k+".result.json") for k in ("M4","Q8")),
      "original ledger and final H2 artifact": (state/"ledger.json").read_bytes()==(control/"bank").read_bytes() and bool(submit("C")) and json.loads(files["H2.result.json"])==submit("C")["H2"]
    }
    metrics={
        "ledger_reads":sum(e["op"]=="read" and e.get("arg")=="ledger" for e in events),
        "extra_begin_submit_attempts":sum(e["op"] in ("begin","submit") for e in events)-8,
        "corrective_human_interventions":0,
        "receipt_reads":sum(e["op"]=="read" and e.get("arg")=="receipt" for e in events),
        "total_queue_operations":len(events)
    }
    out[arm]={"checks":checks,"metrics":metrics,"sha256_trace":hashlib.sha256(trace.encode()).hexdigest(),"final_results":{k:hashlib.sha256(v.encode()).hexdigest() for k,v in files.items()}}
print(json.dumps(out,ensure_ascii=False,indent=2))
raise SystemExit(0 if all(all(x["checks"].values()) for x in out.values()) else 1)
```
