# EVALUATION.md

This file defines the practical scoring model for `review` and `transform`.

The current package uses a **readiness snapshot** model only.

## Evaluation flow

Use these default workflows:

- `review` -> readiness snapshot
- `transform` -> before snapshot, change, proof, after snapshot, delta

Do not invent a heavier protocol unless the user explicitly asks for one and is willing to define it outside this package.

## Fixed comparison conditions

When comparing before and after states, keep these fixed:

- the same work area
- the same readiness rubric
- the same proof path
- the same agent or model family
- the same tool permissions
- the same evidence standard

If any of these change, treat the result as a different evaluation.

## Score model

The snapshot score is `ACRS`:

`ACRS = S1 + S2 + S3 + S4 + S5`

- `ACRS`: AI Codebase Readiness Score, `0..40`

Three-level summary band:

- `good`: `ACRS >= 32`
- `so-so`: `24 <= ACRS < 32`
- `bad`: `ACRS < 24`

Use the summary band as the quick headline. Use the sub-scores to explain the result.

## Scoring anchors

To keep repeated reviews closer together, prefer these anchors:

- `0`: effectively absent
- `2`: weak or mostly implicit
- `4`: partially usable, but important gaps remain
- `6`: solid for normal work, with only moderate friction
- `8`: explicit, current, easy to use, and low ambiguity

Use odd numbers only when the area clearly falls between two anchors.

## ACRS categories

Each readiness category is scored from `0` to `8`.

### S1. Boundary and entrypoints

Evidence to look for:

- the work area boundary is documented
- entrypoints are explicit
- important dependencies and reverse dependencies are visible
- there is a clear starting point for exploration

Anchor interpretation:

- `0`: boundary and starting files are unclear
- `4`: the main path is inferable, but dependencies or entrypoints are still patchy
- `8`: boundary, entrypoints, and starting files are explicit and easy to follow

### S2. Commands and environment

Evidence to look for:

- canonical install, build, test, lint, and dev commands exist, or clear equivalents are called out
- at least one area-scoped proof or validation command exists
- common failure causes are documented briefly
- env vars, seeds, fixtures, or setup entrypoints are visible

Anchor interpretation:

- `0`: no trusted command path
- `4`: proof path exists, but setup or command coverage is incomplete
- `8`: normal build, test, and proof paths are explicit with low setup ambiguity

### S3. Contracts and change surface

Evidence to look for:

- public contracts are visible
- DTOs, schemas, and type boundaries are easy to find
- external integrations are visible
- likely impact radius is predictable

Anchor interpretation:

- `0`: contracts are mostly implicit
- `4`: main contracts are visible, but impact radius is still hard to predict
- `8`: contract surfaces and likely blast radius are explicit and easy to trace

### S4. Context hierarchy and economy

Evidence to look for:

- root guidance and area guidance are separated
- always-loaded instructions are not bloated
- detail is pushed to supporting files
- duplication and conflicts between guidance files are low

Anchor interpretation:

- `0`: guidance is bloated, scattered, or contradictory
- `4`: guidance is usable, but layering or duplication still causes drift
- `8`: high-signal default guidance with clear supporting references and low duplication

### S5. Examples, verification, and persistence

Evidence to look for:

- a canonical or recent example exists
- automated verification exists
- known failures or debug notes are captured
- there is an explicit place to store learned patterns

Anchor interpretation:

- `0`: no dependable examples or verification path
- `4`: either verification or examples exist, but persistence is inconsistent
- `8`: examples, verification, and knowledge capture are all easy to find and current

## Default reporting

### `review`

Report:

- `ACRS`
- readiness breakdown
- summary band
- biggest gaps
- recommended proof path

### `transform`

Report:

- before `ACRS`
- proof results after the change
- after `ACRS`
- absolute delta
- remaining risks

## Evidence minimum

Every scored result should include:

- the bounded work area
- the proof path used or proposed
- the evidence references used for scoring
- the evidence behind each sub-score
- any missing evidence or ambiguity

Do not claim a transformation helped unless the before and after scores use the same rubric and proof path.

## Metrics JSON schema

`scripts/calculate_score.py` expects a JSON object with:

- `label` as an optional string
- `context` as an object containing:
  - `area`
  - `proof_path`
  - `evidence_refs`
  - `ambiguities` as an optional list of strings
- `readiness` as an object containing:
  - `boundary_entrypoints`
  - `commands_env`
  - `contracts`
  - `context_hierarchy`
  - `examples_persistence`
- `justification` as an object with the same five readiness keys, where each key contains:
  - `reason`
  - `evidence_refs`

Each readiness value must be numeric in `[0, 8]`.
Each justification `reason` must be a non-empty string.
Each justification `evidence_refs` value must be a non-empty list of strings.

Minimal example:

```json
{
  "label": "checkout review",
  "context": {
    "area": "apps/web/src/features/checkout",
    "proof_path": "pnpm test --filter checkout",
    "evidence_refs": [
      "apps/web/src/features/checkout/index.ts",
      "apps/web/src/features/checkout/README.md"
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
      "reason": "Primary paths and entrypoints are visible, but reverse dependencies are only partly documented.",
      "evidence_refs": [
        "apps/web/src/features/checkout/index.ts",
        "apps/web/src/features/checkout/README.md"
      ]
    },
    "commands_env": {
      "reason": "Area proof path exists, but setup notes are still thin.",
      "evidence_refs": [
        "apps/web/package.json",
        "apps/web/src/features/checkout/README.md"
      ]
    },
    "contracts": {
      "reason": "Main request and schema surfaces are visible.",
      "evidence_refs": [
        "apps/web/src/features/checkout/schema.ts"
      ]
    },
    "context_hierarchy": {
      "reason": "The area has local guidance, but some global notes still overlap.",
      "evidence_refs": [
        "AGENTS.md",
        "apps/web/src/features/checkout/README.md"
      ]
    },
    "examples_persistence": {
      "reason": "Verification exists and known patterns are recorded in the area README.",
      "evidence_refs": [
        "apps/web/src/features/checkout/README.md",
        "apps/web/src/features/checkout/checkout.test.ts"
      ]
    }
  }
}
```

The score script emits:

- `ACRS`
- readiness breakdown
- summary band

Use the script for stable formatting, not as a substitute for evidence.
