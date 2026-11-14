# PR #6 follow-up — gate repair and frozen A/B package

**结论：门禁修复已验证；模型 A/B、独立模型评审仍为 NOT_VERIFIED，禁止据此升级。**

仅修改实验分支中的门禁、测试、说明和证据。正式版、Candidate 提示正文及 Registry 未变，不合并 PR。

## 冻结身份

- 证据父提交：`25da4c6a29b8a0cd8f0cd10989b598fc944fae17`。
- Stable Blob：`188953441f5c54fdb81c7883ad05aa0e15a277fa`。
- Candidate Blob：`e87076047facb3a88ad95a6322f06a4cd478b0cc`。
- 新任务和逐项验收：`run-01/tasks.json`；输入、Prompt、SHA-256：`run-01/freeze.json` 及四份 `.input.txt`。

## 修复及复核

原门禁只查整套哈希及案例 ID；复制开发集后改名、换序，就能获得内存升级许可。

修复后对 `input + route + effective steps` 计算排序键、固定 JSON 分隔符的 SHA-256。忽略 ID、领域等描述字段，也不允许通过改答案或预算把相同输入当成新题；并拒绝 held-out 内部相同输入。默认 direct/steps 与显式默认写法一致。只做结构性排重，不把它称为语义新颖性证明。

| 检查 | 修复前 | 修复后 |
|---|---|---|
| 开发题改名、换序 | 内存错误放行 | 拒绝 |
| 全量回归 | 46 项原有测试 | 51/51 通过 |
| 新增防绕过测试 | 无 | 5 项通过 |
| Registry 库存 | 原有覆盖 | 14/14 通过 |
| 正式 Prompt、Registry | 原值 | 字节不变 |

五项新增测试覆盖：改名/换序/领域标签、部分重叠且改答案/预算、输入对象键换序、显式默认工作流、held-out 内部重复。既有合法独立输入的升级及回滚测试仍通过。所有 synthetic reviewer 都只是内存测试夹具，不是真实人工批准，不调用生产写入。

外部代码复跑已完成：GitHub Actions run `43566071711` / job `132360096609` 在提交 `937f3be2f3638eb7096d788fdf32ac54652b9d95`、CPython 3.12.16 上成功，51/51 通过，库存审计及反馈发现步骤均成功。原始单测日志片段和步骤状态保存在 `ci/`。这是另一个托管运行器的代码复核，不是独立模型质量评审。[查看 CI](https://github.com/lovemoganna/AgentComponent/actions/runs/43566071711)。

修复前从父提交提取到新目录，修复后执行当前实验代码；原始 stdout/stderr、命令、返回码保存在 `run-01/`，差异在 `patch.diff`。这些是代码验证，不能计入 Prompt A/B 胜率。

## 新任务与重叠检查

替换 PR 已公开的 CSV/NIST 例题，准备两个自包含合成任务：

1. 技术：半开时间窗口的区间覆盖合并、非法记录拒绝、不可变输入及边界处理。
2. 非技术：根据有选择偏差的虚构试点记录，写不超过 220 字的上线建议，区分因果证据和表面变化。

扫描父提交全部受跟踪文件，未发现三个特征标记；结果保存在 `overlap-screen.json`。这只排除了限定标记的精确重叠；作者知道任务，未由独立评审封存，完整开发集及语义排重仍为 NOT_VERIFIED，因此任务分类是 **EXPLORATORY_NOT_BLIND_HELDOUT**。不能用这两题声称盲测泛化优势。

四份 A/B 输入在调用前固定，同一任务字节一致；固定随机种子生成顺序，实际没有完成模型运行。精确模型版本、系统指令、采样条件、原始输出、成本及独立评审均无可核对记录。

## 模型执行阻塞

预检尝试启动 CLI 新会话，原始错误为 `failed to initialize in-process app-server client: Read-only file system (os error 30)`。没有取得 READY 或真实任务答案。

随后工具自动审批拒绝了四份任务的模型运行：仓库提示词与测试输入将发送至 `ab.chatgpt.com`，该目标未得到用户明确授权。没有绕过拒绝，没有改用另一条路径提交相同负载。`approval-block.json` 记录拒绝边界，`model-ledger.json` 中四份结果均为 NOT_VERIFIED，raw_output=null，NOT_RUN。运行文件的默认模式只执行本地控制，不发送模型输入；`--attempt-model` 必须在明确授权后才可使用。

独立模型/人工质量评审也未完成。代码 CI 即使通过，也只证明回归，不代表提示质量或人工批准。

## 可复现及决策

```sh
python3 systems/metaloop/evidence/pr6-followup-20261114/run.py --out /tmp/pr6-followup-replay
```

默认不调用模型；复现内容为冻结输入、代码修复前后对照、回归、库存审计及阻塞台账。使用 Python 3.12；时间戳与耗时可变，状态应一致。`SHA256SUMS.json` 和根目录 `MANIFEST.json` 供证据字节校验。

保留门禁修复；保留旧正式版；Candidate 不晋升；PR #6 不合并。剩余依赖为指定模型目标授权及可启动的隔离运行时，之后才可获得四份模型原始产物并进行独立核验。不得把本报告称为已经完成的模型 A/B。
