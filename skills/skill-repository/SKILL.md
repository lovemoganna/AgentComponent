---
name: skill-repository
description: 收录或更新当前会话中已经调试满意的 Skill。目标仓库固定为 lovemoganna/Org-Skills。负责查重、Canonical 路径、必要资源保存、README 导航同步和回读校验；不负责重新设计或调试 Skill。
---

# Skill Repository

## 用途

用于收录已经完成开发、反复测试并由用户确认满意的 Skill。

典型场景：用户正在另一个 Skill 会话中开发和调试 Skill。当前版本已经满意。此时调用本 Skill，将当前会话中最终确定的 Skill 收录到 `lovemoganna/Org-Skills`，或更新仓库中已有的同类 Skill。

本 Skill 只负责收录和更新。它不是 Skill 设计器，也不是 Skill 调试器。

## 默认调用

用户表达以下意图时执行：

```text
按 Skill Repository 收录当前 Skill
```

也包括语义等价表达，例如“把当前 Skill 收录到 Org-Skills”“更新仓库里的这个 Skill”。

## 事实源

执行收录前，必须读取 `lovemoganna/Org-Skills` 当前 HEAD。

至少检查：

1. `README.md`
2. `MAINTENANCE.md`
3. `skills/` 当前目录
4. 与当前 Skill 相同或高度相似的 Skill
5. 当前 Skill 实际依赖的资源

仓库当前状态优先于聊天记录中的旧版本、历史附件和本地副本。

## 输入

默认输入是当前会话中用户已经确认满意的最终 Skill。

如果当前会话没有明确的最终 Skill，或者必要资源缺失，不得自行推断、补写或虚构。必须明确指出缺失内容。

不得把草稿、中间版本、被用户否定的版本或尚未确认的方案作为最终收录内容。

## 收录流程

### 1. 提取最终 Skill

从当前会话中确定最终版本。

保留已经确认满意的：

1. 行为
2. 规则
3. 流程
4. 约束
5. 能力边界
6. 必要资源和引用关系

收录阶段不得重新设计 Skill，不得擅自优化 Skill。

### 2. 检查重复和相似能力

检查 `lovemoganna/Org-Skills` 是否已有相同或高度相似的 Skill。

如果已有对应 Canonical Skill，增量更新现有 Skill。

如果没有对应 Skill，生成稳定的 `skill-slug`，保存到：

```text
skills/<skill-slug>/SKILL.md
```

禁止创建以下重复版本：

```text
v2
final
new
fixed
```

正常迭代必须持续维护同一个 Canonical Skill。

### 3. 保存必要资源

如果当前 Skill 实际依赖以下资源，应与 Skill 一同保存：

```text
scripts/
references/
assets/
tests/
eval/
CHANGELOG.md
```

只保存实际存在且被 Skill 使用的资源。

不得为了目录完整创建空目录或占位文件。

不得丢失原有相对引用关系。

### 4. 只做收录必需修改

不得因为仓库规范重新改写已经正确的 Skill 内容。

只允许执行收录所必需的处理，例如：

1. 查重
2. 确定稳定路径
3. 保存文件
4. 修复因移动产生的路径引用
5. 更新仓库导航

除上述必要处理外，不得改变 Skill 已确认的行为、规则、流程、约束或能力边界。

### 5. 更新 README

完成 Skill 新增或更新后，必须通篇检查并更新 `lovemoganna/Org-Skills/README.md`。

README 必须继续作为仓库导航地图。

至少同步：

1. Skill 名称
2. 一句话用途
3. 快速场景入口
4. Skill 能力地图
5. Canonical 路径
6. 相关链接
7. 与相近 Skill 的能力边界，必要时更新

README 未同步完成时，不得判定收录完成。

### 6. 回读校验

写入后必须重新读取仓库并确认：

1. Canonical `SKILL.md` 已存在
2. 必要资源已保存
3. 内部引用有效
4. README 已包含该 Skill
5. README 路径与实际仓库一致
6. 未产生重复 Skill
7. 未创建无实际内容的目录
8. 已确认满意的 Skill 行为没有因收录过程被隐性改写

## Skill Lab 边界

不得默认调用 `Skill Lab`。

当前场景的前提是 Skill 已经在前面的会话中完成调试并得到用户确认。

只有用户明确要求以下行为时，才进入 `Skill Lab`：

1. 重新测试
2. 继续优化
3. 验证行为
4. 做回归测试
5. 查找新的 Skill 缺陷

## 验收标准

必须同时满足：

1. 用户只需表达“按 Skill Repository 收录当前 Skill”即可触发完整流程。
2. 同一长期能力只保留一个 Canonical Skill。
3. 已有 Skill 增量更新；新 Skill 才创建新目录。
4. 收录后的 Skill 保持用户确认满意时的能力和行为。
5. 必要资源完整。
6. 无实际内容的目录不得创建。
7. 根 `README.md` 与仓库实际状态一致。
8. README 能让用户快速找到该 Skill。
9. 最终状态无重复 Skill、无失效引用、路径稳定。

## 输出

完成后只返回：

```text
操作结果：新增 / 更新
Canonical Skill 路径
实际修改的资源
README 更新状态
校验结果
commit
```

不要输出无关执行日志。
