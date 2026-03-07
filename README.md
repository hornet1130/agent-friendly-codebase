# CODEBASE_FOR_AI

`CODEBASE_FOR_AI` is a reusable skill package for turning a bounded part of a repository into an AI-friendly work area, then measuring whether the transformation improved real task execution.

This package is intentionally split by responsibility:

- `SKILL.md`: orchestration only
- `RULE.md`: canonical definition of AI-friendly codebase rules
- `EVALUATION.md`: canonical scoring model and experiment rules
- `CHECKLISTS/`: compact execution checklists
- `TEMPLATES/`: files to copy when defining an area and its task set
- `AREAS/`: area-local profiles, tasks, reports, and metrics
- `scripts/`: deterministic helpers for scaffolding areas, scaffolding tasks, and calculating scores

## Why this package exists

Many repositories are workable for humans only because the team already knows where to start, which files matter, which commands are real, and which failures are common.

This package exists to externalize the minimum high-value structure an agent needs to perform representative work repeatedly instead of rediscovering the same context every session.

## Design constraints

This package follows a few deliberate constraints:

- evaluate one bounded work area at a time, not the entire repository at once
- keep `SKILL.md` thin and move detail into rules, metrics, templates, and area-local artifacts
- combine static structure review with dynamic task execution instead of trusting either one alone
- prefer small load-bearing artifacts such as profiles, commands, examples, tests, and known-failure notes
- reject documentation sprawl as a goal

## Install location

Place the package where your agent can discover it.

For Claude Code:

- `.claude/skills/CODEBASE_FOR_AI/`
- `apps/web/.claude/skills/CODEBASE_FOR_AI/`
- `apps/api/.claude/skills/CODEBASE_FOR_AI/`

For Codex-family agents:

- `.agents/skills/CODEBASE_FOR_AI/`
- `apps/web/.agents/skills/CODEBASE_FOR_AI/`
- `apps/api/.agents/skills/CODEBASE_FOR_AI/`

In a monorepo, the most practical setup is a root-level shared skill plus area-local supporting material near the code being transformed.

## How to use it in another codebase

This package is meant to be copied into a target repository and then used manually by the agent on demand.

Recommended flow:

1. Pick a bounded work area such as `apps/api/src/modules/auth`.
2. Create `AREAS/<area>/PROFILE.md` from `TEMPLATES/AREA_PROFILE.md`.
3. Create representative tasks in `AREAS/<area>/tasks/` from `TEMPLATES/TASK.md`.
4. Score the current state as `baseline` using `RULE.md` and `EVALUATION.md`.
5. Apply the smallest useful transformation: commands, examples, tests, area-local guidance, or structure fixes.
6. Re-score the same area with the same task set as `transformed`.
7. Compare the two states with the same agent family, permissions, and budget.

The point is not to "install and forget" the skill. The point is to use it as a repeatable method for a specific area.

## Minimum useful artifacts

For one serious area comparison, keep at least:

- `AREAS/<area>/PROFILE.md`
- `AREAS/<area>/tasks/*.md`
- `AREAS/<area>/reports/baseline.md`
- `AREAS/<area>/reports/transformed.md`
- `AREAS/<area>/metrics/baseline.json`
- `AREAS/<area>/metrics/transformed.json`

## Automation helpers

This package now includes a small deterministic scaffolding layer.

Initialize a work area:

```bash
python scripts/init_area.py \
  --area-id auth-api \
  --human-name "Authentication API module" \
  --primary-path apps/api/src/modules/auth
```

Create a task file:

```bash
python scripts/init_task.py \
  --area-id auth-api \
  --task-id auth-api-001 \
  --slug bug_login_refresh \
  --type bug-fix \
  --difficulty medium
```

Write evaluation output to files:

```bash
python scripts/calculate_score.py \
  AREAS/auth-api/metrics/baseline.json \
  --json-out AREAS/auth-api/reports/baseline-score.json \
  --md-out AREAS/auth-api/reports/baseline-score.md
```

Write comparison output to files:

```bash
python scripts/calculate_score.py \
  AREAS/auth-api/metrics/baseline.json \
  AREAS/auth-api/metrics/transformed.json \
  --json-out AREAS/auth-api/reports/comparison.json \
  --md-out AREAS/auth-api/reports/comparison.md
```

## Manual prompts

Use prompts like these after copying the skill into the target repository.

Transformation prompt:

> Use `CODEBASE_FOR_AI` to define `apps/api/src/modules/auth` as a work area, score its baseline, apply the smallest changes that improve AI-friendliness, and summarize the changes as a rule-mapping table.

Evaluation prompt:

> Use `CODEBASE_FOR_AI` to evaluate `apps/web/src/features/checkout`. Compute the baseline score and task performance, and compare it with the most recent transformed report if it exists.

Comparison prompt:

> Use `CODEBASE_FOR_AI` to compare baseline vs transformed results for `orders-api`. Report total score, resolve rate, regression-free rate, context efficiency, and human dependence.

End-to-end pipeline prompt:

> Use `CODEBASE_FOR_AI` to run the full pipeline for `apps/api/src/modules/auth`: define the work area, write baseline artifacts under `AREAS/auth-api/`, evaluate baseline, apply the smallest safe transformation, evaluate the transformed state, and write the comparison report under `AREAS/auth-api/reports/comparison.md`.

## What "AI-friendly" means here

This package does not define AI-friendliness as "more docs" or "clean code" in the abstract.

A work area is AI-friendly when, under the same model, tools, and budget:

- the agent can find the right starting point quickly
- the important contracts are visible
- build, test, and validation commands are reproducible
- representative changes stay localized
- the agent can verify its own changes
- successful patterns are reusable in later tasks

`RULE.md` contains the canonical rules. `EVALUATION.md` turns those rules into a measurable score.

## What this package does not claim

- More documentation does not automatically mean more AI-friendliness.
- Clean code alone does not automatically mean high agent performance.
- This package does not replace architecture work, testing strategy, or operational discipline.
- This package cannot create autonomy where validation paths and safe tooling do not exist.

## Possible extensions

- Add trace collection for context-efficiency metrics instead of estimating them manually.
- Add benchmark runners that execute task sets under fixed budgets and capture logs automatically.
- Add a patch-quality rubric beyond pass or fail, such as unnecessary diff size or architectural drift.
- Add stronger observability checks for logs, metrics, and debug entrypoints.
- Add domain-specific variants for frontend apps, backend services, data pipelines, and libraries.
- Add a consistent area-memory pattern for storing post-task learnings.

## Safe transformation protocol

The package can support a very cautious transformation process, but it cannot guarantee safety without trustworthy validation.

Use these defaults:

- record the baseline proof commands before changing code
- keep the success oracle fixed across baseline and transformed runs
- prefer the smallest diff that closes the target rule gaps
- run area-scoped proof before broader regression checks
- do not claim safety if validation is missing, flaky, or incomplete

See `CHECKLISTS/SAFE_TRANSFORM.md` for the transformation safety checklist.
