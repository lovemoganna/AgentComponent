# Nontechnical public-reference probe — 2026-11-14

**Scope: one current-model output only, NOT a stable-vs-candidate paired run, NOT independently reviewed, NOT blind held-out.** Protocol: [paired-eval-preregistration-20261114.md](paired-eval-preregistration-20261114.md), Task B.

## Input and provenance
Public source: https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai
Parallel web_fetch extraction ID: `extract_95dba8c03118962cf1527ca62f901cb0`. Source excerpt reported acquired 2026-11-13 UTC. Prompt task: explain in <=220 Chinese characters why self-evaluation is not independent verification; give one evidence trail and one limitation; do not fabricate numeric accuracy or human review. Source and task were already exposed in this chat and cannot count as sealed blind held-out.

## Actual model response (verbatim)
> 模型给自己的回答打分，不能证明事实已被独立核实。NIST提出：把回答中的主张与人工整理的参考文档逐条对照，记录“主张—来源—支持理由”的审计轨迹，并检查忠实性、完整性和证据充分性。局限是：即使引用与参考资料一致，也不能据此证明参考资料本身绝对正确，更不能把自动核验等同于独立人工验收。

## Checks and boundaries
- Character count: **142 Unicode code points**, checked in JavaScript using `[...answer].length`; threshold <=220 PASS.
- Source excerpt explicitly supports reference corpus comparison, structured audit trails, and faithfulness/completeness/sufficiency checks. This is a **source-alignment inspection by the same executor**, not independent review.
- The limitation about source truth is an inference from what source-grounded evaluation measures, not a directly quoted NIST claim. No measured accuracy claimed.
- One model answer produced in current conversation; neither stable nor candidate prompt was isolated and applied to a separate model invocation. No comparative score. Model latency, token usage, exact cost unavailable.
- No authenticated lifecycle feedback event is created. External independent reviewer: NOT_RUN. Technical paired A/B: NOT_RUN. Nontechnical paired A/B: NOT_RUN. Decision: NOT_VERIFIED.

## Next validation
Run stable and candidate in separately isolated model sessions with independently sealed, development-nonoverlapping input, equal tools/model/budget and original artifacts, then independent claim verification. Production prompt and Registry remain untouched.
