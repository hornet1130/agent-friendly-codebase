# agent-friendly-codebase

Codebases built and maintained by humans rely on tacit knowledge, verbal handoffs, and team culture. AI agents don't have that context — they work with what's written, and when nothing is written, they infer. Inference fails.

`agent-friendly-codebase` is an audit skill for turning human-maintained codebases into **Agent-Friendly Codebases (AFC)**. It diagnoses what makes agents fail, and delivers a prioritized improvement roadmap.

## Install

```bash
npx skills add https://github.com/hornet1130/agent-friendly-codebase --skill agent-friendly-codebase
```

## What It Does

Diagnoses the root causes of agent errors through **four friction patterns**:

| Pattern | Problem | Agent impact |
|---|---|---|
| A. Tacit knowledge | Unwritten team knowledge | Infers instead of knowing — inference fails |
| B. Code/doc divergence | Stale docs contradict code | Poisoned context from the start — snowball |
| C. Competing patterns | Two ways to do the same thing | Picks by frequency, not intent — wrong pattern |
| D. No feedback loop | No tests or verification | Can't self-verify — reports "done" without proof |

Then frames improvements using the **AFC maturity model**:

- **L1 — Safety net**: make wrong things impossible via tooling (lint rules, pre-commit hooks, coverage ratchets)
- **L2 — Explicitness**: turn tacit knowledge into explicit knowledge (single canonical patterns, "why" comments, domain glossaries)
- **L3 — Spec-driven**: specs as input, machines verify compliance (SPEC.md → schema → test → implementation)

## AFC Score

5 categories, each 0–20. Total 0–100, expressed as **AFC Score (%)**.

| Category | Key question |
|---|---|
| S1. Boundary & entrypoints | Can the agent find where to start and where to stop? |
| S2. Commands & environment | Can the agent build, test, and run without human memory? |
| S3. Contracts & change surface | Can the agent predict blast radius from what's visible? |
| S4. Context hierarchy & economy | Is guidance high-signal, layered, and appropriately scoped? |
| S5. Examples, verification & persistence | Can the agent learn from examples and verify its own work? |

**Bands**: Good >= 80, So-so 50–79, Bad < 50

## How to Ask

```
Use agent-friendly-codebase to audit apps/api/src/modules/auth
Use agent-friendly-codebase to audit the checkout area
Use agent-friendly-codebase on this repo
```

## What You Get

- **Area profile**: boundaries, entrypoints, contracts, commands, proof path
- **AFC Score**: per-category scores with evidence, total, and band
- **Findings**: friction patterns with evidence and agent impact, ordered by impact
- **Improvement roadmap**: L1 → L2 → L3 steps, each specific enough to assign

## Security Posture

- no external downloads
- no install hooks
- no credential collection
- chat-only by default, files only on explicit request

## Maintainer Notes

All audit logic, scoring rules, and maturity model are in a single file: `skills/agent-friendly-codebase/SKILL.md`
