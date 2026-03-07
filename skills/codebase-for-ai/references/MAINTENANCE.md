# MAINTENANCE.md

Read this file only when you are validating, publishing, or debugging the `codebase-for-ai` skill package itself.

## Skill-package boundary

Treat `skills/codebase-for-ai/` as the bounded work area when maintaining this skill itself.

- primary paths: `SKILL.md`, `references/`, `scripts/`, `agents/openai.yaml`
- entrypoints: `SKILL.md`, `scripts/smoke_test.sh`, `scripts/self_eval_check.sh`
- important dependencies: `README.md`, Python 3, POSIX shell, grep-based validation commands
- reverse dependencies: the root install command, packaged skill loading via `--skill codebase-for-ai`, and any automation that relies on `scripts/calculate_score.py`

## Canonical smoke test

Run these commands from the repository root:

```bash
python3 -m py_compile skills/codebase-for-ai/scripts/calculate_score.py
sh skills/codebase-for-ai/scripts/smoke_test.sh
```

Expected result:

- the score script compiles
- the smoke test prints an `audit-only` report
- the report contains `ACRS: 28/40`
- `ATPS` and `AIFS` are both `incomplete`

## Full package validation

Run these commands from the repository root:

```bash
python3 -m py_compile skills/codebase-for-ai/scripts/calculate_score.py
sh skills/codebase-for-ai/scripts/smoke_test.sh
sh skills/codebase-for-ai/scripts/self_eval_check.sh
```

Expected result:

- the smoke test passes
- the self-eval check reports `8` task specs
- `README.md`, `SKILL.md`, `SELF_EVAL.md`, and `agents/openai.yaml` stay aligned

## Worked example

The bundled smoke test creates this minimal audit-only input:

```json
{
  "label": "smoke-test",
  "evaluation_mode": "audit-only",
  "readiness": {
    "boundary_entrypoints": 6,
    "commands_env": 5,
    "contracts": 6,
    "context_hierarchy": 5,
    "examples_persistence": 6
  },
  "missing_measurements": [
    "representative dynamic task set",
    "task-level success oracle logs"
  ]
}
```

This is the canonical example for verifying that packaging and audit-only scoring still work after edits.

## Common failure modes

- `python3: command not found`
  Install Python 3 or do not claim the helper scripts are verified.
- `evaluation_mode must be 'full' or 'audit-only'`
  The metrics file is malformed.
- `audit-only metrics must omit 'dynamic' or set it to null`
  The metrics payload mixes audit-only and full-evaluation fields.
- `full evaluation metrics require a 'dynamic' object`
  A full-evaluation payload is missing required dynamic measurements.
- `expected 8 self-eval tasks, found N`
  `references/SELF_EVAL.md` drifted or a task heading was renamed.
- `self-eval check references missing file`
  A packaged file moved without updating `scripts/self_eval_check.sh`.

## Knowledge persistence

When recurring maintenance knowledge is discovered:

- record packaging, validation, and publish gotchas here
- update `references/EVALUATION.md` only for scoring-model changes
- update `SKILL.md` only for workflow changes
