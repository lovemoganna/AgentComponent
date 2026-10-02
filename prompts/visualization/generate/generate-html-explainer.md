---
title: HTML 交互解释器
category: visualization/generate
tags:
  - html
  - interactive
  - explainer
  - frontend
  - visualization
source: reverse-engineered-from-conversation
created: 2026-10-02
updated: 2026-10-02
---

# 用途

把复杂内容转成可直接打开的单文件 HTML，通过交互和可视化降低理解成本。

# Prompt

把下面的内容制作成一个**单文件 HTML 交互解释页面**。

目标不是展示原文，而是帮助用户理解。

要求：

- 信息层级清楚。
- 使用卡片、流程、图表、筛选、展开折叠等交互组织复杂信息。
- 能可视化的内容不要只写文字。
- 关键关系、状态、因果和数据必须直观展示。
- 禁止无意义动画和装饰。
- 页面打开即可使用，不依赖后端。
- 最终直接输出完整 HTML。

内容：
【输入内容】

# 使用条件

- 适合信息量较大、存在多个层级或需要交互探索的内容。
- 输入应包含需要解释的完整材料。
- 输出应能离线打开；除非输入明确允许，不依赖后端或外部服务。
