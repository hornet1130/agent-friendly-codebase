---
name: codebase-for-ai
description: Review and transform a bounded repository work area so AI agents can find the right files faster, make smaller safer changes, and verify the result with less human help. Use when the task is to inspect an area for AI-friction or improve it with a proof-oriented before/after workflow.
disable-model-invocation: true
---

# Purpose

Use this skill on a **bounded work area** in one of two modes:

1. `review`
2. `transform`

Keep this file thin. Read the rules, the default scoring path, the relevant checklist, and any area-local artifacts. Read templates only when the user asked to persist files.

## Work area

A work area is a bounded unit of work defined by:

- primary code paths
- entrypoints
- public contracts
- commands used to build, run, and validate it
- typical change types

If the user names only a path, infer the smallest reasonable work area around it.

## Inputs

Infer these unless asking is necessary:

- target area identifier or path
- goal: `review` or `transform`
- proof command or trusted validation path
- persistence target: default to chat-only

## Read path

Read in this order:

1. `references/RULE.md`
2. `references/EVALUATION.md` through the default workflow sections
3. the relevant checklist under `references/CHECKLISTS/`
4. `AREAS/<area>/PROFILE.md` if present
5. existing profiles, reports, and metrics for that area

If the repository stack is obvious, read only the smallest matching overlay:

- `references/node-monorepo.md`
- `references/go-service.md`
- `references/python-service.md`

Read `references/MAINTENANCE.md` only for packaging, smoke-test, or score-script maintenance on this skill itself.

## Output contract

### `review`

Produce:

- area boundary summary
- key entrypoints, contracts, and search starting points
- canonical command and proof path summary
- readiness snapshot score
- top AI-friction gaps
- smallest useful next improvements

The default `review` result is a lightweight before snapshot.

### `transform`

Produce:

- the scoped area and agreed proof path
- a before snapshot, unless a still-valid review result can be reused
- the smallest changes that improve the target area
- proof results
- an after snapshot
- before vs after delta
- remaining risks

Prefer the smallest high-value diff over broad cleanups.

## Workflow

### `review`

1. bound the area
2. map entrypoints, contracts, and commands
3. score the current readiness snapshot
4. report the biggest gaps and next actions

### `transform`

1. confirm the area, goal, and proof path
2. reuse a recent valid review when possible, otherwise create a before snapshot
3. apply the smallest useful changes
4. run the proof path
5. create an after snapshot
6. report the delta and remaining risks

## Persisted outputs

Only write files when the user asks. Default paths:

- `AREAS/<area>/PROFILE.md`
- `AREAS/<area>/reports/review.md`
- `AREAS/<area>/reports/before.md`
- `AREAS/<area>/reports/after.md`
- `AREAS/<area>/metrics/review.json`
- `AREAS/<area>/metrics/before.json`
- `AREAS/<area>/metrics/after.json`

## Guardrails

- Do not treat more documentation as improvement by default.
- Keep always-loaded guidance short and push detail into supporting files.
- Prefer area-scoped guidance over repo-wide blanket rules.
- Prefer executable verification over narrative claims.
- Never claim a transformation is safe unless the named proof path and regression checks were run, or you state that safety is unproven.

## Maintenance notes

When maintaining this skill itself:

- use the helper scripts documented in `references/MAINTENANCE.md`
- keep packaging and verification notes in `references/MAINTENANCE.md`
- keep scoring-model changes in `references/EVALUATION.md`
- keep workflow changes in `SKILL.md`

Use compact headings and separate facts, scores, decisions, and unknowns.
Mark partial evidence as estimated or missing.
