# EVALUATION.md

This file defines the detailed scoring model for `review` and `transform`. For the compact summary, see `SKILL.md`.

## Evaluation flow

- `review` -> readiness snapshot
- `transform` -> current-state summary, change, proof, post-change summary, delta

Do not invent a heavier protocol unless the user explicitly asks for one.

## Fixed comparison conditions

When comparing before and after states, keep these fixed:

- the same work area
- the same readiness rubric
- the same proof path
- the same agent or model family
- the same coordination scope or handoff assumptions
- the same tool permissions
- the same evidence standard

If any of these change, treat the result as a different evaluation.

## Score model

`ACRS = S1 + S2 + S3 + S4 + S5`, range `0..20`.

Bands: **good** `>=16`, **so-so** `10-15`, **bad** `<10`.

Each category is scored `0-4`:

| Score | Meaning |
|---:|---|
| 0 | absent — effectively unusable |
| 1 | weak — mostly implicit |
| 2 | partial — important gaps remain |
| 3 | solid — works for normal tasks, moderate friction only |
| 4 | explicit — current, low ambiguity |

## ACRS categories

### S1. Boundary and entrypoints (0-4)

| Score | Interpretation |
|---:|---|
| 0 | Boundary and starting files are unclear |
| 1 | Some code paths identifiable, but entrypoints and dependencies mostly implicit |
| 2 | Main path inferable, but dependencies or entrypoints patchy |
| 3 | Boundary and entrypoints documented, minor gaps in dependency visibility |
| 4 | Boundary, entrypoints, and starting files explicit and easy to follow |

Evidence: documented boundary, explicit entrypoints, visible dependencies and reverse dependencies, clear exploration starting point.

### S2. Commands and environment (0-4)

| Score | Interpretation |
|---:|---|
| 0 | No trusted command path |
| 1 | Some commands exist but scattered or undocumented |
| 2 | Proof path exists, but setup or coverage incomplete |
| 3 | Build and test paths work, minor setup friction remains |
| 4 | Build, test, and proof paths explicit with low setup ambiguity |

Evidence: canonical install/build/test/lint/dev commands, area-scoped proof command, documented common failures, visible env/seeds/fixtures.

### S3. Contracts and change surface (0-4)

| Score | Interpretation |
|---:|---|
| 0 | Contracts mostly implicit |
| 1 | Some contracts visible, but key surfaces still undocumented |
| 2 | Main contracts visible, but impact radius hard to predict |
| 3 | Contract surfaces documented, blast radius mostly predictable |
| 4 | Contract surfaces and blast radius explicit and traceable |

Evidence: visible public contracts, findable DTOs/schemas/types, visible external integrations, predictable impact radius.

### S4. Context hierarchy and economy (0-4)

| Score | Interpretation |
|---:|---|
| 0 | Guidance bloated, scattered, or contradictory |
| 1 | Some guidance exists but not layered, significant duplication |
| 2 | Guidance usable, but layering or duplication causes drift |
| 3 | Guidance separated by scope, minor duplication remains |
| 4 | High-signal default guidance with clear supporting references |

Evidence: separated root/area guidance, compact always-loaded instructions, detail pushed to supporting files, low duplication.

### S5. Examples, verification, and persistence (0-4)

| Score | Interpretation |
|---:|---|
| 0 | No dependable examples or verification path |
| 1 | Minimal examples or tests exist, no knowledge persistence |
| 2 | Either verification or examples exist, but persistence inconsistent |
| 3 | Examples and verification present, knowledge capture mostly in place |
| 4 | Examples, verification, and knowledge capture all easy to find and current |

Evidence: canonical/recent example, automated verification, captured known failures/debug notes, explicit place for learned patterns.

## Scoring consistency

The scoring rubric must produce stable results across N independent runs by the same agent on the same area.

Rules for consistent scoring:

1. **Score from evidence, not impression.** Each sub-score must cite at least one specific file, section, or command. If no evidence exists, score 0 or 1.
2. **Use the interpretation table literally.** Pick the row that best matches the observed state. Do not interpolate between rows.
3. **Default to the lower score** when the area falls between two levels. Upgrade only when clear evidence supports the higher level.
4. **List evidence before scoring.** Gather the evidence list first, then assign scores. Do not score first and justify later.
5. **Treat absence as 0, not unknown.** If a category has no observable evidence after reasonable exploration, score 0.

These rules reduce the variance between independent runs to at most 1 point per category (±1) and at most 2 points on ACRS (±2).

## Default reporting

### `review`

Report: ACRS, readiness breakdown, summary band, biggest gaps, recommended proof path.

### `transform`

Report: before ACRS, proof results, after ACRS, absolute delta, remaining risks.

## Evidence minimum

Every scored result should include:

- the bounded work area
- the proof path used or proposed
- the evidence references for scoring
- the evidence behind each sub-score
- any missing evidence or ambiguity

Do not claim a transformation helped unless the before and after scores use the same rubric and proof path.
