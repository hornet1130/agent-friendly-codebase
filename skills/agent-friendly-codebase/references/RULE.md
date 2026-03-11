# RULE.md

This file defines what this package means by an agent-friendly codebase and what rules a transformed work area should satisfy. For the condensed Must-level summary, see `SKILL.md` Core principles.

## Core definition

An agent-friendly codebase is a structural combination of code, documentation, tooling, tests, and local guidance that lets an agent:

- reach relevant context with low exploration cost
- make bounded changes with a predictable blast radius
- verify changes with a short trusted proof path
- hand off or split work with low ambiguity

This package evaluates at the **work area** level, not at the whole-repository level.

A **work area** is a bounded unit of work defined by:

- primary code paths
- explicit entrypoints
- visible external and internal contracts
- canonical build, run, and validation commands
- a lightweight review rubric and proof path

Examples: `apps/web/src/features/checkout`, `apps/api/src/modules/auth`, `packages/shared/http-client`

## The rules

### R1. Boundary clarity

Purpose: make it obvious where the agent should read and edit first.

Must:

- name the primary paths for the area
- identify its entrypoints
- identify important dependencies and reverse dependencies

Should:

- document the usual starting files
- keep frequently edited files easy to find

### R2. Contract visibility

Purpose: let the agent predict impact by reading visible surfaces instead of folklore.

Must:

- expose the important public contracts (routes, APIs, schemas, DTOs, env dependencies)
- make external system boundaries visible through types or docs

Should:

- document failure modes and exception paths
- include at least one concrete input/output example

### R3. Standard commands

Purpose: let the agent build, test, and run the area without human memory.

Must:

- define canonical install, build, test, lint, and dev commands or clear equivalents
- keep those commands reproducible inside repository conventions

Should:

- provide area-scoped validation commands
- note common failure causes and short workarounds

### R4. Verifiability

Purpose: let the agent close the loop from "changed" to "verified".

Must:

- provide at least one automated validation path
- cover representative task types with tests or repeatable repro steps

Should:

- keep fixtures, seeds, mocks, stories, or snapshots reusable
- include enough regression coverage to catch obvious spillover

### R5. Change locality

Purpose: keep representative work inside a bounded surface area.

Must:

- make the common edit surface observable
- explain when cross-boundary edits are required and why

Should:

- expose the blast radius of shared package changes
- avoid turning a small feature change into a repo-wide edit

### R6. Context economy

Purpose: avoid burning context on always-loaded instructions.

Must:

- keep always-loaded rules short and high signal
- move detail, long examples, and domain explanations into supporting files

Should:

- keep root guidance minimal and common
- place scoped guidance near the work area

Reference budget: root ~100-200 lines, area ~50-150 lines.

### R7. Hierarchical guidance

Purpose: separate global rules from area-specific rules in large repositories.

Must:

- distinguish repository-wide guidance from area-local guidance
- let more specific rules refine broader ones

Should:

- follow a narrowing path such as `root -> app/service -> feature/package`
- keep area-local skills or notes close to the code

### R8. Golden-path examples

Purpose: let the agent learn from living examples instead of abstract rules only.

Must:

- provide at least one canonical or recent example for a representative task type

Should:

- cover recurring tasks (new endpoint, schema change, validation change, page addition)
- point to a good diff, PR, or before/after example

### R9. Knowledge persistence

Purpose: keep learned patterns from disappearing between sessions.

Must:

- externalize recurring patterns, mistakes, and conventions into docs, skills, tests, ADRs, or similar artifacts

Should:

- keep gotchas, known failures, and debug notes structured
- define where new knowledge should be saved after work

### R10. Observability and debug path

Purpose: make failures diagnosable instead of mysterious.

Must:

- identify the main logs, error paths, or state checkpoints for the area

Should:

- provide debug starting points for common failure scenarios
- make env and config mismatches easy to check

### R11. Evaluation readiness

Purpose: ensure the area can be reviewed before and after transformation with the same rubric and proof path.

Must:

- define a lightweight review rubric and proof path for day-to-day work
- keep the same readiness rubric and proof path across before and after snapshots
- preserve enough evidence to justify the score

Should:

- keep proof outputs or equivalent notes when changes matter
- make before/after score deltas easy to explain from visible evidence

## Multi-agent extensions

When several agents may work in parallel on the same area, extend the rules above:

- **R1**: make ownership lanes or starting points for a second agent visible
- **R2**: make handoff surfaces and ownership boundaries visible
- **R5**: make likely conflict hotspots visible when parallel work is expected
- **R9**: preserve handoff notes or shared coordination patterns
- **R10**: keep shared debug starting points visible when one agent may continue another's investigation
- **R11**: preserve enough evidence that another agent can continue without re-discovery

## Operating principles

- Prefer executable verification over narrative claims.
- Prefer area-scoped guidance over repository-wide bulk text.
- Prefer a few high-value artifacts over documentation sprawl.
- Do not treat "more documentation" as improvement by default.
- Measure the before state before claiming the transformation helped.
