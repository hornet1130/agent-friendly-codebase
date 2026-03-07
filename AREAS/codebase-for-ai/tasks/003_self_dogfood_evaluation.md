# TASK

- Task ID: codebase-for-ai-003
- Area ID: codebase-for-ai
- Type: repo-qa
- Difficulty: medium

## Problem statement

Evaluate this repository with its own method and persist the area profile, representative tasks, metrics, and reports under `AREAS/codebase-for-ai/`.

## Scope

- In scope: self-evaluation artifacts for the root area, audit-only metrics, and comparison notes
- Out of scope: fabricated dynamic benchmark numbers or claims of full evaluation without task-run evidence

## Expected relevant files

- `AREAS/codebase-for-ai/PROFILE.md`
- `AREAS/codebase-for-ai/tasks/*`
- `AREAS/codebase-for-ai/reports/*`

## Validation

- Target command: `python3 skills/codebase-for-ai/scripts/calculate_score.py AREAS/codebase-for-ai/metrics/baseline.json AREAS/codebase-for-ai/metrics/transformed.json`
- Success oracle: the self-evaluation area can be scored and its comparison output matches the persisted reports
- Regression check: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`
- Preferred grader: code-based
- Evidence to capture: score output, persisted reports, and a clear missing-measurements section

## Gold patch or human reference

- PR / commit / diff reference: `AREAS/codebase-for-ai/reports/comparison.md`

## Notes

- Why this task is representative: it forces the skill package to dogfood its own contracts and repository structure
- Why this task is hard for agents: it is easy to overstate confidence or write placeholder artifacts that do not line up with the scoring rules
