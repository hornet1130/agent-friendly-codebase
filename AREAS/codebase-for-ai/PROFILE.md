# AREA PROFILE

## 1. Identity

- Area ID: codebase-for-ai
- Human name: codebase-for-ai skill package
- Primary paths: `SKILL.md`, `RULE.md`, `EVALUATION.md`, `scripts/`, `TEMPLATES/`, `AREAS/example-auth-api/`
- Non-goals / out of scope: downstream target repositories that copy this package, unrelated agent skills outside this repository

## 2. Why this area matters

- Business purpose: define, transform, evaluate, and compare AI-friendly work areas inside other repositories
- Typical requests received in this area: score a bounded area, scaffold area artifacts, update scoring rules, add reusable examples, harden helper scripts
- Why this area is a good benchmark target: it mixes prompt-layer contracts, deterministic helper scripts, templates, and example evaluation artifacts in one bounded package

## 3. Entrypoints

- User entrypoints: `SKILL.md`
- HTTP/API entrypoints: none
- Job/queue entrypoints: none
- UI route/page entrypoints: none
- CLI/script entrypoints: `scripts/calculate_score.py`, `scripts/init_area.py`, `scripts/init_task.py`

## 4. Dependency map

- Primary dependencies: Python 3 standard library, filesystem writes under `AREAS/`, the metrics schema defined in `EVALUATION.md`
- Reverse dependencies: agent sessions that invoke the skill, repositories that copy this package, the bundled example area and reports
- Shared packages / infrastructure touched: none beyond local filesystem and shell execution

## 5. Key contracts

- Public API / route: the score calculator CLI inputs and outputs, the area scaffold layout, and the output contract in `SKILL.md`
- DTO / schema / zod / class-validator: metrics JSON schema in `EVALUATION.md`, evaluation report template, task template, and area profile template
- Shared package contracts: `AREAS/<area>/PROFILE.md`, `AREAS/<area>/tasks/*.md`, `AREAS/<area>/reports/*.md`, `AREAS/<area>/metrics/*.json`
- External services: none required
- Required env vars: none; Python 3 is the only runtime dependency

## 6. Canonical commands

- install: `python3 --version`
- build: `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile scripts/*.py tests/*.py`
- lint: `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile scripts/*.py tests/*.py`
- test: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`
- test (area-only): `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`
- dev: `python3 scripts/calculate_score.py assets/example_audit_only_metrics.json`
- e2e: `python3 scripts/calculate_score.py AREAS/example-auth-api/metrics/baseline.json AREAS/example-auth-api/metrics/transformed.json`

## 7. Typical change types

- Bug fix: correct score math, validation behavior, or scaffolded output
- Feature add: support a new evaluation mode, output format, or helper script
- Refactor: split shared helper logic without changing CLI behavior
- Validation / schema change: adjust metrics JSON, report templates, or required evidence
- Test hardening: add deterministic CLI coverage and repository smoke checks

## 8. Common files touched

- Hot files: `SKILL.md`, `EVALUATION.md`, `README.md`, `scripts/calculate_score.py`, `scripts/init_area.py`
- Supporting files: `TEMPLATES/*`, `AREAS/example-auth-api/*`, `tests/test_cli_scripts.py`
- Dangerous shared files: `RULE.md`, `EVALUATION.md`, and templates consumed by every generated area

## 9. Exploration hints

- Fastest starting files: `SKILL.md`, `EVALUATION.md`, `README.md`, `tests/test_cli_scripts.py`
- High-signal symbols / grep seeds: `evaluation_mode`, `missing_measurements`, `AIFS`, `ACRS`, `ATPS`, `metrics_stub`
- Directory focus order: `scripts/` -> `tests/` -> `TEMPLATES/` -> `AREAS/example-auth-api/`

## 10. Verification

- Fastest proof command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`
- Full proof command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`
- Known flaky tests: none documented
- Manual checks still required: read generated markdown reports to confirm the narrative matches the numeric score output

## 11. Known failure patterns

- audit-only metrics accidentally treated as zero-valued dynamic scores
- example reports drifting away from the metrics fixtures they claim to summarize
- generated Python bytecode dirtying the repository and obscuring real changes

## 12. Golden path examples

- Example PR / commit / file path 1: `AREAS/example-auth-api/reports/comparison.md`
- Example PR / commit / file path 2: `tests/test_cli_scripts.py`

## 13. Current AI-readiness gaps

- the repository still lacks a full dynamic task benchmark for the self-evaluation area
- score narratives are stored, but raw transcripts and confidence intervals are not bundled
- root methodology remains split across several top-level docs and could be condensed further later
