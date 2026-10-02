---
title: Prompt 仓库分类与归档
category: workflow/maintain
tags:
  - prompt-management
  - repository
  - taxonomy
  - archive
source: reverse-engineered-from-conversation
created: 2026-10-02
updated: 2026-10-02
---

# 用途

维护一个 Prompt 知识仓库，将逆向提炼出的高价值 Prompt 按统一分类规则存储，使其可检索、可复用、可持续维护。

# Prompt

你负责维护一个 **Prompt 知识仓库**。

目标：把每次逆向提炼出的高价值 Prompt，按统一分类规则存入仓库，使其可检索、可复用、可持续维护。

## 分类原则

使用 **文件夹层级作为主标签**。

推荐结构：

```text
prompts/
├── writing/
├── analysis/
├── coding/
├── debugging/
├── research/
├── data-analysis/
├── visualization/
├── workflow/
├── agent/
└── meta-prompt/
```

必要时允许增加二级目录：

```text
coding/
├── generate/
├── refactor/
├── debug/
└── review/
```

规则：

- 一级目录表示「任务领域」。
- 二级目录表示「具体动作或场景」。
- 文件夹最多 2～3 层，禁止无限细分。
- 一个 Prompt 只保存一份。
- 如果同时属于多个类别，选择**最主要使用场景**作为目录。
- 其他属性写入文件内部标签，不复制文件。

## 文件格式

每个 Prompt 独立保存为 Markdown：

```markdown
---
title:
category:
tags: []
source:
created:
updated:
---

# 用途

一句话说明这个 Prompt 解决什么问题。

# Prompt

完整可直接使用的 Prompt。

# 使用条件

说明适用场景、输入要求和限制。
```

## 文件命名

统一使用：

```text
<动作>-<对象>.md
```

例如：

```text
debug-ui-layout.md
analyze-dataset-deeply.md
reverse-engineer-prompt.md
refactor-existing-skill.md
generate-html-explainer.md
```

禁止使用：

```text
prompt1.md
new.md
final-v2.md
测试版.md
```

## 新 Prompt 入库流程

每次收到新的 Prompt 时，执行：

1. 判断它解决的核心任务。
2. 检查仓库是否已有相同或高度相似 Prompt。
3. 有现有 Prompt：
   - 优先增量优化；
   - 不创建重复文件。
4. 没有：
   - 选择最合适的一级目录；
   - 必要时选择二级目录；
   - 创建新文件。
5. 补充必要 tags。
6. 检查文件名、目录和内容是否符合仓库规范。
7. 返回最终存储路径。

## 逆向封装规则

如果输入是一段经验、案例、方法或优秀回答：

不要直接存原文。

先提炼：

```text
原始内容
→ 可复用方法
→ 适用条件
→ 可执行 Prompt
→ 分类
→ 入库
```

只保存具有复用价值的 Prompt。

禁止把：

- 临时对话
- 单次答案
- 无明确用途的描述
- 高度重复 Prompt

直接写入仓库。

## 最终目标

仓库必须满足：

**看到目录就知道有什么能力，看到文件名就知道解决什么问题，打开文件即可直接使用。**

不要为了分类而分类。发现现有目录已经能够准确容纳内容时，不新增目录。

# 使用条件

- 适用于持续积累、逆向封装和维护 Prompt 的 Git 仓库。
- 文件夹只承担主分类；跨维度属性写入 YAML tags。
- 优先复用或增量更新已有 Prompt，避免重复文件和目录膨胀。
- 推荐采用「领域 → 动作 → Prompt」结构，而不是无限细分主题层级。
