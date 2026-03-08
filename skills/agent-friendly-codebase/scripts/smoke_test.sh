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
  "context": {
    "area": "skills/agent-friendly-codebase",
    "proof_path": "sh skills/agent-friendly-codebase/scripts/smoke_test.sh",
    "evidence_refs": [
      "skills/agent-friendly-codebase/scripts/smoke_test.sh",
      "skills/agent-friendly-codebase/scripts/calculate_score.py"
    ],
    "ambiguities": [],
    "coordination_scope": "multi-agent"
  },
  "readiness": {
    "boundary_entrypoints": 6,
    "commands_env": 5,
    "contracts": 6,
    "context_hierarchy": 5,
    "examples_persistence": 6
  },
  "justification": {
    "boundary_entrypoints": {
      "reason": "The skill package boundary and entrypoints are explicit in the maintainer docs.",
      "evidence_refs": [
        "skills/agent-friendly-codebase/references/MAINTENANCE.md",
        "skills/agent-friendly-codebase/SKILL.md"
      ]
    },
    "commands_env": {
      "reason": "The package has clear smoke and package validation commands.",
      "evidence_refs": [
        "skills/agent-friendly-codebase/references/MAINTENANCE.md",
        "skills/agent-friendly-codebase/scripts/smoke_test.sh"
      ]
    },
    "contracts": {
      "reason": "The score model, workflow, and handoff-safe defaults are visible in the public and maintainer docs.",
      "evidence_refs": [
        "skills/agent-friendly-codebase/references/EVALUATION.md",
        "skills/agent-friendly-codebase/SKILL.md"
      ]
    },
    "context_hierarchy": {
      "reason": "The package keeps public workflow guidance separate from maintenance guidance.",
      "evidence_refs": [
        "skills/agent-friendly-codebase/SKILL.md",
        "skills/agent-friendly-codebase/references/MAINTENANCE.md"
      ]
    },
    "examples_persistence": {
      "reason": "Smoke validation exists and the maintainer guide stores recurring package knowledge for future agents.",
      "evidence_refs": [
        "skills/agent-friendly-codebase/scripts/smoke_test.sh",
        "skills/agent-friendly-codebase/references/MAINTENANCE.md"
      ]
    }
  }
}
EOF

output="$(python3 "$script_dir/calculate_score.py" "$tmpdir/smoke-test.json")"
printf '%s\n' "Fixture mode: deterministic sample, not a live package review"
printf '%s\n' "$output"

printf '%s\n' "$output" | grep -q "Area: skills/agent-friendly-codebase"
printf '%s\n' "$output" | grep -q "ACRS: 28/40"
printf '%s\n' "$output" | grep -q "Readiness band: so-so"
printf '%s\n' "$output" | grep -q "Coordination scope: multi-agent"
printf '%s\n' "$output" | grep -q "Justification summary:"
