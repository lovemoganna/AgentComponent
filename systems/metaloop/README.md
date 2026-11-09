# MetaLoop MVP

这是**最小可运行原型**，不是自主改写提示仓库的无限循环。自然语言入口见 [MetaLoop Prompt](../../prompts/meta-prompt/execute/orchestrate-metaloop.md)。

## 已提供
- Task Contract：operation / input / expected / route / steps / repair_candidates / max_calls / max_repairs，明确输入、交付和可复核的期望值。
- Prompt Registry：registry.json 记录旧 Prompt stable 和 MetaLoop candidate 的唯一位置与版本；文本质量升级仍须单独评审。
- Context Boundary：只把输入作为数据传给白名单纯函数；不会执行外部材料中的指令。
- Workflow Router：direct 单步、sequence 有依赖链、parallel 逻辑扇出（**本 MVP 顺序计算，不宣称并发加速**）。
- Evaluation / Repair：确定性比对，最多两轮显式修复，工具调用预算与轨迹可见。
- Experience / Version：候选相对稳定版的逐例对照、升级日志、回滚；--journal 可持久保存 JSONL 执行记录。
- Regression：冻结的 6 个案例，含非技术文本、技术数值、JSON；CI 每次相关 PR 和 push 自动运行。

## 运行命令
在仓库根目录执行：

    python -m unittest discover -s systems/metaloop/tests -v
    python systems/metaloop/engine.py compare
    python systems/metaloop/engine.py promote
    python systems/metaloop/engine.py promote --write  # 拒绝：缺少独立复核和人工批准
    python systems/metaloop/engine.py promote --review approval.json --write  # 仅在完成外部审核后
    python systems/metaloop/engine.py rollback --write
    python systems/metaloop/engine.py run --task my-task.json --journal runlog.jsonl

示例任务 JSON：

    {"id":"price-drop","operation":"percentage_drop","input":{"high":28.46,"low":25.60},"expected":10.0492}

工具适配器（纯函数）：normalize_ascii、normalize_unicode、dedupe_lines、percentage_drop、json_lookup。不得将此适配器集合描述为通用 LLM 的全部能力。

## 可观察结果与边界
6 个冻结测试中，baseline 5/6、candidate 6/6，差异来自非断行空格（NBSP）处理；工程级逐项结果可用 compare 复现。测试集与实现一起开发，因此**不是独立盲测、不能证明提示词或 Agent 效果变好**；registry 默认仍保留旧版为 stable，不自动升级正式 Prompt。

代码的 compare.promotable 只说明确定性示例满足“有提升且无回归”的局部条件，**不等于准许升级**。无 --review 时，即使 --write 也必须拒绝升级。独立复核文件需包含 `approved=true`、`reviewer_type=human`、非空 `reviewer_id`、`evidence_ref`，以及与开发集不重叠的 `heldout_suite.cases`（至少 3 例、2 个领域）。程序重新计算开发集和 held-out 的确定性结果，再决定能否提升文本适配器 stable，并记录复核引用和两个测试集的哈希；回滚使用 history。

**限制**：文件字段仅是人工批准的程序化凭据，脚本不能验证审核人真实身份、原始证据真实性，也不能证明真实 LLM 提示质量。任何人都可以伪造 JSON 字段，因此独立人工验收必须在脚本外核实，自动化任务不得自行生成批准记录。没有可核对的证据则 NOOP。

## 下一轮高价值改进
用真实但尚未参与开发的仓库 Prompt 任务建立跨域 held-out 集；保存模型、上下文与产物哈希，进行隔离 A/B。之后才决定是否增加真正并发、硬超时或外部工具适配器。不要因一轮失败修改所有 Prompt。

## 分层对抗性测试（第二轮）

新增 test_layer_evaluation.py 覆盖 L1 的直接/顺序/逻辑并行、预算和白名单；L2 的复杂工作流对照与退化；L3 的未复核升级拦截、无历史回滚和 NOOP。首轮基线执行发现两个问题：复杂流程对比依赖缺失 operation 而崩溃；内部 6 例通过即自动升级。两处已做最小修复。是否完整回归通过，以本 PR Actions 原始结果为准。
