---
title: PlantUML 自主选图
category: visualization/generate
tags:
  - plantuml
  - diagram-selection
  - visualization
  - sql
  - explain
  - meta-prompt
source: reverse-engineered-from-conversation
created: 2026-10-02
updated: 2026-10-02
---

# 用途

根据用户真正需要看清的关系，自主选择最合适的 PlantUML 图类型并直接生成，避免默认使用流程图或机械拆节点。

# Prompt

请分析下面的内容，并自主选择最适合的 **PlantUML 图类型**进行表达。

不要默认使用流程图。

先判断用户真正需要理解什么，再选图。

可选图类型包括：

- **Activity Diagram**：步骤、流程、算法、SQL 数据处理链。
- **MindMap / WBS**：层级、执行计划树、知识结构、任务拆解。
- **Component Diagram**：模块、系统、表、CTE、子查询之间的依赖关系。
- **Sequence Diagram**：对象之间按顺序发生的调用、交互和数据传递。
- **State Diagram**：对象或数据从一种状态变成另一种状态。
- **Timing Diagram**：耗时、性能、阶段持续时间、时间关系。
- **Class / Object Diagram**：对象、字段、属性及关系。
- **ER 风格关系图**：表、实体、主键、外键和数据关系。
- 其他 PlantUML 图：只有明显更合适时才使用。

## 自主决策规则

先回答一个问题：

**用户最需要看清的是“什么关系”？**

按下面规则选图：

- 看“先做什么、后做什么” → Activity
- 看“谁包含谁、谁属于谁” → MindMap / WBS
- 看“谁依赖谁” → Component
- 看“谁调用谁、先后如何” → Sequence
- 看“东西如何发生状态变化” → State
- 看“时间耗在哪里” → Timing
- 看“数据对象及字段关系” → Class / ER

如果一种图已经能完整解释问题，只生成一种。

只有单图明显无法表达时，才组合最多两种图，并让两张图分别回答不同问题。

## SQL 专用规则

如果输入是 SQL，先判断分析目标：

- 理解 SQL 如何一步步处理数据 → **Activity Diagram**
- 查看 `EXPLAIN` 执行计划 → **MindMap / WBS**
- 查看表、CTE、子查询依赖 → **Component Diagram**
- 查看多个 CTE / 子查询之间的数据传递 → **Sequence Diagram**
- 查看数据经过每一步后的状态变化 → **State Diagram**
- 查看 `EXPLAIN ANALYZE` 性能与耗时 → **Timing Diagram**

禁止把 SQL 书写顺序机械画成：

`SELECT → FROM → WHERE → GROUP BY`

应还原真实的数据处理逻辑或数据库执行结构。

## 图形要求

- 只保留帮助理解的对象、关系、变化和关键数据。
- 不机械地把原文每一句拆成节点。
- 不为了“图复杂”而增加节点。
- 同类节点使用一致视觉样式。
- 不同语义节点使用不同颜色或样式。
- 节点内部区分：业务含义、技术动作、代码或关键字。
- 专业代码、SQL、字段名使用等宽字体。
- 关键路径必须一眼可以识别。
- 优先控制交叉连线和无意义回折。

## PlantUML 语法约束

延续当前 PlantUML 风格：

- 使用 `!define` 集中管理颜色、字体和样式。
- 使用 `skinparam` 管理全局样式。
- 优先使用简洁的链式语法。
- 可以使用 `-r->`、`-d->` 等方向控制布局。
- 可以使用 `<color>`、`<size>`、`<font>`、`<b>` 等富文本区分节点内部元素。
- **任何 XML / HTML-like 标签禁止跨物理行格式化。**
- 节点内部需要视觉换行时，只使用 `\n`。
- 保证所有标签完整闭合。
- 优先保证 PlantUML 可以直接渲染，不为了源码排版牺牲语法正确性。

## 输出规则

直接输出最终 PlantUML。

不要先输出长篇分析。

如果需要说明选图原因，只允许在代码前写一句：

**选择：XXX Diagram，因为需要看清 XXX。**

输入：

【输入内容】

# 使用条件

- 适用于需要把流程、层级、依赖、交互、状态、性能或数据关系转换为 PlantUML 的任务。
- 尤其适合 SQL 逻辑执行、DuckDB `EXPLAIN`、`EXPLAIN ANALYZE`、CTE 依赖和数据流分析。
- 输入应包含待分析内容；如果要求还原数据库真实执行过程，应同时提供执行计划或性能分析结果。
- 图类型选择服务于理解效率，不为了形式丰富而组合多种图。
- PlantUML 富文本标签必须保持在同一物理行，避免解析错误。
