# TRANSFORMED REPORT

This bundled example report is derived from `AREAS/example-auth-api/metrics/transformed.json`.

## 1. Metadata

- Area ID: auth-api
- State: transformed
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
| S1 Boundary & Entrypoints | 7 |
| S2 Commands & Environment | 7 |
| S3 Contracts & Change Surface | 7 |
| S4 Context Hierarchy & Economy | 6 |
| S5 Examples, Verification & Persistence | 7 |
| **ACRS** | **34** |

## 4. Dynamic task scores

| Metric | Value | Score |
|---|---:|---:|
| Resolve Rate | 0.72 | 14.40 |
| Valid Patch Rate | 0.84 | 8.40 |
| Regression-Free Rate | 0.79 | 7.90 |
| Context Efficiency | precision 0.61 / recall 0.83 / first hit 0.76 | 7.06 |
| Human Dependence | intervention-free 0.63 / review acceptance 0.70 | 3.29 |
| Reuse Gain | sequence 0.24 / cost reduction 0.19 | 1.10 |
| **ATPS** |  | **42.15** |

## 5. Total

| Metric | Score |
|---|---:|
| ACRS | 34.00 |
| ATPS | 42.15 |
| **AIFS** | **76.15** |

## 6. Evidence

- Strongest evidence for improvement: the transformed fixture assumes clearer commands, stronger examples, and more reusable guidance, which lift both readiness and dynamic outcomes
- Weakest evidence / ambiguity: raw run logs are still omitted, so this example is useful as a format reference rather than a definitive benchmark
- Missing measurements: repeated-run statistics and full transcripts are not included in the repository example
- Transcript or run-log locations: not included in the repository example
- Grader notes: this example demonstrates report shape and score interpretation, not a formally audited benchmark package

## 7. Rule-level findings

| Rule | Status | Notes |
|---|---|---|
| R1 Boundary clarity | pass | The transformed fixture assumes tighter area guidance and clearer search entrypoints. |
| R2 Contract visibility | pass | Contract surfaces and likely changes are easier to trace in the transformed state. |
| R3 Command standardization | pass | Area-scoped and broader commands are both explicit and easier to trust. |
| R4 Verifiability | pass | Validation paths are stronger and dynamic metrics improve materially. |
| R5 Change locality | pass | Common edit boundaries remain bounded and more predictable. |
| R6 Context economy | partial | Context hierarchy improves, but some top-level guidance is still duplicated. |
| R7 Hierarchical guidance | pass | The transformed state retains a clean root-to-area narrowing path. |
| R8 Golden path examples | pass | The transformed fixture assumes examples are concrete enough to improve downstream task success. |
| R9 Knowledge persistence | pass | Learned patterns are more reusable across related tasks. |
| R10 Observability | partial | Debugging improves, but the example still lacks concrete log bundles. |
| R11 Evaluation readiness | pass | The transformed fixture supports side-by-side scoring with the same task set and budget. |

## 8. Recommendation

- Keep / revise / rollback / expand: keep
- Immediate next step: add raw logs and repeated runs so the example can support stronger statistical claims
