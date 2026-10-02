---
name: skill-lab
description: Test, play with, debug, regress, and continuously maintain AI Skills without overfitting to changing user-authored test cases.
---

# Skill Lab

## Purpose

Use this Skill to test, play with, debug, and maintain another AI Skill.

The goal is not to make the current sample pass. The goal is to improve the target Skill's reusable capability while protecting previously verified behavior.

Treat the target Skill as a long-term asset. Treat test cases as evidence.

## Core rule

Never modify a Skill only because one sample looks bad.

Before changing the target Skill, prove that the failure is a reusable Skill defect rather than:

- a bad test case;
- a bad evaluation rule;
- missing input;
- an execution-environment problem;
- an expected capability boundary.

Do not hard-code the current task, dataset, answer, entity, filename, or special-case branch to make one sample pass.

## Test set model

Keep tests separate from the target Skill.

Use three layers:

### regression

Historical cases that exposed a real defect and were fixed.

Purpose: prevent old failures from returning.

Passed regression cases are compatibility contracts. Do not weaken or delete them only to make a new test pass.

### exploratory

New, temporary, user-authored, or frequently changing tasks.

Purpose: play with the Skill and discover its current boundary.

Exploratory cases may change often. A failed exploratory case does not automatically justify a Skill change.

### adversarial

Cases intentionally designed to stress the Skill.

Examples:

- incomplete input;
- conflicting goals;
- ambiguous requests;
- boundary cases;
- very large input;
- invalid input;
- similar-looking but different tasks;
- cases that encourage mechanical templating or overfitting.

Purpose: find brittle rules before users do.

## Repository scaffold

For a maintained Skill, prefer:

```text
<skill>/
├── SKILL.md
├── tests/
│   ├── regression/
│   ├── exploratory/
│   └── adversarial/
├── eval/
│   └── criteria.md
└── CHANGELOG.md
```

Do not create empty structure only for appearance. Add these assets when they are needed by the maintenance workflow.

## Operating workflow

Whenever the user asks to test, retry, optimize, maintain, or "run another round" on a Skill, execute this loop.

### 1. Read current facts

Read the target repository as the source of truth:

- current `SKILL.md`;
- related code and resources;
- current tests;
- evaluation criteria;
- `CHANGELOG.md`;
- recent valid test evidence when available.

Do not reconstruct current behavior from old conversation memory when repository state is available.

### 2. Build the test batch

The batch should contain, when available:

```text
representative regression
+
current exploratory
+
necessary adversarial
```

Do not test only the newest sample.

If regression is large, select representative cases that cover previously known defect classes.

### 3. Run the current Skill unchanged

First establish the baseline.

Do not edit the Skill during the baseline run.

Record only useful evidence:

- input;
- actual behavior;
- actual output;
- expected behavior;
- meaningful delta.

### 4. Classify every failure

Classify failures as one of:

```text
Skill defect
Test defect
Evaluation defect
Missing input
Execution-environment problem
Expected capability boundary
```

Only a confirmed Skill defect can enter the modification path.

### 5. Find the reusable root cause

Trace:

```text
Observed failure
→ triggering mechanism
→ missing / wrong Skill rule
→ reusable correction
```

Prefer fixing:

- decision logic;
- input routing;
- execution order;
- tool-use rules;
- output-quality constraints;
- self-check logic;
- stop conditions.

Do not begin with sample-specific exceptions.

### 6. Make the smallest useful change

Existing correct behavior is locked by default.

Change only the minimum scope that explains the defect.

Do not:

- rewrite the whole Skill without evidence;
- refactor unrelated correct content;
- add rules merely to look more complete;
- trade away passed regression behavior for the newest sample.

### 7. Re-test in order

After a change, test:

```text
original failing case
→ regression
→ new generalization case
→ adversarial
```

A fix is not proven by the original failing case alone.

### 8. Perform reverse-diff verification

Ask:

- What real failure disappeared?
- What only changed wording or layout?
- What did not improve?
- Did any old behavior regress?
- Did the change create a new mechanical pattern?
- Did complexity increase more than capability?

Cosmetic change is not capability improvement.

### 9. Keep or revert

Keep the modification only if:

- the real defect is fixed;
- the change is reusable;
- regression remains acceptable;
- no material new side effect appears;
- complexity growth is justified.

Otherwise revert or repair again.

### 10. Promote useful tests

If an exploratory case exposed a real, reproducible Skill defect and the fix is verified, promote the case or its minimal reusable form into `tests/regression/`.

Do not archive every exploratory test.

Keep exploratory disposable.

### 11. Update maintenance evidence

After a verified Skill change, update `CHANGELOG.md` with:

```text
Problem
Root cause
Change
New regression
Verification result
Known remaining issue
```

If the repository has a README, Skill index, capability map, or maintenance map, update it when the changed Skill affects that navigation.

## Autonomous loop mode

If the user says:

- continue optimizing;
- run another round;
- keep fixing;
- test until stable;
- do not ask midway;

run:

```text
baseline
→ defect detection
→ root cause
→ minimal repair
→ failing-case retest
→ regression
→ generalization
→ adversarial
→ reverse-diff
→ next loop
```

Stop when:

- no new material defect is found;
- remaining changes are low-value polish;
- further changes begin to damage historical capability;
- required external information is missing;
- explicit acceptance criteria are met.

Do not manufacture changes merely to keep the loop moving.

## User-authored tests

A new user test is `exploratory` by default.

Process it as:

```text
new test
→ run unchanged Skill
→ classify failure
→ prove reusable defect
→ repair Skill
→ verify
→ promote to regression only if warranted
```

The user's test set is allowed to change frequently. The Skill must not chase every test mutation.

## Maintenance audit mode

When the user asks to maintain or clean up a Skill that has been iterated many times, inspect for:

- sample-specific hard-coding;
- duplicated rules;
- conflicting rules;
- obsolete rules;
- regression cases that no longer represent real defects;
- exploratory cases that should be promoted or discarded;
- complexity growth without capability growth;
- recent changes that silently degraded older behavior.

Do not rewrite correct content only for stylistic consistency.

Any removal or simplification must pass regression and generalization checks.

## Output contract

For normal rounds, report only:

```text
Material problems found
What changed
Test result
Regression status
Remaining real issues
Repository paths / commit
```

Do not dump internal execution logs unless the user asks for them.

## Success condition

The target Skill should become easier to trust over time:

```text
changing exploratory tests
        ↓
real defects discovered
        ↓
reusable Skill fixes
        ↓
regression memory grows
        ↓
old failures stay fixed
        ↓
Skill capability improves without uncontrolled complexity
```
