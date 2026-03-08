# codebase-for-ai

`codebase-for-ai` is a `skills.sh` skill for making a bounded work area easier for AI agents to review, change, and verify.

## Install

```bash
npx skills add https://github.com/hornet1130/codebase-for-ai
```

## When to Use

Use this skill when you want an agent to work on a codebase more like a good teammate and less like a tourist.

It is designed for two practical workflows:

- `review`: inspect a bounded work area, score its current readiness, and surface the biggest AI-friction points
- `transform`: improve a bounded work area, run the proof path, and report the before/after delta

## How to Ask

Good requests are concrete about the area and the proof path. For example:

- `Use codebase-for-ai to review apps/api/src/modules/auth`
- `Use codebase-for-ai to review the checkout area and show the biggest AI-friction points`
- `Use codebase-for-ai to transform packages/shared/http-client so an AI agent can ship bug fixes with less context hunting`
- `Use codebase-for-ai to transform apps/web/src/features/checkout and use pnpm test --filter checkout as the proof command`
- `Use codebase-for-ai on this repo, but keep the result chat-only unless I ask you to persist files`

## What You Get

Depending on the request, the skill produces some combination of:

- work-area boundaries and entrypoints
- canonical commands and validation paths
- contract and blast-radius mapping
- before or review snapshot scoring
- proof-oriented transformation plans
- before vs after comparisons for the transformed area

By default, the result is returned in chat. It only writes files when the user explicitly asks for persisted artifacts.

## How It Was Built

This skill was built by applying the skill to itself in repeated loops.

- start with a thin publishable package
- audit the package against its own readiness rules
- add only load-bearing artifacts that improve boundaries, contracts, verification, or persistence
- re-score after each loop and keep the package deployable for `skills.sh`

The current package was shaped through that sequence: packaging cleanup, smoke validation, review-first maintenance guidance, and readiness-score simplification.

## Philosophy

This skill treats AI-friendliness as an operational property, not a vibe.

Think of a codebase like a workshop for an agent. A good workshop has labeled drawers, calibrated gauges, and a test jig near the bench. An AI-friendly work area should feel the same way: clear boundaries, visible contracts, short paths to the right files, and a deterministic way to check whether the work is actually done.

The bias is toward small executable proofs over long prose. More documentation is not automatically better. The goal is to give the agent the fewest high-value artifacts that make navigation, change, and verification reliable.

Skills work best when they use progressive disclosure:

- short activation metadata
- a thin `SKILL.md`
- deeper references and helper scripts only when needed

That is the design here as well. The always-loaded part stays small, and the heavier scoring or maintenance logic lives behind references and helper scripts.

## Layout

```text
skills/
  codebase-for-ai/
    SKILL.md
    agents/openai.yaml
    references/
    assets/TEMPLATES/
    scripts/
```

## Maintainer Notes

- Packaging and validation workflow: `skills/codebase-for-ai/references/MAINTENANCE.md`
- Scoring model and qualitative bands: `skills/codebase-for-ai/references/EVALUATION.md`

Only deployable skill files are tracked in this repository.
