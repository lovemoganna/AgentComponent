# AgentComponent Prompt & Skill Repository

这是 Prompt 与 Skill 仓库的导航地图。不要从目录逐个翻文件，先从“我要解决什么问题”进入。

## 快速入口

| 你现在要做什么 | 推荐 Prompt | 用途 |
|---|---|---|
| 不确定该用文字、表格、图、HTML 还是视频 | [自动选择最佳输出形式](prompts/meta-prompt/select/select-best-output-format.md) | 先判断最省认知成本的输出形式，再直接生成 |
| 把复杂内容写得更短、更清楚、更容易读懂 | [ASD-STE100 清晰表达](prompts/writing/explain/explain-with-asd-ste100.md) | 用接近 ASD-STE100 的受控表达约束解释复杂内容 |
| 用流程、因果、结构或关系图解释问题 | [图解优先](prompts/visualization/generate/generate-diagram-first-explainer.md) | 先选最合适的图，再用图解释 |
| 自主选择最合适的 PlantUML 图来表达流程、依赖、执行计划或性能 | [PlantUML 自主选图](prompts/visualization/generate/select-and-generate-plantuml-diagram.md) | 按关系类型选择 Activity、WBS、Component、Sequence、State、Timing 等图，并直接生成可渲染 PlantUML |
| 把复杂内容做成可交互解释页面 | [HTML 交互解释器](prompts/visualization/generate/generate-html-explainer.md) | 生成可直接打开的单文件 HTML 解释页面 |
| 把一个主题做成动态图形讲解视频 | [讲解视频生成](prompts/visualization/generate/generate-explainer-video.md) | 输出分镜、旁白、画面动作和实现方案 |
| 把模糊想法整理成 Coding Agent 可直接执行的开发需求 | [Vibe Coding 需求表达标准](prompts/coding/specify/write-vibe-coding-requirement.md) | 明确现状、痛点、目标、约束、执行闭环与验收标准 |\n| 把新的高价值 Prompt 规范归档到仓库 | [Prompt 仓库分类与归档](prompts/workflow/maintain/prompt-repository.md) | 查重、分类、命名、入库，并同步维护本 README |
| 把新的 Skill 查重、规范化并存入仓库 | [Skill Repository](skills/skill-repository/SKILL.md) | 负责 Skill 的 canonical 入库、资源归档、README 导航与生命周期维护 |
| 测试、玩耍、调试和持续维护 AI Skills | [Skill Lab](skills/skill-lab/SKILL.md) | 用 exploratory / regression / adversarial 闭环测试 Skill，修复可泛化缺陷并防止历史能力回归 |

## 能力地图

```text
prompts/
├── meta-prompt/
│   └── select/
│       └── 自动选择最佳输出形式
│
├── writing/
│   └── explain/
│       └── ASD-STE100 清晰表达
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
│   └── Skill Repository：查重、规范化、入库与导航维护
└── skill-lab/
    └── Skill Lab：测试、调试、回归与持续维护 Skills
```

## 按能力分类

### Coding\n\n| Prompt | 解决的问题 | 路径 |\n|---|---|---|\n| [Vibe Coding 需求表达标准](prompts/coding/specify/write-vibe-coding-requirement.md) | 把模糊开发想法转换成 Coding Agent 可执行、可验证、可回滚的工程需求 | `prompts/coding/specify/write-vibe-coding-requirement.md` |\n\n### Meta Prompt

| Prompt | 解决的问题 | 路径 |
|---|---|---|
| [自动选择最佳输出形式](prompts/meta-prompt/select/select-best-output-format.md) | 不知道当前内容最适合用哪种形式输出 | `prompts/meta-prompt/select/select-best-output-format.md` |

### Writing

| Prompt | 解决的问题 | 路径 |
|---|---|---|
| [ASD-STE100 清晰表达](prompts/writing/explain/explain-with-asd-ste100.md) | 复杂内容太绕、太长、难读 | `prompts/writing/explain/explain-with-asd-ste100.md` |

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
| [Skill Repository](skills/skill-repository/SKILL.md) | 新 Skill 如何查重、规范化、确定 canonical 路径、保存资源并同步仓库导航 | `skills/skill-repository/SKILL.md` |
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

- `Skill Repository` 管“怎么存、存哪、怎么维护 canonical 资产”。
- `Skill Lab` 管“怎么测、怎么改、怎么证明没有改坏”。

## 使用方式

优先从“快速入口”按任务选择 Prompt 或 Skill。只有在需要了解仓库结构时，再进入具体分类目录。

仓库文件是事实源；本 README 是导航层。任何 Prompt 或 Skill 新增、更新、移动、重命名或删除后，都必须同步更新本页，保证导航与实际仓库一致。
