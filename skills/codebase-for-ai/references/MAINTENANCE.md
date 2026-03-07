# MAINTENANCE.md

Read this file only when you are validating, publishing, or debugging the `codebase-for-ai` skill package itself.

## Skill-package boundary

Treat `skills/codebase-for-ai/` as the bounded work area when maintaining this skill itself.

- primary paths: `SKILL.md`, `references/`, `scripts/`, `agents/openai.yaml`
- entrypoints: `SKILL.md`, `scripts/smoke_test.sh`, `scripts/self_eval_check.sh`
- important dependencies: `README.md`, Python 3, POSIX shell, grep-based validation commands
- reverse dependencies: the root install command, packaged skill loading via `--skill codebase-for-ai`, and any automation that relies on `scripts/calculate_score.py`

## Command matrix

Run commands from the repository root.

| Need | Command | When to use it |
|---|---|---|
| install | `N/A` | This package ships plain files and helper scripts. No package install step is required beyond having `python3` and `sh`. |
| build | `python3 -m py_compile skills/codebase-for-ai/scripts/calculate_score.py skills/codebase-for-ai/scripts/build_self_eval_metrics.py` | Fast syntax proof after script edits. |
| test | `sh skills/codebase-for-ai/scripts/smoke_test.sh` | Fastest trusted area-scoped proof for score formatting and audit-only validation. |
| lint | `N/A` | No dedicated linter is bundled. Use `py_compile` plus the shell checks as the canonical validation path. |
| dev | `N/A` | This skill package has no long-running dev server. |
| regression | `sh skills/codebase-for-ai/scripts/self_eval_check.sh` | Broader package regression after docs, metadata, templates, or helper changes. |

Use the `test` row before the `regression` row when both apply.

## Contract surface map

Treat these files as the source of truth for the package contracts.

| Contract surface | Source of truth | Checked by |
|---|---|---|
| score model and formulas | `references/EVALUATION.md`, `scripts/calculate_score.py` | `python3 -m py_compile ...`, `sh scripts/smoke_test.sh` |
| self-eval task set and run evidence contract | `references/SELF_EVAL.md`, `assets/TEMPLATES/SELF_EVAL_RUN.json`, `scripts/build_self_eval_metrics.py` | `sh scripts/self_eval_check.sh` |
| persisted artifact paths | `SKILL.md`, `assets/TEMPLATES/AREA_PROFILE.md`, `assets/TEMPLATES/TASK.md`, `assets/TEMPLATES/EVALUATION_REPORT.md` | `sh scripts/self_eval_check.sh` |
| package identity and install surface | `README.md`, `SKILL.md`, `agents/openai.yaml` | `sh scripts/self_eval_check.sh` |

## Canonical smoke test

Run these commands from the repository root:

```bash
python3 -m py_compile skills/codebase-for-ai/scripts/calculate_score.py
python3 -m py_compile skills/codebase-for-ai/scripts/build_self_eval_metrics.py
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
python3 -m py_compile skills/codebase-for-ai/scripts/build_self_eval_metrics.py
sh skills/codebase-for-ai/scripts/smoke_test.sh
sh skills/codebase-for-ai/scripts/self_eval_check.sh
```

Expected result:

- the smoke test passes
- the self-eval check reports `8` task specs
- `README.md`, `SKILL.md`, `SELF_EVAL.md`, and `agents/openai.yaml` stay aligned

## Dynamic self-benchmark workflow

When you have task-level self-eval evidence:

1. Start from `skills/codebase-for-ai/assets/TEMPLATES/SELF_EVAL_RUN.json`.
2. Fill the task outcomes and context traces for `SE-001` through `SE-008`.
3. Convert that run file into score-script metrics:

```bash
python3 skills/codebase-for-ai/scripts/build_self_eval_metrics.py path/to/self-eval-run.json --out path/to/metrics.json
python3 skills/codebase-for-ai/scripts/calculate_score.py path/to/metrics.json
```

The builder script validates the run file before emitting metrics. Do not claim `ATPS` unless this path succeeds on a completed run file.
Raw template placeholders are rejected on purpose.

For repeated runs under fixed conditions, summarize them with:

```bash
python3 skills/codebase-for-ai/scripts/summarize_self_eval_runs.py run-01.json run-02.json run-03.json
```

Prefer reporting median and spread from repeated runs over a single lucky run.

## Exploration starting points

Use these first when the task is obvious:

- score output or scoring drift: `scripts/calculate_score.py`
- run-file schema or derived metrics drift: `scripts/build_self_eval_metrics.py`
- package layout or metadata drift: `README.md`, `SKILL.md`, `agents/openai.yaml`
- validation-path drift: `scripts/smoke_test.sh`, `scripts/self_eval_check.sh`
- task-set drift: `references/SELF_EVAL.md`

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
- `duplicate or unexpected task ids in self-eval run`
  The run file drifted from the fixed `SE-001` to `SE-008` task set.
- `first_relevant_read_index must be 0 or within the files_read range`
  The context trace is malformed.
- `self-eval run still contains template placeholder values`
  The run file was copied from the template but not filled with real evidence yet.
- `at least one self-eval run json path is required`
  The summary script was called without any completed run files.

## Knowledge persistence

When recurring maintenance knowledge is discovered:

- record packaging, validation, and publish gotchas here
- update `references/EVALUATION.md` only for scoring-model changes
- update `SKILL.md` only for workflow changes
