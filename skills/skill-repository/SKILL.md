---
name: skill-repository
description: Archive, deduplicate, normalize, index, and maintain AI Skills in a Git repository without creating duplicate or sample-specific Skill variants.
---

# Skill Repository

## Purpose

Use this Skill to store and maintain AI Skills as long-term repository assets.

It is responsible for:

~~~text
receive Skill
→ inspect repository
→ detect duplicate / overlap
→ normalize package
→ choose stable path
→ archive Skill and resources
→ update repository map
→ hand off to Skill Lab for validation when appropriate
~~~

It does not replace `skill-lab`.

- **Skill Repository** decides how a Skill enters and lives in the repository.
- **Skill Lab** decides whether the Skill works, how it should be tested, and whether a change is safe.

## Core rule

A Skill is not considered archived until:

1. repository duplicate checks are complete;
2. the Skill has one stable canonical location;
3. required resources are stored with it;
4. repository navigation is updated;
5. links and paths are verified.

Do not create `v2`, `final`, `new`, `fixed`, or sample-specific duplicate Skills when an existing canonical Skill should be updated.

## Default repository structure

Prefer:

~~~text
skills/
└── <skill-slug>/
    ├── SKILL.md
    ├── references/      # only when the Skill actually needs reference files
    ├── scripts/         # only when executable helpers are required
    ├── templates/       # only when reusable templates are required
    ├── tests/           # created when real tests exist
    │   ├── regression/
    │   ├── exploratory/
    │   └── adversarial/
    ├── eval/            # only when explicit evaluation criteria exist
    └── CHANGELOG.md     # created when the Skill begins iterative maintenance
~~~

Do not create empty directories for appearance.

## Canonical identity

Each Skill must have one stable identity.

Use:

~~~text
skills/<skill-slug>/SKILL.md
~~~

The slug should:

- describe the Skill's durable capability;
- use lowercase kebab-case;
- stay stable across normal revisions;
- avoid dates, versions, temporary project names, and test-case names.

Good:

~~~text
skill-lab
sql-business-thinking
org-literate-engineering
data-quality-audit
~~~

Bad:

~~~text
skill-v2
final-skill
sql-skill-fixed
dataset-2026-test
new-analysis-skill
~~~

## Archive workflow

Whenever the user asks to save, archive, add, import, maintain, or put a Skill into the repository, execute the following workflow.

### 1. Read repository state first

Treat the current repository as the source of truth.

Inspect:

- current `skills/` tree;
- root `README.md`;
- existing Skill names and descriptions;
- likely overlapping Skills;
- the target Skill package and referenced resources.

Do not decide the destination only from conversation memory.

### 2. Identify the Skill's durable capability

Reduce the incoming Skill to:

~~~text
What job does this Skill repeatedly perform?
What inputs does it accept?
What decisions does it own?
What outputs does it produce?
What makes it materially different from existing Skills?
~~~

Use that capability to choose the canonical name and path.

Do not name the Skill after the current test case.

### 3. Check duplicates and overlap

Before creating a new directory, compare the incoming Skill with existing Skills.

Check:

- name;
- description;
- purpose;
- workflow;
- trigger conditions;
- owned decisions;
- expected outputs;
- referenced tools and resources.

Classify the result as:

~~~text
same Skill
highly overlapping Skill
complementary Skill
new Skill
~~~

#### Same Skill

Update the existing canonical Skill.

Do not create another copy.

#### Highly overlapping Skill

Prefer merging into the existing canonical Skill if both are trying to own the same durable capability.

Do not merge only because they share vocabulary.

If merging would destroy a real boundary, keep them separate and make the boundary explicit.

#### Complementary Skill

Keep separate.

Example:

~~~text
skill-repository = storage and repository lifecycle
skill-lab        = testing and iterative quality maintenance
~~~

#### New Skill

Create a new canonical directory.

### 4. Normalize without rewriting valid capability

Preserve the incoming Skill's real behavior.

Only normalize what is necessary for repository consistency:

- stable frontmatter;
- stable name;
- clear description;
- canonical path;
- broken references;
- required local resources;
- obvious duplicated packaging.

Do not rewrite correct Skill logic merely for style consistency.

Do not silently remove constraints, examples, tests, scripts, or reference files that are required by the Skill.

### 5. Archive resources with the Skill

If the Skill depends on local files, store them inside its canonical Skill directory when practical.

Keep relative references valid.

Examples:

~~~text
skills/<slug>/references/...
skills/<slug>/scripts/...
skills/<slug>/templates/...
~~~

Do not copy unrelated repository files into the Skill directory.

Do not create placeholder resource files.

### 6. Initialize maintenance assets only when justified

A new Skill does not automatically need every maintenance directory.

Create assets when real content exists:

- `tests/exploratory/`: when the user provides active test cases;
- `tests/regression/`: after a verified defect becomes a historical contract;
- `tests/adversarial/`: when stress cases are intentionally maintained;
- `eval/criteria.md`: when explicit quality criteria exist;
- `CHANGELOG.md`: once the Skill starts accumulating verified maintenance changes.

Never create empty structure only to make the package look mature.

### 7. Update repository navigation

README synchronization is an archive completion condition.

After any Skill is:

- added;
- updated in a way that changes capability;
- moved;
- renamed;
- merged;
- split;
- deleted;

update the root `README.md` against the current repository state.

The README must act as a **Skill navigation map**, not merely a file list.

At minimum keep synchronized:

- quick task entry;
- Skill name;
- one-line purpose;
- canonical path;
- capability map;
- boundary between related Skills.

Verify:

- no missing Skill;
- no duplicate Skill entry;
- no stale path;
- no dead link;
- README matches the actual repository tree.

If README synchronization is incomplete, the archive operation is incomplete.

### 8. Validate the stored package

Before declaring success, verify:

~~~text
canonical SKILL.md exists
required resources exist
relative references resolve
README contains the Skill
README path matches repository path
no accidental duplicate Skill was created
~~~

When practical, perform a minimal structural smoke test.

If the Skill needs behavioral testing or has just been materially changed, hand it to `skill-lab`.

Use this lifecycle:

~~~text
Skill Repository
→ canonical archive
→ Skill Lab
→ exploratory test
→ verified defect
→ reusable fix
→ regression
→ Skill Repository keeps canonical package and navigation current
~~~

## Updating an existing Skill

When the user provides a revised Skill:

1. find the canonical Skill;
2. compare the new version with repository HEAD;
3. preserve correct existing content by default;
4. apply only intended or evidence-backed changes;
5. preserve required resources and historical tests;
6. do not delete regression assets merely because they are absent from the incoming draft;
7. update README if capability, name, boundary, or path changed;
8. use Skill Lab when behavioral validation is needed.

## Moving or renaming a Skill

Only rename or move a Skill when there is a real identity or taxonomy problem.

When moving or renaming:

~~~text
move canonical package
→ repair internal references
→ repair external repository references
→ update README
→ verify old path is no longer referenced
~~~

Do not rename a stable Skill merely because the wording can be improved.

## Deleting or merging a Skill

Before deletion or merge, prove that the Skill is:

- duplicate;
- obsolete;
- fully superseded;
- or intentionally consolidated.

Preserve unique capability, tests, references, scripts, and maintenance history before removal.

After deletion or merge:

- remove stale README entries;
- repair references;
- verify there is still exactly one canonical owner for the capability.

## User commands

### Archive a new Skill

~~~text
Use Skill Repository to archive this Skill into AgentComponent.

First inspect the current repository and check for duplicates.
If a canonical Skill already exists, update it instead of creating a duplicate.
Preserve required resources.
Update the README navigation map.
Then validate the stored package.

Skill:
【input】
~~~

### Archive and test

~~~text
Use Skill Repository to archive this Skill.
After canonical storage is complete, use Skill Lab to run a smoke / exploratory test.
Only persist behavioral changes that pass regression and generalization checks.
~~~

### Update an existing Skill

~~~text
Use Skill Repository to maintain <skill-name> from the current repository HEAD.

Apply this revision incrementally.
Do not create another version directory.
Preserve valid existing resources and regression tests.
Update README only where repository capability or navigation actually changes.
~~~

## Output contract

Return only useful maintenance results:

~~~text
Decision: created / updated / merged / kept separate
Canonical Skill path
Resources changed
README status
Validation status
Commit
Remaining real issue
~~~

Do not dump low-level repository logs unless requested.

## Success condition

The repository should converge toward:

~~~text
one durable capability
        ↓
one canonical Skill
        ↓
one stable path
        ↓
resources live with the Skill
        ↓
README makes it easy to find
        ↓
Skill Lab proves behavior over time
~~~

Avoid both failure modes:

~~~text
same capability → many Skill copies
~~~

and

~~~text
different capabilities → forced into one giant Skill
~~~
