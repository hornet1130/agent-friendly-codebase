# agent-friendly-codebase

`agent-friendly-codebase` is a `skills.sh` skill designed to review and transform bounded work areas so agents can find files faster, make smaller safer changes, verify results with less human help, and hand off work with low ambiguity.

## Install

```bash
npx skills add https://github.com/hornet1130/agent-friendly-codebase
```

## When to Use

Use this skill when you want an agent to work on a codebase more like a good teammate and less like a tourist. Apply it on a **bounded work area** in one of two modes:

- `review`: inspect a bounded work area, score its current readiness, and surface the biggest agent-friction points
- `transform`: improve a bounded work area, run the proof path, and summarize what improved for both direct work and future handoffs

## Core Principles

This skill evaluates and transforms areas based on five Must-level rules:

- **P1. Boundary & entrypoints**: Name primary paths, identify entrypoints, and map important dependencies.
- **P2. Commands & environment**: Define canonical build/test/dev commands and provide an automated validation path.
- **P3. Contracts & change surface**: Expose public contracts and make the external system boundaries visible.
- **P4. Context hierarchy & economy**: Keep guidance high-signal, layered, and distinguish repository-wide from area-local guidance.
- **P5. Examples, verification & persistence**: Externalize recurring patterns into docs/tests and define a lightweight proof path.

## Scoring Model (ACRS)

The snapshot score is evaluated using the **Agent Codebase Readiness Score (ACRS)** (range 0..20), summed from 5 categories:

- **S1. Boundary & entrypoints** (0-4)
- **S2. Commands & environment** (0-4)
- **S3. Contracts & change surface** (0-4)
- **S4. Context hierarchy & economy** (0-4)
- **S5. Examples, verification & persistence** (0-4)

**Bands**: **good** `>=16`, **so-so** `10-15`, **bad** `<10`.

## How to Ask

Good requests are concrete about the area and the proof path. For example:

- `Use agent-friendly-codebase to review apps/api/src/modules/auth`
- `Use agent-friendly-codebase to review the checkout area and show the biggest agent-friction points`
- `Use agent-friendly-codebase to transform packages/shared/http-client so an agent can ship bug fixes with less context hunting`
- `Use agent-friendly-codebase to transform apps/web/src/features/checkout and use pnpm test --filter checkout as the proof command`
- `Use agent-friendly-codebase on this repo, but keep the result chat-only unless I ask you to persist files`
- `Use agent-friendly-codebase to make the auth module easier for multiple agents to split and hand off safely`

## What You Get

### `review` Mode
Produce an area boundary summary, entrypoints, canonical proof paths, ACRS readiness snapshot, top agent-friction gaps, and the smallest useful next improvements.

### `transform` Mode
Produce scoped area rules, apply the smallest useful changes, run proof paths, provide a post-change summary with the new ACRS score, and note remaining risks.

*Note: When the user explicitly mentions parallel agents or handoff, the skill will map ownership lanes and collision hotspots.*

By default, the result is returned in chat. It only writes files when the user explicitly asks for persisted artifacts.

## Security Posture

This package ships plain text guidance and small local helper scripts.

- no external downloads
- no install hooks
- no credential collection
- chat-only by default, with saved files only on explicit request

## Maintainer Notes

- Packaging and validation workflow: `skills/agent-friendly-codebase/references/MAINTENANCE.md`
- Scoring model and qualitative bands: `skills/agent-friendly-codebase/references/EVALUATION.md`
- Full rules and definitions: `skills/agent-friendly-codebase/references/RULE.md`
- Checklists for review and transform: `skills/agent-friendly-codebase/references/CHECKLIST.md`

Only deployable skill files are tracked in this repository.
