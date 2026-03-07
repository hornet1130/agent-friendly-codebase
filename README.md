# codebase-for-ai

Publishable `skills.sh` repository for the `codebase-for-ai` skill.

## Install

```bash
npx skills add https://github.com/<owner>/<repo> --skill codebase-for-ai
```

## Layout

```text
skills/
  codebase-for-ai/
    SKILL.md
    agents/openai.yaml
    references/
    assets/TEMPLATES/
    scripts/smoke_test.sh
    scripts/self_eval_check.sh
    scripts/calculate_score.py
```

## Verify

```bash
python3 -m py_compile skills/codebase-for-ai/scripts/calculate_score.py
sh skills/codebase-for-ai/scripts/smoke_test.sh
sh skills/codebase-for-ai/scripts/self_eval_check.sh
```

Only deployable skill files are tracked in this repository.
