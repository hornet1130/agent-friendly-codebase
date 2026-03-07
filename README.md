# codebase-for-ai

This repository is the development home for a publishable skill package at [skills/codebase-for-ai](/Users/user/projects/codebase-for-ai/skills/codebase-for-ai).

## Layout

- [skills/codebase-for-ai](/Users/user/projects/codebase-for-ai/skills/codebase-for-ai): publishable skill payload for skills.sh and other skill installers
- [AREAS](/Users/user/projects/codebase-for-ai/AREAS): development-only evaluation artifacts and self-dogfood reports
- [assets](/Users/user/projects/codebase-for-ai/assets): development fixtures such as example metrics
- [tests](/Users/user/projects/codebase-for-ai/tests): deterministic validation for the bundled helper scripts

## skills.sh

This repo is structured as a skill collection repo with one publishable skill.

Install it with:

```bash
npx skills add <repo-url> --skill codebase-for-ai
```

After installation, the skill payload should include only the `skills/codebase-for-ai/` subtree. `AREAS/`, `tests/`, and this root README are development artifacts and are not required in the installed skill.

## Development

The source of truth for the skill is the publishable subtree:

- [SKILL.md](/Users/user/projects/codebase-for-ai/skills/codebase-for-ai/SKILL.md)
- [references/RULE.md](/Users/user/projects/codebase-for-ai/skills/codebase-for-ai/references/RULE.md)
- [references/EVALUATION.md](/Users/user/projects/codebase-for-ai/skills/codebase-for-ai/references/EVALUATION.md)
- [scripts](/Users/user/projects/codebase-for-ai/skills/codebase-for-ai/scripts)
- [assets/TEMPLATES](/Users/user/projects/codebase-for-ai/skills/codebase-for-ai/assets/TEMPLATES)
- [agents/openai.yaml](/Users/user/projects/codebase-for-ai/skills/codebase-for-ai/agents/openai.yaml)

`init_area.py` and `init_task.py` are install-safe: they read templates from the skill directory but write `AREAS/<area>/...` into the current working directory by default. Pass `--repo-root` if you need to target a different repository path.

## Validation

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile skills/codebase-for-ai/scripts/*.py tests/*.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 skills/codebase-for-ai/scripts/calculate_score.py assets/example_audit_only_metrics.json
python3 skills/codebase-for-ai/scripts/calculate_score.py AREAS/codebase-for-ai/metrics/baseline.json AREAS/codebase-for-ai/metrics/transformed.json
```
