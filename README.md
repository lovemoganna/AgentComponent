# AgentComponent Prompt & Skill Repository

这是 Prompt 与 Skill 仓库的导航地图。不要从目录逐个翻文件，先从“我要解决什么问题”进入。

## 快速入口

| 你现在要做什么 | 推荐 Prompt | 用途 |
|---|---|---|
| 不确定该用文字、表格、图、HTML 还是视频 | [自动选择最佳输出形式](prompts/meta-prompt/select/select-best-output-format.md) | 先判断最省认知成本的输出形式，再直接生成 |
| 把复杂内容写得更短、更清楚、更容易读懂 | [ASD-STE100 清晰表达](prompts/writing/explain/explain-with-asd-ste100.md) | 用接近 ASD-STE100 的受控表达约束解释复杂内容 |
| 核验一个概念并找到真正讲透它的学习资料 | [概念核验与深度学习资料检索](prompts/research/discover/research-concept-learning-materials.md) | 先核验概念名称、定义和来源，再交叉筛选原始、高质量、可学习的资料 |
| 把已有技术材料写成中英双语 Twitter / X Thread | [Twitter / X 技术 Thread 生成](prompts/writing/generate/generate-twitter-technical-thread.md) | 提炼中心判断，保留真实机制和工作流，生成 8 至 10 条技术 Thread |
| 把公开加密行业事件转成专业 LinkedIn 风险情报博文 | [LinkedIn 加密风险情报博文生成](prompts/writing/generate/generate-linkedin-crypto-risk-intelligence-post.md) | 先核验事实，再提炼风险机制、业务影响和独立判断，生成中英双语 LinkedIn 内容 |
| 用流程、因果、结构或关系图解释问题 | [图解优先](prompts/visualization/generate/generate-diagram-first-explainer.md) | 先选最合适的图，再用图解释 |
| 自主选择最合适的 PlantUML 图来表达流程、依赖、执行计划或性能 | [PlantUML 自主选图](prompts/visualization/generate/select-and-generate-plantuml-diagram.md) | 按关系类型选择 Activity、WBS、Component、Sequence、State、Timing 等图，并直接生成可渲染 PlantUML |
| 把复杂内容做成可交互解释页面 | [HTML 交互解释器](prompts/visualization/generate/generate-html-explainer.md) | 生成可直接打开的单文件 HTML 解释页面 |
| 把一个主题做成动态图形讲解视频 | [讲解视频生成](prompts/visualization/generate/generate-explainer-video.md) | 输出分镜、旁白、画面动作和实现方案 |
| 把模糊想法整理成 Coding Agent 可直接执行的开发需求 | [Vibe Coding 需求表达标准](prompts/coding/specify/write-vibe-coding-requirement.md) | 明确现状、痛点、目标、约束、执行闭环与验收标准 |
| 把新的高价值 Prompt 规范归档到仓库 | [Prompt 仓库分类与归档](prompts/workflow/maintain/prompt-repository.md) | 查重、分类、命名、入库，并同步维护本 README |
| 把当前会话中已经调试满意的 Skill 收录或更新到 Org-Skills | [Skill Repository](skills/skill-repository/SKILL.md) | 读取 `lovemoganna/Org-Skills` 当前 HEAD，查重后新增或更新 Canonical Skill，并同步 Org-Skills README；不重新设计或调试 Skill |
| 测试、玩耍、调试和持续维护 AI Skills | [Skill Lab](skills/skill-lab/SKILL.md) | 用 exploratory / regression / adversarial 闭环测试 Skill，修复可泛化缺陷并防止历史能力回归 |

## 能力地图

```text
prompts/
├── coding/
│   └── specify/
│       └── Vibe Coding 需求表达标准
│
├── meta-prompt/
│   └── select/
│       └── 自动选择最佳输出形式
│
├── research/
│   └── discover/
│       └── 概念核验与深度学习资料检索
│
├── writing/
│   ├── explain/
│   │   └── ASD-STE100 清晰表达
│   └── generate/
│       ├── Twitter / X 技术 Thread 生成
│       └── LinkedIn 加密风险情报博文生成
│
├── visualization/
│   └── generate/
│       ├── 图解优先
│       ├── PlantUML 自主选图
│       ├── HTML 交互解释器
│       └── 讲解视频生成
│
└── workflow/
    └── maintain/
        └── Prompt 仓库分类与归档

skills/
├── skill-repository/
│   └── Skill Repository：将已调试满意的 Skill 收录或更新到 Org-Skills
└── skill-lab/
    └── Skill Lab：测试、调试、回归与持续维护 Skills
```

## 按能力分类

### Coding

| Prompt | 解决的问题 | 路径 |
|---|---|---|
| [Vibe Coding 需求表达标准](prompts/coding/specify/write-vibe-coding-requirement.md) | 把模糊开发想法转换成 Coding Agent 可执行、可验证、可回滚的工程需求 | `prompts/coding/specify/write-vibe-coding-requirement.md` |

### Meta Prompt

| Prompt | 解决的问题 | 路径 |
|---|---|---|
| [自动选择最佳输出形式](prompts/meta-prompt/select/select-best-output-format.md) | 不知道当前内容最适合用哪种形式输出 | `prompts/meta-prompt/select/select-best-output-format.md` |

### Research

| Prompt | 解决的问题 | 路径 |
|---|---|---|
| [概念核验与深度学习资料检索](prompts/research/discover/research-concept-learning-materials.md) | 概念名称可能不准确时，如何先核验定义和来源，再筛选真正能讲透概念的高质量学习资料 | `prompts/research/discover/research-concept-learning-materials.md` |

### Writing

| Prompt | 解决的问题 | 路径 |
|---|---|---|
| [ASD-STE100 清晰表达](prompts/writing/explain/explain-with-asd-ste100.md) | 复杂内容太绕、太长、难读 | `prompts/writing/explain/explain-with-asd-ste100.md` |
| [Twitter / X 技术 Thread 生成](prompts/writing/generate/generate-twitter-technical-thread.md) | 已有技术材料如何压成中英双语 Twitter / X Thread，同时保留真实机制、工作流和独特价值 | `prompts/writing/generate/generate-twitter-technical-thread.md` |
| [LinkedIn 加密风险情报博文生成](prompts/writing/generate/generate-linkedin-crypto-risk-intelligence-post.md) | 如何把公开加密行业事件、监管与执法材料转成经过事实核验、体现风险机制和业务判断的中英双语 LinkedIn 博文 | `prompts/writing/generate/generate-linkedin-crypto-risk-intelligence-post.md` |

### Visualization

| Prompt | 解决的问题 | 路径 |
|---|---|---|
| [图解优先](prompts/visualization/generate/generate-diagram-first-explainer.md) | 文字不如图容易理解 | `prompts/visualization/generate/generate-diagram-first-explainer.md` |
| [PlantUML 自主选图](prompts/visualization/generate/select-and-generate-plantuml-diagram.md) | 不知道该用哪种 PlantUML 图表达流程、层级、依赖、交互、状态、SQL 执行计划或性能 | `prompts/visualization/generate/select-and-generate-plantuml-diagram.md` |
| [HTML 交互解释器](prompts/visualization/generate/generate-html-explainer.md) | 静态文字不足以承载复杂信息 | `prompts/visualization/generate/generate-html-explainer.md` |
| [讲解视频生成](prompts/visualization/generate/generate-explainer-video.md) | 需要用动态过程逐步解释主题 | `prompts/visualization/generate/generate-explainer-video.md` |

### Workflow

| Prompt | 解决的问题 | 路径 |
|---|---|---|
| [Prompt 仓库分类与归档](prompts/workflow/maintain/prompt-repository.md) | 新 Prompt 如何查重、分类、命名和持续维护 | `prompts/workflow/maintain/prompt-repository.md` |

## Skills

| Skill | 解决的问题 | 路径 |
|---|---|---|
| [Skill Repository](skills/skill-repository/SKILL.md) | 将当前会话中已调试满意的 Skill 查重后收录或更新到 `lovemoganna/Org-Skills`，并同步其 README 导航 | `skills/skill-repository/SKILL.md` |
| [Skill Lab](skills/skill-lab/SKILL.md) | 测试集经常变化时，如何持续测试、修正和维护 Skills，同时防止针对单一样本过拟合和历史能力回归 | `skills/skill-lab/SKILL.md` |

## Skills 分工

```text
新 Skill / 新版本
      ↓
Skill Repository
  查重 → 规范化 → canonical 入库 → README 导航
      ↓
Skill Lab
  exploratory → 缺陷定位 → 修正 → regression → adversarial
      ↓
Skill Repository
  保持 canonical 包与仓库导航持续一致
```

- `Skill Repository` 管“把已经调试满意的 Skill 收录或更新到 `lovemoganna/Org-Skills`”，不负责重新设计或调试。
- `Skill Lab` 管“怎么测、怎么改、怎么证明没有改坏”。

## 使用方式

优先从“快速入口”按任务选择 Prompt 或 Skill。只有在需要了解仓库结构时，再进入具体分类目录。

仓库文件是事实源；本 README 是导航层。任何 Prompt 或 Skill 新增、更新、移动、重命名或删除后，都必须同步更新本页，保证导航与实际仓库一致。
