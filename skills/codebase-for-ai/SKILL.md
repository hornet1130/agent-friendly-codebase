---
name: codebase-for-ai
description: Transform and quantitatively evaluate a bounded repository work area for AI-agent friendliness. Use when the task is to define a work area, audit it against AI-friendly codebase rules, create or improve area-specific context and workflow artifacts, or compare baseline vs transformed performance on the same task set. Do not use for unrelated feature work outside codebase-for-AI transformation or for vague repository-wide refactors without a scoped target area.
disable-model-invocation: true
---

# Purpose

Use this skill to do one of four things for a **bounded work area** inside a repository.

1. **Define** the work area.
2. **Transform** the work area to be more AI-agent friendly.
3. **Evaluate** the work area quantitatively.
4. **Compare** baseline and transformed states.

This skill is intentionally thin. It should orchestrate work by reading `references/RULE.md`, `references/EVALUATION.md`, the relevant checklist under `references/CHECKLISTS/`, the templates under `assets/TEMPLATES/`, and any area-specific profile files in the target repository. Do not duplicate long rules here.

If the repository stack is clear, read the smallest relevant stack overlay:

- `references/node-monorepo.md`
- `references/go-service.md`
- `references/python-service.md`

Do not read all overlays by default. Pick only the one that matches the target area.

# Core definitions

A **work area** is not just a folder. It is a bounded unit of work defined by:

- primary code paths
- entrypoints
- public contracts
- commands used to build/test/run it
- typical change types
- representative task set

If the user names only a path, infer the smallest reasonable work area around that path.

# Required inputs

Try to infer these from the prompt or repository. Ask only when necessary.

- target area identifier or path
- goal: `define`, `transform`, `evaluate`, or `compare`
- state under test: `baseline`, `transformed`, or both
- persistence target: chat-only or write files under `AREAS/<area>/...`

# Always read in this order

1. `references/RULE.md`
2. `references/EVALUATION.md`
3. `references/CHECKLISTS/WORK.md`, `references/CHECKLISTS/SAFE_TRANSFORM.md`, or `references/CHECKLISTS/EVALUATION.md` as applicable
4. `AREAS/<area>/PROFILE.md` if present
5. existing task files and previous reports for the same area

# Output contract

## When goal = define

Produce:

- area boundary summary
- dependency map and likely blast radius
- key entrypoints and contracts
- search starting points for future runs
- canonical commands
- initial missing-information list
- proposed task set outline

## When goal = transform

Produce:

- baseline gap table against `references/RULE.md`
- minimal set of changes needed to satisfy the rules
- artifact plan: docs, scripts, examples, tests, scoped instructions
- changed or proposed file list
- validation plan and remaining-risk summary
- post-change evaluation plan

Prefer **minimal, load-bearing artifacts** over broad documentation dumps.

## When goal = evaluate

Produce:

- readiness score breakdown
- dynamic task score breakdown
- total score
- grader approach and evidence locations
- supporting evidence per metric
- confidence and known measurement gaps

Do not output only prose. Always output numeric results.

## When goal = compare

Produce:

- side-by-side score table
- absolute delta
- relative delta
- strongest improvement areas
- remaining blockers
- recommendation: keep / revise / rollback / expand

# Full pipeline mode

If the user asks for the full pipeline, run these stages in order:

1. `define`
2. `evaluate` the baseline state
3. `transform` with safety gates
4. `evaluate` the transformed state
5. `compare`

If the user asks for persisted outputs, write them under:

- `AREAS/<area>/PROFILE.md`
- `AREAS/<area>/tasks/*.md`
- `AREAS/<area>/reports/baseline.md`
- `AREAS/<area>/reports/transformed.md`
- `AREAS/<area>/reports/comparison.md`
- `AREAS/<area>/metrics/baseline.json`
- `AREAS/<area>/metrics/transformed.json`

# Transformation workflow

1. Bound the work area.
2. Map entrypoints, contracts, commands, and tests.
3. Capture the trusted baseline proof commands.
4. Score the baseline using `references/EVALUATION.md`.
5. Identify the smallest set of artifacts or codebase changes that improve the score.
6. Apply or propose those changes.
7. Re-run area-scoped proof first, then broader regression checks.
8. Re-run the same evaluation logic.
9. Compare baseline vs transformed using the same task set and same conditions.

# Installed helper scripts

This skill bundles deterministic helper scripts under `scripts/`.

- `scripts/init_area.py`
- `scripts/init_task.py`
- `scripts/calculate_score.py`

When invoked from an installed skill, `init_area.py` and `init_task.py` should write into the current working directory by default, or into an explicit `--repo-root`. Do not assume the skill files live inside the target repository.

# Evaluation workflow

Use two layers.

1. **Static readiness audit**: structure, commands, contracts, docs, examples.
2. **Dynamic task evaluation**: actual representative tasks executed under fixed conditions.

If dynamic tasks are missing, explicitly say the evaluation is **audit-only** and incomplete.

# Guardrails

- Do not treat “more documentation” as improvement by default.
- Keep always-loaded instructions short; move detail into supporting files.
- Prefer area-scoped guidance over repo-wide blanket rules.
- Prefer executable verification over narrative claims.
- Prefer representative tasks from real work history over synthetic toy tasks.
- Never compare baseline and transformed states with different task sets, different budgets, or different agent scaffolds.
- Never claim the transformation is safe unless the named proof path and regression checks were actually run, or you clearly state that safety is unproven.

# Expected repository artifacts

Recommended structure:

- `AREAS/<area>/PROFILE.md`
- `AREAS/<area>/tasks/*.md`
- `AREAS/<area>/reports/*.md`
- `AREAS/<area>/metrics/*.json`
- optional area-local docs/examples/tests/scripts

# Report style

Use compact headings and tables when useful. Separate:

- facts
- scores
- decisions
- unknowns

When evidence is partial, mark the metric as estimated or missing rather than pretending it was measured.
