# MAINTENANCE.md

Read this file only when you are validating, publishing, or debugging the `agent-friendly-codebase` skill package itself.

## Skill-package boundary

Treat `skills/agent-friendly-codebase/` as the bounded work area when maintaining this skill itself.

- primary paths: `SKILL.md`, `references/`, `scripts/`, `agents/openai.yaml`
- entrypoints: `SKILL.md`, `scripts/smoke_test.sh`, `scripts/package_check.sh`
- important dependencies: `README.md`, Python 3, POSIX shell, and text-search tools (`rg` when available, otherwise `grep -R`)
- reverse dependencies: the root install command, packaged skill loading, and any automation that shells out to `scripts/calculate_score.py`

## Command matrix

Run commands from the repository root.

| Need | Command | When to use it |
|---|---|---|
| install | `N/A` | This package ships plain files and helper scripts. No install step is required beyond having `python3` and `sh`. |
| build | `python3 -m py_compile skills/agent-friendly-codebase/scripts/calculate_score.py` | Fast syntax proof after score-script edits. |
| test | `sh skills/agent-friendly-codebase/scripts/smoke_test.sh` | Fastest trusted area-scoped proof for readiness-score formatting. |
| lint | `N/A` | No dedicated linter is bundled. Use `py_compile` plus the shell checks as the canonical validation path. |
| dev | `N/A` | This skill package has no long-running dev server. |
| regression | `sh skills/agent-friendly-codebase/scripts/package_check.sh` | Broader package regression after docs, metadata, templates, or validation-path changes. |

Use the `test` row before the `regression` row when both apply.

## Contract surface map

Treat these files as the source of truth for the package contracts.

| Contract surface | Source of truth | Checked by |
|---|---|---|
| workflow and readiness score model | `SKILL.md`, `references/EVALUATION.md`, `scripts/calculate_score.py` | `python3 -m py_compile ...`, `sh scripts/smoke_test.sh` |
| saved output paths | `references/MAINTENANCE.md`, `assets/TEMPLATES/AREA_PROFILE.md`, `assets/TEMPLATES/EVALUATION_REPORT.md` | `sh scripts/package_check.sh` |
| package identity and install surface | `README.md`, `SKILL.md`, `agents/openai.yaml` | `sh scripts/package_check.sh` |
| package validation paths | `references/MAINTENANCE.md`, `scripts/smoke_test.sh`, `scripts/package_check.sh` | `sh scripts/package_check.sh` |

## Document ownership

Keep the package contract split sharp:

- `README.md`: install, when to use, request examples, and top-level maintainer links
- `SKILL.md`: runtime contract, read path, output contract, and workflow
- `references/EVALUATION.md`: readiness rubric, scoring anchors, evidence minimum, and metrics schema
- `references/MAINTENANCE.md`: validation, packaging, saved output paths, drift debugging, and document ownership

If a change adds the same contract detail to multiple documents, prefer one source of truth and replace the rest with short links.

## Saved output paths

Default to chat-only. Only write files when the user explicitly asks.

When saved outputs are requested, keep them under `AREAS/<area>/`. Typical files are:

- `AREAS/<area>/PROFILE.md`
- `AREAS/<area>/reports/review.md`
- `AREAS/<area>/reports/before.md`
- `AREAS/<area>/reports/after.md`
- `AREAS/<area>/metrics/review.json`
- `AREAS/<area>/metrics/before.json`
- `AREAS/<area>/metrics/after.json`

## Canonical smoke test

Run these commands from the repository root:

```bash
python3 -m py_compile skills/agent-friendly-codebase/scripts/calculate_score.py
sh skills/agent-friendly-codebase/scripts/smoke_test.sh
```

Expected result:

- the score script compiles
- the smoke test prints `ACRS: 28/40`
- the smoke test prints `Readiness band: so-so`

## Full package validation

Run these commands from the repository root:

```bash
python3 -m py_compile skills/agent-friendly-codebase/scripts/calculate_score.py
sh skills/agent-friendly-codebase/scripts/smoke_test.sh
sh skills/agent-friendly-codebase/scripts/package_check.sh
```

Expected result:

- the smoke test passes
- the package check passes
- `README.md`, `SKILL.md`, `EVALUATION.md`, and `agents/openai.yaml` stay aligned
- deleted benchmark artifacts do not reappear in the package

## Exploration starting points

Use these first when the task is obvious:

- score output or schema drift: `scripts/calculate_score.py`
- package layout or metadata drift: `README.md`, `SKILL.md`, `agents/openai.yaml`
- validation-path drift: `scripts/smoke_test.sh`, `scripts/package_check.sh`
- score-model wording drift: `references/EVALUATION.md`

## Worked example

The bundled smoke test creates this minimal readiness input:

```json
{
  "label": "smoke-test",
  "context": {
    "area": "skills/agent-friendly-codebase",
    "proof_path": "sh skills/agent-friendly-codebase/scripts/smoke_test.sh",
    "evidence_refs": [
      "skills/agent-friendly-codebase/scripts/smoke_test.sh",
      "skills/agent-friendly-codebase/scripts/calculate_score.py"
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
      "reason": "The score model and workflow are visible in the public and maintainer docs.",
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
      "reason": "Smoke validation exists and the maintainer guide stores recurring package knowledge.",
      "evidence_refs": [
        "skills/agent-friendly-codebase/scripts/smoke_test.sh",
        "skills/agent-friendly-codebase/references/MAINTENANCE.md"
      ]
    }
  }
}
```

This is the canonical example for verifying that packaging and readiness scoring still work after edits.

## Common failure modes

- `python3: command not found`
  Install Python 3 or do not claim the helper scripts are verified.
- `expected top-level key 'readiness'`
  The metrics file is malformed.
- `missing readiness key '...'`
  The metrics payload no longer matches the readiness schema.
- `readiness '...' must be a number in [0, 8]`
  A readiness value is outside the supported range.
- `missing justification key '...'`
  A readiness score was recorded without a per-category rationale block.
- `justification '...' evidence_refs must be a non-empty list of strings`
  A category score lacks traceable evidence references.
- `package check references missing file`
  A packaged file moved without updating `scripts/package_check.sh`.
- `legacy benchmark artifact reference found`
  A deleted benchmark-only file or term was reintroduced into the package surface.

## Knowledge persistence

When recurring maintenance knowledge is discovered:

- record packaging, validation, and publish gotchas here
- update `references/EVALUATION.md` only for score-model changes
- update `SKILL.md` only for workflow changes
