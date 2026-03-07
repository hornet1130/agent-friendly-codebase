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
summarizer="$skill_dir/scripts/summarize_self_eval_runs.py"
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
require_file "$summarizer"
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
grep -q 'scripts/summarize_self_eval_runs.py' "$skill"
grep -q 'scripts/self_eval_check.sh' "$readme"
grep -q 'scripts/build_self_eval_metrics.py' "$readme"
grep -q 'scripts/summarize_self_eval_runs.py' "$readme"
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

python3 - "$run_template" "$tmpdir/run-01.json" "$tmpdir/run-02.json" <<'PY'
import json
import sys
from pathlib import Path

template_path = Path(sys.argv[1])
output_path_one = Path(sys.argv[2])
output_path_two = Path(sys.argv[3])
data = json.loads(template_path.read_text(encoding="utf-8"))
data["label"] = "self-eval-check synthetic run 1"
for task in data["tasks"]:
    task["files_read"] = [task["gold_files"][0]]
    task["first_relevant_read_index"] = 1
    task["resolved"] = True
    task["valid_patch"] = True
    task["regression_free"] = True
    task["human_intervention_needed"] = False
output_path_one.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

run_two = json.loads(json.dumps(data))
run_two["label"] = "self-eval-check synthetic run 2"
run_two["sequence_gain"] = 0.1
run_two["cost_reduction_rate"] = 0.05
run_two["tasks"][0]["review_accepted"] = True
output_path_two.write_text(json.dumps(run_two, indent=2) + "\n", encoding="utf-8")
PY

python3 "$builder" "$tmpdir/run-01.json" >/dev/null
python3 "$summarizer" "$tmpdir/run-01.json" "$tmpdir/run-02.json" >/dev/null
echo "self-eval check passed"
