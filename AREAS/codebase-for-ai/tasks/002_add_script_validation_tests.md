# TASK

- Task ID: codebase-for-ai-002
- Area ID: codebase-for-ai
- Type: test
- Difficulty: medium

## Problem statement

Add deterministic tests that cover the score calculator and scaffold CLIs so quality improvements can be verified without manual smoke runs only.

## Scope

- In scope: Python stdlib test coverage for CLI behavior, temporary fixture setup, and README command updates
- Out of scope: external test frameworks or snapshot tooling

## Expected relevant files

- `tests/test_cli_scripts.py`
- `README.md`
- `skills/codebase-for-ai/scripts/calculate_score.py`

## Validation

- Target command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`
- Success oracle: the test suite passes from a clean checkout and exercises audit-only output plus scaffold generation
- Regression check: `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile skills/codebase-for-ai/scripts/*.py tests/*.py`
- Preferred grader: code-based
- Evidence to capture: passing unittest output and generated fixture assertions

## Gold patch or human reference

- PR / commit / diff reference: `tests/test_cli_scripts.py`

## Notes

- Why this task is representative: helper scripts are the most failure-prone executable surface in this repository
- Why this task is hard for agents: the CLIs write into repo-local paths and must be tested without polluting the working tree
