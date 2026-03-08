# Python Service Reference

Use this reference when the target area belongs to a Python service, library, or backend application.

## Good fit signals

- `pyproject.toml`, `requirements.txt`, or `poetry.lock`
- package roots such as `src/`, `app/`, or service-local modules
- tests run with `pytest`
- contracts expressed through pydantic models, serializers, schemas, or dataclasses

## Work-area heuristics

- Prefer one feature module, API slice, or library package.
- Identify app entrypoints and route registration early.
- Separate domain logic from framework wiring in the profile.

Good examples:

- `app/auth`
- `src/payments`
- `package/http_client`

## Common contract surfaces

- route handlers, views, routers
- pydantic models, serializers, marshmallow schemas
- service interfaces and repository abstractions
- settings objects and env parsing
- task queue entrypoints when applicable

## Common command patterns

- install: repo-specific, such as `pip install -r requirements.txt` or `poetry install`
- test: `pytest`
- area-local test: `pytest tests/auth -q`
- lint: project-specific, often `ruff check .` or `flake8`
- type check: project-specific, often `mypy`

## Common blast-radius risks

- schema changes that affect API and persistence layers
- settings/env changes
- import cycles from cross-module refactors
- fixtures drifting from real behavior

## Exploration hints worth storing

- starting modules and route registration points
- grep seeds such as schema names, task names, or env keys
- package boundaries and shared utility hotspots
