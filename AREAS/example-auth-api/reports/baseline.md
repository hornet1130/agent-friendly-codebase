# BASELINE REPORT

This bundled example report is derived from `AREAS/example-auth-api/metrics/baseline.json`.

## 1. Metadata

- Area ID: auth-api
- State: baseline
- Evaluation mode: full
- Date: 2026-03-07
- Agent/model: bundled example fixture
- Tool permissions: bundled example fixture
- Budget: bundled example fixture
- Evaluator: bundled example
- Grader approach: code-based target validation plus estimated context-efficiency and human-dependence metrics
- Raw evidence / log location: not bundled with this example fixture

## 2. Task set summary

- Number of tasks: 10
- Task distribution: 4 bug-fix, 2 feature, 2 refactor, 1 test, 1 repo-qa
- Repeated runs per task: 1

## 3. Static readiness scores

| Metric | Score |
|---|---:|
| S1 Boundary & Entrypoints | 5 |
| S2 Commands & Environment | 4 |
| S3 Contracts & Change Surface | 6 |
| S4 Context Hierarchy & Economy | 3 |
| S5 Examples, Verification & Persistence | 4 |
| **ACRS** | **22** |

## 4. Dynamic task scores

| Metric | Value | Score |
|---|---:|---:|
| Resolve Rate | 0.45 | 9.00 |
| Valid Patch Rate | 0.65 | 6.50 |
| Regression-Free Rate | 0.55 | 5.50 |
| Context Efficiency | precision 0.42 / recall 0.71 / first hit 0.58 | 5.39 |
| Human Dependence | intervention-free 0.35 / review acceptance 0.40 | 1.85 |
| Reuse Gain | sequence 0.10 / cost reduction 0.08 | 0.46 |
| **ATPS** |  | **28.70** |

## 5. Total

| Metric | Score |
|---|---:|
| ACRS | 22.00 |
| ATPS | 28.70 |
| **AIFS** | **50.70** |

## 6. Evidence

- Strongest evidence for improvement: the example profile defines area boundaries, entrypoints, commands, and common failure patterns in one place
- Weakest evidence / ambiguity: raw run logs and repeated-run statistics are not bundled with this example fixture
- Missing measurements: none in the metrics file, but task transcripts and confidence intervals are omitted
- Transcript or run-log locations: not included in the repository example
- Grader notes: context-efficiency and human-dependence values should be treated as example measurements, not publication-grade results

## 7. Rule-level findings

| Rule | Status | Notes |
|---|---|---|
| R1 Boundary clarity | pass | The profile names the primary path, entrypoints, dependencies, and search seeds. |
| R2 Contract visibility | partial | Contracts are named, but concrete request or response examples are still thin. |
| R3 Command standardization | partial | Canonical commands exist, but the area-local command is not yet reinforced elsewhere. |
| R4 Verifiability | partial | Target and regression commands exist, but reusable evidence and fixtures are limited. |
| R5 Change locality | pass | The common edit surface and dangerous shared files are explicit. |
| R6 Context economy | partial | The skill stays split by responsibility, but some method guidance is repeated across top-level docs. |
| R7 Hierarchical guidance | pass | Root rules, evaluation docs, templates, and area-local profile are cleanly separated. |
| R8 Golden path examples | partial | Golden-path examples are named, but not linked to concrete diffs or files. |
| R9 Knowledge persistence | partial | Known failures are captured, but there is no explicit post-task writeback loop yet. |
| R10 Observability | partial | The profile calls out env mismatches, but the debug path remains shallow. |
| R11 Evaluation readiness | partial | A representative task and metrics fixture exist, but supporting run evidence is incomplete. |

## 8. Recommendation

- Keep / revise / rollback / expand: revise
- Immediate next step: add concrete golden-path diffs and preserve raw run logs for the example task set
