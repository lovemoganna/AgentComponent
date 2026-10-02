# AgentComponent Prompt Repository

这是 Prompt 仓库的导航地图。不要从目录逐个翻文件，先从“我要解决什么问题”进入。

## 快速入口

| 你现在要做什么 | 推荐 Prompt | 用途 |
|---|---|---|
| 不确定该用文字、表格、图、HTML 还是视频 | [自动选择最佳输出形式](prompts/meta-prompt/select/select-best-output-format.md) | 先判断最省认知成本的输出形式，再直接生成 |
| 把复杂内容写得更短、更清楚、更容易读懂 | [ASD-STE100 清晰表达](prompts/writing/explain/explain-with-asd-ste100.md) | 用接近 ASD-STE100 的受控表达约束解释复杂内容 |
| 用流程、因果、结构或关系图解释问题 | [图解优先](prompts/visualization/generate/generate-diagram-first-explainer.md) | 先选最合适的图，再用图解释 |
| 把复杂内容做成可交互解释页面 | [HTML 交互解释器](prompts/visualization/generate/generate-html-explainer.md) | 生成可直接打开的单文件 HTML 解释页面 |
| 把一个主题做成动态图形讲解视频 | [讲解视频生成](prompts/visualization/generate/generate-explainer-video.md) | 输出分镜、旁白、画面动作和实现方案 |
| 把新的高价值 Prompt 规范归档到仓库 | [Prompt 仓库分类与归档](prompts/workflow/maintain/prompt-repository.md) | 查重、分类、命名、入库，并同步维护本 README |

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
│       ├── HTML 交互解释器
│       └── 讲解视频生成
│
└── workflow/
    └── maintain/
        └── Prompt 仓库分类与归档
```

## 按能力分类

### Meta Prompt

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
| [HTML 交互解释器](prompts/visualization/generate/generate-html-explainer.md) | 静态文字不足以承载复杂信息 | `prompts/visualization/generate/generate-html-explainer.md` |
| [讲解视频生成](prompts/visualization/generate/generate-explainer-video.md) | 需要用动态过程逐步解释主题 | `prompts/visualization/generate/generate-explainer-video.md` |

### Workflow

| Prompt | 解决的问题 | 路径 |
|---|---|---|
| [Prompt 仓库分类与归档](prompts/workflow/maintain/prompt-repository.md) | 新 Prompt 如何查重、分类、命名和持续维护 | `prompts/workflow/maintain/prompt-repository.md` |

## 使用方式

优先从“快速入口”按任务选择 Prompt。只有在需要了解仓库结构时，再进入具体分类目录。

仓库文件是事实源；本 README 是导航层。任何 Prompt 新增、更新、移动、重命名或删除后，都必须同步更新本页，保证导航与实际仓库一致。
