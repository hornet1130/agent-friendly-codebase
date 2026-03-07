# codebase-for-ai

Publishable `skills.sh` repository for the `codebase-for-ai` skill.

## Install

```bash
npx skills add https://github.com/<owner>/<repo> --skill codebase-for-ai
```

## How It Was Built

This skill was built by applying the skill to itself in repeated loops.

- start with a thin publishable package
- audit the package against its own readiness rules
- add only load-bearing artifacts that improve boundaries, contracts, verification, or persistence
- re-score after each loop and keep the package deployable for `skills.sh`

The current package was shaped through that sequence: packaging cleanup, smoke validation, fixed self-task set, dynamic metrics builder, and repeated-run summary support.

## Philosophy

This skill treats AI-friendliness as an operational property, not a vibe.

Think of a codebase like a workshop for an agent. A good workshop has labeled drawers, calibrated gauges, and a test jig near the bench. An AI-friendly work area should feel the same way: clear boundaries, visible contracts, short paths to the right files, and a deterministic way to check whether the work is actually done.

The bias is toward small executable proofs over long prose. More documentation is not automatically better. The goal is to give the agent the fewest high-value artifacts that make navigation, change, and verification reliable.

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
    scripts/summarize_self_eval_runs.py
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

For repeated runs:

```bash
python3 skills/codebase-for-ai/scripts/summarize_self_eval_runs.py run-01.json run-02.json run-03.json
```

Only deployable skill files are tracked in this repository.
