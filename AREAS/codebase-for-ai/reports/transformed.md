# TRANSFORMED REPORT

## 1. Metadata

- Area ID: codebase-for-ai
- State: transformed
- Evaluation mode: audit-only
- Date: 2026-03-07
- Agent/model: Codex GPT-5
- Tool permissions: local filesystem plus shell access
- Budget: single interactive coding session
- Evaluator: self-dogfood audit
- Grader approach: static readiness audit plus deterministic repository validation commands
- Raw evidence / log location: unittest and score CLI runs from this session

## 2. Task set summary

- Number of tasks: 3 representative tasks defined, 0 dynamic runs executed yet
- Task distribution: 1 bug-fix, 1 test, 1 repo-qa
- Repeated runs per task: 0

## 3. Static readiness scores

| Metric | Score |
|---|---:|
| S1 Boundary & Entrypoints | 8 |
| S2 Commands & Environment | 7 |
| S3 Contracts & Change Surface | 7 |
| S4 Context Hierarchy & Economy | 6 |
| S5 Examples, Verification & Persistence | 7 |
| **ACRS** | **35** |

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
| ACRS | 35 |
| ATPS | incomplete |
| **AIFS** | **incomplete** |

## 6. Evidence

- Strongest evidence for improvement: committed `unittest` coverage now exercises audit-only scoring, markdown output, and both scaffold CLIs
- Weakest evidence / ambiguity: the repository still lacks a true multi-task dynamic benchmark for the self-evaluation area
- Missing measurements: all dynamic task outcomes, context-efficiency traces, human-intervention notes
- Transcript or run-log locations: current session shell runs for `unittest`, `py_compile`, and `calculate_score.py`
- Grader notes: the transformed state is measurably easier to validate and dogfoods the repository method through `AREAS/codebase-for-ai/`

## 7. Rule-level findings

| Rule | Status | Notes |
|---|---|---|
| R1 Boundary clarity | pass | The self-profile now names the repo’s own bounded area, entrypoints, and verification path. |
| R2 Contract visibility | pass | The metrics schema, CLI contracts, templates, and output artifacts are mapped in one place. |
| R3 Command standardization | pass | Root validation commands are explicit in both the README and self-profile. |
| R4 Verifiability | pass | `tests/test_cli_scripts.py` provides deterministic coverage for the main CLIs. |
| R5 Change locality | pass | The common edit surface remains bounded to docs, scripts, tests, and example areas. |
| R6 Context economy | pass | The root skill remains thin while self-evaluation details live under the area folder. |
| R7 Hierarchical guidance | pass | The repo now demonstrates root -> area-local guidance on itself. |
| R8 Golden path examples | pass | The repository now includes a concrete self-evaluation path plus updated example reports. |
| R9 Knowledge persistence | pass | Current evaluation findings and representative tasks are stored under `AREAS/codebase-for-ai/`. |
| R10 Observability | partial | Validation output is reproducible, but richer trace capture is still absent. |
| R11 Evaluation readiness | pass | The repository can now score its own baseline and transformed audit states with persisted evidence. |

## 8. Recommendation

- Keep / revise / rollback / expand: keep
- Immediate next step: execute a small dynamic task set for `AREAS/codebase-for-ai/` and replace audit-only metrics with measured task outcomes
