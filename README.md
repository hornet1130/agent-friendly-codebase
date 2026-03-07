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
    scripts/build_self_eval_metrics.py
    scripts/calculate_score.py
```

## Verify

```bash
python3 -m py_compile skills/codebase-for-ai/scripts/calculate_score.py
python3 -m py_compile skills/codebase-for-ai/scripts/build_self_eval_metrics.py
sh skills/codebase-for-ai/scripts/smoke_test.sh
sh skills/codebase-for-ai/scripts/self_eval_check.sh
```

## Self Benchmark

```bash
python3 skills/codebase-for-ai/scripts/build_self_eval_metrics.py path/to/self-eval-run.json --out path/to/metrics.json
python3 skills/codebase-for-ai/scripts/calculate_score.py path/to/metrics.json
```

Start from `skills/codebase-for-ai/assets/TEMPLATES/SELF_EVAL_RUN.json` and replace all `REPLACE_WITH_...` placeholders first.

Only deployable skill files are tracked in this repository.
