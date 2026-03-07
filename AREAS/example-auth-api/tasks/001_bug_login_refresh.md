# TASK

- Task ID: auth-api-001
- Area ID: auth-api
- Type: bug-fix
- Difficulty: medium

## Problem statement

The refresh token is not expired, but some users still receive `401` responses. Fix the session-validation path.

## Scope

- In scope: auth refresh flow, relevant DTOs, service logic, and tests
- Out of scope: login UI, billing, unrelated shared configuration

## Expected relevant files

- `apps/api/src/modules/auth/*`
- `packages/shared/auth-contract/*`
- `apps/api/test/auth/*`

## Validation

- Target command: `pnpm --filter api test auth`
- Success oracle: reproduce the refresh-related failure, fix it, and keep existing auth tests green
- Regression check: `pnpm turbo run test --filter=api`
- Preferred grader: code-based
- Evidence to capture: failing test output, passing test output, changed files, regression command result

## Gold patch or human reference

- PR / commit / diff reference: `TBD from history`

## Notes

- Why this task is representative: it touches DTOs, service logic, shared contracts, and tests together
- Why this task is hard for agents: the visible surface is small, but contract mismatches are easy to miss
