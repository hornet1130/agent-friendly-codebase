# TASK

- Task ID: codebase-for-ai-001
- Area ID: codebase-for-ai
- Type: bug-fix
- Difficulty: medium

## Problem statement

Audit-only evaluations should report `ATPS` and `AIFS` as incomplete instead of silently treating missing dynamic measurements as zero.

## Scope

- In scope: metrics validation, score rendering, scaffold defaults, and report templates
- Out of scope: new benchmark runners or non-Python implementations

## Expected relevant files

- `skills/codebase-for-ai/scripts/calculate_score.py`
- `skills/codebase-for-ai/scripts/init_area.py`
- `skills/codebase-for-ai/references/EVALUATION.md`

## Validation

- Target command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`
- Success oracle: audit-only fixtures print and render `ATPS` and `AIFS` as incomplete while full fixtures still score normally
- Regression check: `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile skills/codebase-for-ai/scripts/*.py tests/*.py`
- Preferred grader: code-based
- Evidence to capture: unittest output, example score output, changed fixtures and templates

## Gold patch or human reference

- PR / commit / diff reference: `9345e59` and follow-up self-evaluation artifacts

## Notes

- Why this task is representative: it changes the core contract between the score schema, CLI output, and generated area scaffolds
- Why this task is hard for agents: schema, docs, helper scripts, and examples must all stay in sync
