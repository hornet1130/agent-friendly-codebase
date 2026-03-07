# COMPARISON REPORT

This bundled example comparison is derived from `AREAS/example-auth-api/metrics/baseline.json` and `AREAS/example-auth-api/metrics/transformed.json`.

## 1. Score summary

| Metric | Baseline | Transformed | Delta | Relative delta |
|---|---:|---:|---:|---:|
| ACRS | 22.00 | 34.00 | +12.00 | +54.55% |
| ATPS | 28.70 | 42.15 | +13.45 | +46.86% |
| **AIFS** | **50.70** | **76.15** | **+25.45** | **+50.20%** |

## 2. Strongest improvement areas

- Commands and environment moved from 4 to 7, removing a major source of agent hesitation.
- Examples, verification, and persistence moved from 4 to 7, which correlates with higher resolve and regression-free rates.
- Context efficiency improved from 5.39 to 7.06, suggesting the transformed state reduces exploration waste.

## 3. Remaining blockers

- The bundled example still lacks raw logs, repeated runs, and confidence intervals.
- Observability evidence remains weaker than the scoring model ideally expects.
- Some top-level methodological guidance is still duplicated across root docs.

## 4. Recommendation

- Recommendation: keep and expand
- Why: the transformed fixture crosses from `partially workable, high guidance cost` to `workable with low to moderate friction` without changing the scoring model
- Next step: pair the example metrics with real task transcripts so the package demonstrates a complete audited comparison, not only the reporting shape
