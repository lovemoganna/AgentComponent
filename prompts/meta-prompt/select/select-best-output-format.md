---
title: 自动选择最佳输出形式
category: meta-prompt/select
tags:
  - output-format
  - modality-selection
  - cognitive-load
  - explanation
  - meta-prompt
source: reverse-engineered-from-conversation
created: 2026-10-02
updated: 2026-10-02
---

# 用途

先判断最适合当前内容的输出媒介，再直接按该形式完成结果，避免默认把所有问题都回答成文字。

# Prompt

先不要直接回答问题。

判断下面的内容使用哪种输出方式最容易理解：

- 普通文字
- ASD-STE100 风格文字
- 表格
- 流程图 / 架构图
- 信息图
- 交互式 HTML
- 动画 / 讲解视频

选择标准只有一个：

**哪种形式能让用户用最少认知成本理解最多信息。**

然后直接使用该形式完成输出。

如果一种形式不够，可以组合，但不要为了丰富形式而增加形式。

输入：
【输入内容】

# 使用条件

- 适合输出形式尚未确定、内容复杂度差异较大的通用任务。
- 输入应包含待处理内容及必要的输出约束。
- 输出形式选择服务于理解效率，不追求形式数量或视觉复杂度。
