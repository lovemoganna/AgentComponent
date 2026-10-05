---
name: skill-repository
description: 将当前会话中已反复测试并由用户确认满意的 Skill 收录到 lovemoganna/Org-Skills，或更新已有 Canonical Skill。只负责收录和更新，不负责设计、调试或优化。
---

# Skill Repository

## 用途

用于收录已经完成开发和调试，并由用户确认满意的 Skill。用户调用后，将当前会话中最终确定的 Skill 收录到 `lovemoganna/Org-Skills`，或更新仓库中已有的同类 Skill。

本 Skill 只负责收录和更新。不得承担 Skill 设计、调试或优化职责。

## 调用

用户只需表达：

```text
按 Skill Repository 收录当前 Skill
```

## 执行

1. 以当前会话中用户已经确认满意的最终 Skill 为输入。如果最终 Skill 不明确，或必要资源缺失，不得自行推断、补写或虚构，必须指出缺失内容。
2. 读取 `lovemoganna/Org-Skills` 当前状态。检查现有 Skills、根 `README.md`、相关维护规则及相同或高度相似的 Skill。不得仅根据历史对话判断。
3. 检查是否已有对应 Canonical Skill。已有时增量更新，不创建重复版本。没有时生成稳定的 `skill-slug`，保存到 `skills/<skill-slug>/SKILL.md`。
4. 如果 Skill 实际依赖 `scripts`、`references`、`assets` 或其他必要资源，应一并保存并保持原有引用关系。没有实际资源时，不创建空目录或占位文件。
5. 收录阶段不得重新设计、优化或扩展 Skill，不得改变已经确认满意的行为、规则、流程、约束或能力边界。不得为了仓库风格重写正确内容。只允许查重、确定稳定路径、保存文件、修复因移动产生的引用和更新仓库导航。
6. 完成新增或更新后，必须通篇检查并更新 `lovemoganna/Org-Skills/README.md`。至少同步 Skill 名称、用途、能力地图、场景入口、Canonical 路径和相关链接。
7. 写入完成后重新读取仓库。确认 Canonical `SKILL.md` 已存在，必要资源完整，内部引用有效，README 已包含该 Skill，README 路径与实际路径一致，没有重复 Skill，也没有无实际内容的目录或文件。
8. 禁止创建 `v2`、`final`、`new`、`fixed` 等重复 Skill 版本。正常迭代持续维护同一个 Canonical Skill。

## Skill Lab 边界

不得默认调用 `Skill Lab`。只有用户明确要求重新测试、继续优化、验证行为或执行回归测试时，才进入 `Skill Lab`。

## 验收

必须满足：

1. “按 Skill Repository 收录当前 Skill”可以触发完整流程。
2. 同一长期能力只保留一个 Canonical Skill。
3. 已有 Skill 增量更新；只有不存在对应 Skill 时才创建新目录。
4. 收录后的 Skill 保持用户确认满意时的能力和行为。
5. 必要资源完整，无空目录或占位文件。
6. 根 `README.md` 与仓库实际状态一致，并能帮助用户快速找到该 Skill。
7. 最终状态无重复 Skill、无失效引用，Canonical 路径稳定。

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
