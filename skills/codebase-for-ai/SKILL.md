---
name: codebase-for-ai
description: Transform and quantitatively evaluate a bounded repository work area for AI-agent friendliness. Use when the task is to define a work area, audit it against AI-friendly codebase rules, create or improve area-specific context and workflow artifacts, or compare baseline vs transformed performance on the same task set. Do not use for unrelated feature work outside codebase-for-AI transformation or for vague repository-wide refactors without a scoped target area.
disable-model-invocation: true
---

# Purpose

Use this skill on a **bounded work area** to do one of four things:

1. `define`
2. `transform`
3. `evaluate`
4. `compare`

Keep this file thin. Read the rules, score model, relevant checklist, and any area-local artifacts. Read templates only when the user asked to persist files.

## Work area

A work area is a bounded unit of work defined by:

- primary code paths
- entrypoints
- public contracts
- commands used to build, run, and validate it
- typical change types
- representative tasks

If the user names only a path, infer the smallest reasonable work area around it.

## Inputs

Infer these unless asking is necessary:

- target area identifier or path
- goal: `define`, `transform`, `evaluate`, or `compare`
- state under test: `baseline`, `transformed`, or both
- persistence target: default to chat-only

## Read path

Read in this order:

1. `references/RULE.md`
2. `references/EVALUATION.md`
3. the relevant checklist under `references/CHECKLISTS/`
4. `AREAS/<area>/PROFILE.md` if present
5. existing tasks, reports, and metrics for that area

If the repository stack is obvious, read only the smallest matching overlay:

- `references/node-monorepo.md`
- `references/go-service.md`
- `references/python-service.md`

Read `references/MAINTENANCE.md` only for packaging, smoke-test, or score-script maintenance on this skill itself.
Read `references/SELF_EVAL.md` only when evaluating or maintaining `codebase-for-ai` itself.

## Output contract

### `define`

Produce:

- area boundary summary
- dependency map and likely blast radius
- key entrypoints and contracts
- search starting points
- canonical commands
- missing-information list
- proposed task set outline

### `transform`

Produce:

- baseline gap table against `references/RULE.md`
- smallest changes that improve the target rules
- artifact plan for docs, scripts, examples, tests, or scoped instructions
- changed or proposed file list
- validation plan and remaining risks
- post-change evaluation plan

Prefer minimal, load-bearing artifacts over documentation bulk.

### `evaluate`

Produce numeric results, not prose only:

- readiness score breakdown
- dynamic task score breakdown
- total score
- grader approach and evidence locations
- supporting evidence per metric
- confidence and measurement gaps

### `compare`

Produce:

- side-by-side score table
- absolute delta
- relative delta
- strongest improvements
- remaining blockers
- recommendation: keep, revise, rollback, or expand

## Workflow

If the user asks for the full pipeline, run:

1. `define`
2. baseline `evaluate`
3. `transform`
4. transformed `evaluate`
5. `compare`

For transformations:

1. bound the area
2. map entrypoints, contracts, commands, and tests
3. record the baseline proof commands
4. score the baseline
5. apply or propose the smallest high-value changes
6. re-run area proof first, then broader checks
7. re-run the same evaluation logic
8. compare baseline and transformed states under the same conditions

## Persisted outputs

Only write files when the user asks. Default paths:

- `AREAS/<area>/PROFILE.md`
- `AREAS/<area>/tasks/*.md`
- `AREAS/<area>/reports/baseline.md`
- `AREAS/<area>/reports/transformed.md`
- `AREAS/<area>/reports/comparison.md`
- `AREAS/<area>/metrics/baseline.json`
- `AREAS/<area>/metrics/transformed.json`

## Helpers

This skill bundles:

- `scripts/smoke_test.sh`
- `scripts/self_eval_check.sh`
- `scripts/build_self_eval_metrics.py`
- `scripts/summarize_self_eval_runs.py`
- `scripts/calculate_score.py`

Packaging and validation details live in `references/MAINTENANCE.md`.

## Guardrails

- Do not treat more documentation as improvement by default.
- Keep always-loaded guidance short and push detail into supporting files.
- Prefer area-scoped guidance over repo-wide blanket rules.
- Prefer executable verification over narrative claims.
- Prefer representative tasks from real work history over toy tasks.
- Never compare runs that changed task set, budget, tools, or scaffolding.
- Never claim a transformation is safe unless the named proof path and regression checks were run, or you state that safety is unproven.

## Maintenance notes

When maintaining this skill itself:

- keep packaging and verification notes in `references/MAINTENANCE.md`
- keep the fixed self-task set in `references/SELF_EVAL.md`
- keep scoring-model changes in `references/EVALUATION.md`
- keep workflow changes in `SKILL.md`

Use compact headings and separate facts, scores, decisions, and unknowns.
Mark partial evidence as estimated or missing.
