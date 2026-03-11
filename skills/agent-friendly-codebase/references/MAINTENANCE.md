# MAINTENANCE.md

Read this file only when maintaining the `agent-friendly-codebase` skill package itself.

## Skill-package boundary

Treat `skills/agent-friendly-codebase/` as the bounded work area.

- primary paths: `SKILL.md`, `references/`
- entrypoints: `SKILL.md`
- assets: `assets/TEMPLATES/`

## Document ownership

- `SKILL.md`: runtime contract, core principles, scoring model, output contract, workflow, references
- `references/EVALUATION.md`: detailed scoring anchors, comparison conditions, consistency guidelines
- `references/RULE.md`: full rule definitions with Should-level guidance
- `references/CHECKLIST.md`: step-by-step checklists for review and transform
- `references/MAINTENANCE.md`: package structure, document ownership

If a change adds the same contract detail to multiple documents, prefer one source of truth and replace the rest with short links.

## Knowledge persistence

When recurring maintenance knowledge is discovered:

- record packaging gotchas here
- update `references/EVALUATION.md` only for score-model changes
- update `SKILL.md` only for workflow changes
