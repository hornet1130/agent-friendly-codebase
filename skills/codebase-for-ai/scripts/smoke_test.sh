#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
tmpdir="$(mktemp -d)"

cleanup() {
  rm -rf "$tmpdir"
}

trap cleanup EXIT

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required to run smoke_test.sh" >&2
  exit 1
fi

python3 -m py_compile "$script_dir/calculate_score.py"

cat >"$tmpdir/smoke-test.json" <<'EOF'
{
  "label": "smoke-test",
  "evaluation_mode": "audit-only",
  "readiness": {
    "boundary_entrypoints": 6,
    "commands_env": 5,
    "contracts": 6,
    "context_hierarchy": 5,
    "examples_persistence": 6
  },
  "missing_measurements": [
    "representative dynamic task set",
    "task-level success oracle logs"
  ]
}
EOF

output="$(python3 "$script_dir/calculate_score.py" "$tmpdir/smoke-test.json")"
printf '%s\n' "$output"

printf '%s\n' "$output" | grep -q "Evaluation mode: audit-only"
printf '%s\n' "$output" | grep -q "ACRS: 28/40"
printf '%s\n' "$output" | grep -q "ATPS: incomplete"
printf '%s\n' "$output" | grep -q "AIFS: incomplete"
