---
title: 图解优先
category: visualization/generate
tags:
  - diagram
  - visualization
  - explanation
  - cognitive-load
source: reverse-engineered-from-conversation
created: 2026-10-02
updated: 2026-10-02
---

# 用途

先判断最合适的图形表达方式，再用图解释复杂问题，避免先生成长篇文字。

# Prompt

不要先写长篇解释。

先分析下面的问题最适合用什么图表达，例如：

- 流程图
- 因果图
- 架构图
- 时间线
- 对比图
- 决策树
- 状态机
- 数据关系图

选择最合适的一种，直接生成图解。

要求：

- 图中只保留关键对象、关系和变化。
- 禁止把原文机械拆成节点。
- 图必须帮助理解机制，而不是装饰。
- 图后最多补充 5 条必要说明。

内容：
【输入内容】

# 使用条件

- 适合流程、因果、结构、状态、关系和时间演化明显的内容。
- 输入应包含待解释的问题或材料。
- 如果图形无法提升理解效率，不应为了可视化而强行画图。
