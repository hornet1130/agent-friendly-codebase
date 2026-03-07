#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
repo_root="$(CDPATH= cd -- "$script_dir/../../.." && pwd)"

skill_dir="$repo_root/skills/codebase-for-ai"
self_eval="$skill_dir/references/SELF_EVAL.md"
maintenance="$skill_dir/references/MAINTENANCE.md"
skill="$skill_dir/SKILL.md"
readme="$repo_root/README.md"
metadata="$skill_dir/agents/openai.yaml"
smoke="$skill_dir/scripts/smoke_test.sh"
builder="$skill_dir/scripts/build_self_eval_metrics.py"
run_template="$skill_dir/assets/TEMPLATES/SELF_EVAL_RUN.json"

require_file() {
  local path="$1"
  if [ ! -f "$path" ]; then
    echo "self-eval check references missing file: $path" >&2
    exit 1
  fi
}

require_file "$self_eval"
require_file "$maintenance"
require_file "$skill"
require_file "$readme"
require_file "$metadata"
require_file "$smoke"
require_file "$builder"
require_file "$run_template"

grep -q '^## Self area boundary$' "$self_eval"
grep -q '^## Fixed evaluation conditions$' "$self_eval"
task_count="$(grep -c '^### SE-' "$self_eval")"
if [ "$task_count" -ne 8 ]; then
  echo "expected 8 self-eval tasks, found $task_count" >&2
  exit 1
fi

grep -q 'references/MAINTENANCE.md' "$skill"
grep -q 'references/SELF_EVAL.md' "$skill"
grep -q 'scripts/self_eval_check.sh' "$skill"
grep -q 'scripts/build_self_eval_metrics.py' "$skill"
grep -q 'scripts/self_eval_check.sh' "$readme"
grep -q 'scripts/build_self_eval_metrics.py' "$readme"
grep -q 'display_name:' "$metadata"
grep -q 'codebase-for-ai' "$metadata"

for template in AREA_PROFILE.md TASK.md EVALUATION_REPORT.md; do
  require_file "$skill_dir/assets/TEMPLATES/$template"
done

sh "$smoke" >/dev/null
tmpdir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmpdir"
}
trap cleanup EXIT

python3 - "$run_template" "$tmpdir/run.json" <<'PY'
import json
import sys
from pathlib import Path

template_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
data = json.loads(template_path.read_text(encoding="utf-8"))
data["label"] = "self-eval-check synthetic run"
for task in data["tasks"]:
    task["files_read"] = [task["gold_files"][0]]
    task["first_relevant_read_index"] = 1
output_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY

python3 "$builder" "$tmpdir/run.json" >/dev/null
echo "self-eval check passed"
