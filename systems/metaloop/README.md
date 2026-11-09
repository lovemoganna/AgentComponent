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
    python systems/metaloop/engine.py promote --write
    python systems/metaloop/engine.py rollback --write
    python systems/metaloop/engine.py run --task my-task.json --journal runlog.jsonl

示例任务 JSON：

    {"id":"price-drop","operation":"percentage_drop","input":{"high":28.46,"low":25.60},"expected":10.0492}

工具适配器（纯函数）：normalize_ascii、normalize_unicode、dedupe_lines、percentage_drop、json_lookup。不得将此适配器集合描述为通用 LLM 的全部能力。

## 可观察结果与边界
6 个冻结测试中，baseline 5/6、candidate 6/6，差异来自非断行空格（NBSP）处理；工程级逐项结果可用 compare 复现。测试集与实现一起开发，因此**不是独立盲测、不能证明提示词或 Agent 效果变好**；registry 默认仍保留旧版为 stable，不自动升级正式 Prompt。

代码的 compare.promotable 只说明确定性示例满足“有提升且无回归”的局部条件。正式升级必须追加独立真实任务、未见样本、多次模型对照、独立评审、版本锁定与成本核验。没有证据则 NOOP。

## 下一轮高价值改进
用真实但尚未参与开发的仓库 Prompt 任务建立跨域 held-out 集；保存模型、上下文与产物哈希，进行隔离 A/B。之后才决定是否增加真正并发、硬超时或外部工具适配器。不要因一轮失败修改所有 Prompt。
