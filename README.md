# agent-friendly-codebase

`agent-friendly-codebase` is a `skills.sh` skill for making a bounded work area easier for agents to review, change, verify, and hand off.

## Install

```bash
npx skills add https://github.com/hornet1130/agent-friendly-codebase
```

## When to Use

Use this skill when you want an agent to work on a codebase more like a good teammate and less like a tourist.

It is designed for two practical workflows:

- `review`: inspect a bounded work area, score its current readiness, and surface the biggest agent-friction points
- `transform`: improve a bounded work area, run the proof path, and summarize what improved for both direct work and future handoffs

## How to Ask

Good requests are concrete about the area and the proof path. For example:

- `Use agent-friendly-codebase to review apps/api/src/modules/auth`
- `Use agent-friendly-codebase to review the checkout area and show the biggest agent-friction points`
- `Use agent-friendly-codebase to transform packages/shared/http-client so an agent can ship bug fixes with less context hunting`
- `Use agent-friendly-codebase to transform apps/web/src/features/checkout and use pnpm test --filter checkout as the proof command`
- `Use agent-friendly-codebase on this repo, but keep the result chat-only unless I ask you to persist files`
- `Use agent-friendly-codebase to make the auth module easier for multiple agents to split and hand off safely`

## What You Get

Depending on the request, the skill produces some combination of:

- work-area boundaries and entrypoints
- canonical commands and validation paths
- contract and blast-radius mapping
- current-state or review snapshot scoring
- proof-oriented transformation plans
- improvement summaries for the transformed area
- ownership, handoff, and collision-risk notes when multiple agents are relevant

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

Only deployable skill files are tracked in this repository.
