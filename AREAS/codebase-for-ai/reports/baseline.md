# BASELINE REPORT

## 1. Metadata

- Area ID: codebase-for-ai
- State: baseline
- Evaluation mode: audit-only
- Date: 2026-03-07
- Agent/model: Codex GPT-5
- Tool permissions: local filesystem plus shell access
- Budget: single interactive coding session
- Evaluator: self-dogfood audit
- Grader approach: static readiness audit only
- Raw evidence / log location: not persisted for the baseline state

## 2. Task set summary

- Number of tasks: 3 representative tasks defined, 0 dynamic runs executed yet
- Task distribution: 1 bug-fix, 1 test, 1 repo-qa
- Repeated runs per task: 0

## 3. Static readiness scores

| Metric | Score |
|---|---:|
| S1 Boundary & Entrypoints | 7 |
| S2 Commands & Environment | 4 |
| S3 Contracts & Change Surface | 6 |
| S4 Context Hierarchy & Economy | 6 |
| S5 Examples, Verification & Persistence | 4 |
| **ACRS** | **27** |

## 4. Dynamic task scores

For audit-only runs, every value and score below is incomplete.

| Metric | Value | Score |
|---|---:|---:|
| Resolve Rate | incomplete | incomplete |
| Valid Patch Rate | incomplete | incomplete |
| Regression-Free Rate | incomplete | incomplete |
| Context Efficiency | incomplete | incomplete |
| Human Dependence | incomplete | incomplete |
| Reuse Gain | incomplete | incomplete |
| **ATPS** | incomplete | incomplete |

## 5. Total

| Metric | Score |
|---|---:|
| ACRS | 27 |
| ATPS | incomplete |
| **AIFS** | **incomplete** |

## 6. Evidence

- Strongest evidence for improvement: the root package already had clear purpose, rules, scoring model, and example auth-area artifacts
- Weakest evidence / ambiguity: root-level validation commands and deterministic tests were missing
- Missing measurements: all dynamic task outcomes, context-efficiency traces, human-intervention notes
- Transcript or run-log locations: none preserved for the baseline state
- Grader notes: this baseline captures the repo before the second quality-improvement loop in this conversation

## 7. Rule-level findings

| Rule | Status | Notes |
|---|---|---|
| R1 Boundary clarity | pass | The repository purpose and major directories were already explicit. |
| R2 Contract visibility | pass | The core contracts lived in `SKILL.md`, `RULE.md`, `EVALUATION.md`, and the templates. |
| R3 Command standardization | partial | Script usage existed, but no root validation command was documented as the canonical proof path. |
| R4 Verifiability | partial | Smoke runs existed, but there was no committed automated test suite. |
| R5 Change locality | pass | Most work stayed inside scripts, templates, and example areas. |
| R6 Context economy | pass | The root skill stayed thin and pushed detail into support files. |
| R7 Hierarchical guidance | pass | Root rules, templates, overlays, and example areas were separated well. |
| R8 Golden path examples | partial | The auth example existed, but the repository itself did not dogfood a self-evaluation area yet. |
| R9 Knowledge persistence | partial | Patterns were documented, but the repo had no dedicated place for its own evaluation loop. |
| R10 Observability | partial | Debug paths existed mainly as manual shell checks. |
| R11 Evaluation readiness | partial | The method was defined, but self-evaluation artifacts for this repository were not yet persisted. |

## 8. Recommendation

- Keep / revise / rollback / expand: revise
- Immediate next step: add deterministic tests, root validation commands, and self-evaluation artifacts for this repository
