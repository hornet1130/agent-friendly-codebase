#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
repo_root="$(CDPATH= cd -- "$script_dir/../../.." && pwd)"

skill_dir="$repo_root/skills/codebase-for-ai"
skill="$skill_dir/SKILL.md"
readme="$repo_root/README.md"
metadata="$skill_dir/agents/openai.yaml"
maintenance="$skill_dir/references/MAINTENANCE.md"
evaluation="$skill_dir/references/EVALUATION.md"
smoke="$skill_dir/scripts/smoke_test.sh"
score_script="$skill_dir/scripts/calculate_score.py"

require_file() {
  local path="$1"
  if [ ! -f "$path" ]; then
    echo "package check references missing file: $path" >&2
    exit 1
  fi
}

require_file "$skill"
require_file "$readme"
require_file "$metadata"
require_file "$maintenance"
require_file "$evaluation"
require_file "$smoke"
require_file "$score_script"

grep -q 'references/MAINTENANCE.md' "$skill"
grep -q 'references/EVALUATION.md' "$skill"
grep -q '^## Output contract$' "$skill"
grep -q '^## Workflow$' "$skill"
grep -q '^## Persisted outputs$' "$skill"
grep -q '^## Command matrix$' "$maintenance"
grep -q '^## Contract surface map$' "$maintenance"
grep -q '^## Document ownership$' "$maintenance"
grep -q '^## Exploration starting points$' "$maintenance"
grep -q 'skills/codebase-for-ai/references/MAINTENANCE.md' "$readme"
grep -q 'skills/codebase-for-ai/references/EVALUATION.md' "$readme"
grep -q '^## Install$' "$readme"
grep -q '^## How to Ask$' "$readme"
grep -q '^## Maintainer Notes$' "$readme"
grep -q 'scripts/' "$readme"
grep -q 'display_name:' "$metadata"
grep -q 'codebase-for-ai' "$metadata"

for template in AREA_PROFILE.md EVALUATION_REPORT.md; do
  require_file "$skill_dir/assets/TEMPLATES/$template"
done

sh "$smoke" >/dev/null

for stale_path in \
  "$skill_dir/references/SELF_EVAL.md" \
  "$skill_dir/assets/TEMPLATES/SELF_EVAL_RUN.json" \
  "$skill_dir/assets/TEMPLATES/TASK.md" \
  "$skill_dir/scripts/build_self_eval_metrics.py" \
  "$skill_dir/scripts/summarize_self_eval_runs.py"; do
  if [ -e "$stale_path" ]; then
    echo "legacy benchmark artifact still exists: $stale_path" >&2
    exit 1
  fi
done

if grep -q '^## Command matrix$' "$skill"; then
  echo "ownership drift: command matrix belongs in MAINTENANCE.md" >&2
  exit 1
fi

if grep -q '^## Metrics JSON schema$' "$skill"; then
  echo "ownership drift: metrics schema belongs in EVALUATION.md" >&2
  exit 1
fi

if grep -q '^## Output contract$' "$maintenance"; then
  echo "ownership drift: output contract belongs in SKILL.md" >&2
  exit 1
fi

if grep -q '^## Workflow$' "$maintenance"; then
  echo "ownership drift: runtime workflow belongs in SKILL.md" >&2
  exit 1
fi

if grep -q '^## Metrics JSON schema$' "$maintenance"; then
  echo "ownership drift: metrics schema belongs in EVALUATION.md" >&2
  exit 1
fi

if grep -q '^## Score model$' "$readme"; then
  echo "ownership drift: score model belongs in EVALUATION.md" >&2
  exit 1
fi

if grep -q 'boundary_entrypoints' "$readme"; then
  echo "ownership drift: readiness schema belongs in EVALUATION.md" >&2
  exit 1
fi

if grep -q '^## Persisted outputs$' "$evaluation"; then
  echo "ownership drift: persisted output paths belong in SKILL.md" >&2
  exit 1
fi

if grep -q '^## Command matrix$' "$evaluation"; then
  echo "ownership drift: command matrix belongs in MAINTENANCE.md" >&2
  exit 1
fi

legacy_pattern='SELF_EVAL\.md|SELF_EVAL_RUN\.json|build_self_eval_metrics\.py|summarize_self_eval_runs\.py|ATPS|AIFS|evaluation_mode|missing_measurements|dynamic_breakdown|TASK\.md'

if command -v rg >/dev/null 2>&1; then
  if rg -n "$legacy_pattern" \
    "$readme" "$skill" "$metadata" "$maintenance" "$evaluation" "$skill_dir/assets/TEMPLATES" \
    -g '!**/__pycache__/**' >/dev/null; then
    echo "legacy benchmark artifact reference found" >&2
    exit 1
  fi
elif grep -RInE "$legacy_pattern" \
  "$readme" "$skill" "$metadata" "$maintenance" "$evaluation" "$skill_dir/assets/TEMPLATES" >/dev/null; then
  echo "legacy benchmark artifact reference found" >&2
  exit 1
fi

echo "package check passed"
