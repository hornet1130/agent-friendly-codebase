# EVALUATION.md

This file defines the scoring model for comparing a work area's `baseline` and `transformed` states.

## Evaluation goal

Use the same work area and the same task set to measure whether a transformation improved AI-friendliness under fixed conditions.

Use two layers:

1. `Static Readiness Audit`
2. `Dynamic Task Evaluation`

Static audit alone is not enough. Dynamic task performance is required for a full comparison.

## Fixed experimental conditions

Keep these fixed when comparing `baseline` and `transformed`:

- repository base revision, or a clearly comparable baseline
- the same work area
- the same task set
- the same agent or model family
- the same tool permissions
- the same time, token, or cost budget
- the same success oracle

If any of these change, treat the result as a different experiment.

## Score model

The total score is `AIFS`:

`AIFS = ACRS + ATPS`

- `ACRS`: AI Codebase Readiness Score, `0..40`
- `ATPS`: Agent Task Performance Score, `0..60`
- `AIFS`: total score, `0..100`

Interpretation:

- `85..100`: agent-ready
- `70..84`: workable with low to moderate friction
- `50..69`: partially workable, high guidance cost
- `<50`: human-dependent area

## ACRS: static readiness audit

Each readiness category is scored from `0` to `8`.

### S1. Boundary and entrypoints

Evidence to look for:

- the work area boundary is documented
- entrypoints are explicit
- important dependencies and reverse dependencies are visible
- there is a clear starting point for exploration

### S2. Commands and environment

Evidence to look for:

- canonical install, build, test, lint, and dev commands exist
- at least one area-scoped command exists
- common failure causes are documented briefly
- env vars, seeds, fixtures, or setup entrypoints are visible

### S3. Contracts and change surface

Evidence to look for:

- public contracts are visible
- DTOs, schemas, and type boundaries are easy to find
- external integrations are visible
- likely impact radius is predictable

### S4. Context hierarchy and economy

Evidence to look for:

- root guidance and area guidance are separated
- always-loaded instructions are not bloated
- detail is pushed to supporting files
- duplication and conflicts between guidance files are low

### S5. Examples, verification, and persistence

Evidence to look for:

- a canonical or recent example exists
- automated verification exists
- known failures or debug notes are captured
- there is an explicit place to store learned patterns

### ACRS formula

`ACRS = S1 + S2 + S3 + S4 + S5`

## ATPS: dynamic task evaluation

### Task set guidance

Recommended task counts:

- pilot: `8..12`
- formal comparison: `20..40`

Recommended task mix:

- bug fix: `30%..40%`
- feature addition: `20%..30%`
- refactor: `15%..25%`
- test authoring or hardening: `10%..20%`
- repo QA or code understanding: `10%..20%`

Prefer tasks from real issue or PR history whenever possible.

### Required data per task

Each task should capture at least:

- task id
- task type
- problem statement
- area path
- expected relevant files or gold context
- validation command
- success oracle

### Grader choice

Prefer code-based graders for coding work whenever success can be made executable.

- Use code-based grading when tests, builds, or deterministic checks exist.
- Use model-based or human grading only when success cannot be reduced to a reliable executable check.
- Preserve raw logs, transcripts, or equivalent run evidence when available so later comparisons can be audited.

### D1. Resolve rate (`0..20`)

`resolve_rate = resolved_tasks / total_tasks`

`D1 = 20 * resolve_rate`

A task is `resolved` only if it satisfies the success oracle.

### D2. Valid patch rate (`0..10`)

`valid_patch_rate = valid_patches / total_tasks`

`D2 = 10 * valid_patch_rate`

A patch is `valid` if it at least builds or runs the target validation path.

### D3. Regression-free rate (`0..10`)

`regression_free_rate = regression_free_tasks / total_tasks`

`D3 = 10 * regression_free_rate`

### D4. Context efficiency (`0..10`)

Track three normalized values in `0..1`:

- `context_precision`: ratio of read files that were actually relevant
- `context_recall`: ratio of gold relevant files that were actually read
- `first_relevant_hit_rate`: how quickly the first relevant file was reached

Formula:

`D4 = 5 * context_precision + 3 * context_recall + 2 * first_relevant_hit_rate`

### D5. Human dependence (`0..5`)

Track two normalized values in `0..1`:

- `human_intervention_free_rate`
- `review_acceptance_rate`

Formula:

`D5 = 3 * human_intervention_free_rate + 2 * review_acceptance_rate`

### D6. Reuse gain (`0..5`)

Use this only when you have a meaningful sequence of related tasks.

Track:

- `sequence_gain`: normalized improvement in downstream task success
- `cost_reduction_rate`: normalized reduction in downstream time, token, or cost

Formula:

`D6 = 3 * clamp(sequence_gain, 0, 1) + 2 * clamp(cost_reduction_rate, 0, 1)`

If there is no sequence, set `D6 = 0` and say so explicitly.

### ATPS formula

`ATPS = D1 + D2 + D3 + D4 + D5 + D6`

## Audit-only vs full evaluation

Use `audit-only` when dynamic tasks have not been executed yet.

Requirements for an audit-only result:

- report `ACRS`
- mark `ATPS` as incomplete or estimated
- state the missing measurements clearly

Use `full evaluation` only when static and dynamic data are both available.

## Reporting requirements

Every serious result should record:

- `ACRS`, `ATPS`, and `AIFS`
- readiness breakdown
- dynamic breakdown
- task-level pass or fail
- evidence for each score
- time, token, or cost notes when available
- human intervention notes

Comparison reports should include:

- absolute delta: `transformed - baseline`
- relative delta
- strongest improvement areas
- remaining blockers
- recommendation: keep, revise, rollback, or expand

## Recommended statistics

If agent behavior is stochastic, run each task multiple times.

Reasonable defaults:

- binary outcomes: paired bootstrap confidence interval or McNemar
- continuous outcomes such as time or tokens: paired bootstrap or Wilcoxon signed-rank
- report median and spread, not only the mean

If publication-quality rigor matters, preserve per-task raw logs.

## Metrics file format

The score script expects:

- top-level keys: `label`, `readiness`, `dynamic`
- readiness keys:
  - `boundary_entrypoints`
  - `commands_env`
  - `contracts`
  - `context_hierarchy`
  - `examples_persistence`
- dynamic keys:
  - `resolve_rate`
  - `valid_patch_rate`
  - `regression_free_rate`
  - `context_precision`
  - `context_recall`
  - `first_relevant_hit_rate`
  - `human_intervention_free_rate`
  - `review_acceptance_rate`
  - `sequence_gain`
  - `cost_reduction_rate`

See `assets/example_baseline_metrics.json` and `assets/example_transformed_metrics.json` for concrete examples.
