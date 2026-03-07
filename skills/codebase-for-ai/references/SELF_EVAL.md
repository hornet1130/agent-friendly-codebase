# SELF_EVAL.md

Read this file only when you are evaluating or maintaining the `codebase-for-ai` skill package itself.

## Self area boundary

Use `skills/codebase-for-ai/` as the bounded work area.

- primary paths: `SKILL.md`, `references/`, `scripts/`, `agents/openai.yaml`
- key entrypoints: `SKILL.md`, `scripts/smoke_test.sh`, `scripts/self_eval_check.sh`
- important dependencies: `README.md`, Python 3, POSIX shell, grep-based verification commands
- reverse dependencies: `npx skills add ... --skill codebase-for-ai`, local maintenance runs, and any workflow that shells out to `scripts/calculate_score.py`

## Fixed evaluation conditions

Keep these fixed when comparing self-evaluation results across revisions:

- same repository root and packaged skill path
- same task set `SE-001` to `SE-008`
- same helper scripts and validation commands
- same agent family and tool permissions
- same budget assumptions for read/edit/verify work

## Representative self-task set

### SE-001 Packaging layout drift

- Type: repo QA
- Problem statement: keep the published tree and install instructions aligned after packaging changes
- Relevant files: `README.md`, `skills/codebase-for-ai/SKILL.md`, `skills/codebase-for-ai/agents/openai.yaml`
- Validation command: `sh skills/codebase-for-ai/scripts/self_eval_check.sh`
- Success oracle: the install path, packaged tree, and required files still match the documented layout

### SE-002 Smoke validation upkeep

- Type: test hardening
- Problem statement: preserve a deterministic package-level smoke path when helper scripts or score formatting change
- Relevant files: `skills/codebase-for-ai/scripts/smoke_test.sh`, `skills/codebase-for-ai/scripts/calculate_score.py`, `skills/codebase-for-ai/references/MAINTENANCE.md`
- Validation command: `sh skills/codebase-for-ai/scripts/smoke_test.sh`
- Success oracle: the smoke test exits `0` and prints the expected audit-only score lines

### SE-003 Score-schema contract alignment

- Type: contract update
- Problem statement: keep the scoring script and scoring-model reference aligned when evaluation fields change
- Relevant files: `skills/codebase-for-ai/references/EVALUATION.md`, `skills/codebase-for-ai/scripts/calculate_score.py`
- Validation command: `python3 -m py_compile skills/codebase-for-ai/scripts/calculate_score.py`
- Success oracle: the score script remains syntactically valid and the evaluation reference documents the supported schema

### SE-004 Audit-only validation regression

- Type: bug fix
- Problem statement: prevent audit-only payloads from silently accepting `dynamic` data or malformed modes
- Relevant files: `skills/codebase-for-ai/scripts/calculate_score.py`, `skills/codebase-for-ai/references/EVALUATION.md`, `skills/codebase-for-ai/references/MAINTENANCE.md`
- Validation command: `sh skills/codebase-for-ai/scripts/smoke_test.sh`
- Success oracle: valid audit-only inputs still pass and maintenance notes still describe the common failure modes

### SE-005 Maintenance knowledge update

- Type: knowledge persistence
- Problem statement: save recurring packaging and verification gotchas in a stable location instead of chat-only memory
- Relevant files: `skills/codebase-for-ai/references/MAINTENANCE.md`, `skills/codebase-for-ai/SKILL.md`
- Validation command: `sh skills/codebase-for-ai/scripts/self_eval_check.sh`
- Success oracle: `MAINTENANCE.md` remains referenced by `SKILL.md` and contains canonical validation guidance plus failure notes

### SE-006 Persisted artifact contract upkeep

- Type: refactor
- Problem statement: keep the persisted output contract aligned with the bundled templates when artifact paths change
- Relevant files: `skills/codebase-for-ai/SKILL.md`, `skills/codebase-for-ai/assets/TEMPLATES/AREA_PROFILE.md`, `skills/codebase-for-ai/assets/TEMPLATES/TASK.md`, `skills/codebase-for-ai/assets/TEMPLATES/EVALUATION_REPORT.md`
- Validation command: `sh skills/codebase-for-ai/scripts/self_eval_check.sh`
- Success oracle: the documented `AREAS/<area>/...` outputs still exist as bundled templates and remain discoverable from `SKILL.md`

### SE-007 Self-task-set completeness

- Type: evaluation readiness
- Problem statement: preserve a fixed, bounded self-task set so future self-comparisons do not drift
- Relevant files: `skills/codebase-for-ai/references/SELF_EVAL.md`, `skills/codebase-for-ai/scripts/self_eval_check.sh`
- Validation command: `sh skills/codebase-for-ai/scripts/self_eval_check.sh`
- Success oracle: the self-eval reference contains exactly `8` task entries and the helper check enforces that invariant

### SE-008 Agent metadata drift

- Type: packaging
- Problem statement: keep UI-facing metadata and packaged skill naming aligned after renames or scope changes
- Relevant files: `skills/codebase-for-ai/agents/openai.yaml`, `README.md`, `skills/codebase-for-ai/SKILL.md`
- Validation command: `sh skills/codebase-for-ai/scripts/self_eval_check.sh`
- Success oracle: the package name remains `codebase-for-ai` across install docs, metadata, and the skill frontmatter

## Evidence expectations

For full self-evaluation runs, record at least:

- pass or fail for each `SE-001` to `SE-008`
- command output for each validation step
- files read before the first relevant hit
- human interventions needed to finish the task
- whether downstream tasks got cheaper after earlier fixes

## Run file contract

When recording a full self-evaluation run, create a JSON file based on `assets/TEMPLATES/SELF_EVAL_RUN.json`.
Replace every `REPLACE_WITH_...` placeholder before running the builder script.

Required top-level keys:

- `label`
- `readiness`
- `tasks`

Optional top-level keys:

- `sequence_gain`
- `cost_reduction_rate`
- `notes`

Each task entry must include:

- `task_id`
- `task_type`
- `resolved`
- `valid_patch`
- `regression_free`
- `files_read`
- `gold_files`
- `first_relevant_read_index`
- `human_intervention_needed`
- `review_accepted`

Use `first_relevant_read_index = 0` when no relevant file was reached. Otherwise use a `1`-based index into `files_read`.

After filling the run file, convert it to a metrics JSON with:

```bash
python3 skills/codebase-for-ai/scripts/build_self_eval_metrics.py path/to/self-eval-run.json --out path/to/metrics.json
python3 skills/codebase-for-ai/scripts/calculate_score.py path/to/metrics.json
```

## Repeated-run summary

If you run the self-benchmark multiple times under fixed conditions, summarize the runs with:

```bash
python3 skills/codebase-for-ai/scripts/summarize_self_eval_runs.py run-01.json run-02.json run-03.json
```

The summary reports per-run scores plus median, mean, min, and max for `ACRS`, `ATPS`, `AIFS`, and dynamic sub-scores.
