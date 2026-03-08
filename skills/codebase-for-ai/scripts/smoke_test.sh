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
    "area": "skills/codebase-for-ai",
    "proof_path": "sh skills/codebase-for-ai/scripts/smoke_test.sh",
    "evidence_refs": [
      "skills/codebase-for-ai/scripts/smoke_test.sh",
      "skills/codebase-for-ai/scripts/calculate_score.py"
    ],
    "ambiguities": []
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
        "skills/codebase-for-ai/references/MAINTENANCE.md",
        "skills/codebase-for-ai/SKILL.md"
      ]
    },
    "commands_env": {
      "reason": "The package has clear smoke and package validation commands.",
      "evidence_refs": [
        "skills/codebase-for-ai/references/MAINTENANCE.md",
        "skills/codebase-for-ai/scripts/smoke_test.sh"
      ]
    },
    "contracts": {
      "reason": "The score model and workflow are visible in the public and maintainer docs.",
      "evidence_refs": [
        "skills/codebase-for-ai/references/EVALUATION.md",
        "skills/codebase-for-ai/SKILL.md"
      ]
    },
    "context_hierarchy": {
      "reason": "The package keeps public workflow guidance separate from maintenance guidance.",
      "evidence_refs": [
        "skills/codebase-for-ai/SKILL.md",
        "skills/codebase-for-ai/references/MAINTENANCE.md"
      ]
    },
    "examples_persistence": {
      "reason": "Smoke validation exists and the maintainer guide stores recurring package knowledge.",
      "evidence_refs": [
        "skills/codebase-for-ai/scripts/smoke_test.sh",
        "skills/codebase-for-ai/references/MAINTENANCE.md"
      ]
    }
  }
}
EOF

output="$(python3 "$script_dir/calculate_score.py" "$tmpdir/smoke-test.json")"
printf '%s\n' "$output"

printf '%s\n' "$output" | grep -q "Area: skills/codebase-for-ai"
printf '%s\n' "$output" | grep -q "ACRS: 28/40"
printf '%s\n' "$output" | grep -q "Readiness band: so-so"
printf '%s\n' "$output" | grep -q "Justification summary:"
