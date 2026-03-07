# AREA PROFILE

## 1. Identity

- Area ID: auth-api
- Human name: Authentication API module
- Primary paths: `apps/api/src/modules/auth`
- Non-goals / out of scope: billing, notifications, unrelated shared infrastructure

## 2. Why this area matters

- Business purpose: login, token refresh, and session management
- Typical requests received in this area: login bug fixes, guard changes, DTO validation additions
- Why this area is a good benchmark target: it combines API contracts, validation, tests, and shared auth logic in one bounded area

## 3. Entrypoints

- HTTP/API entrypoints: auth controller routes
- Job/queue entrypoints: none
- CLI/script entrypoints: area-local test command

## 4. Key contracts

- Public API / route: login, refresh, logout, sessions
- DTO / schema / zod / class-validator: login DTO, refresh DTO
- Shared package contracts: auth token utilities, user session types
- External services: user repository, token signing service
- Required env vars: JWT secret, session TTL

## 5. Canonical commands

- install: `pnpm install`
- build: `pnpm turbo run build --filter=api`
- lint: `pnpm turbo run lint --filter=api`
- test: `pnpm turbo run test --filter=api`
- test (area-only): `pnpm --filter api test auth`
- dev: `pnpm turbo run dev --filter=api`
- e2e: `pnpm --filter api test:e2e auth`

## 6. Typical change types

- Bug fix: adjust refresh-token validation
- Feature add: add session list retrieval
- Refactor: split guard and service responsibilities
- Validation / schema change: add a DTO field
- Test hardening: add an auth edge-case fixture

## 7. Common files touched

- Hot files: auth controller, auth service, auth DTOs, auth tests
- Supporting files: token utilities, shared types
- Dangerous shared files: shared auth contract package

## 8. Verification

- Fastest proof command: `pnpm --filter api test auth`
- Full proof command: `pnpm turbo run test --filter=api`
- Known flaky tests: none documented yet
- Manual checks still required: confirm refresh flow when local env values differ

## 9. Known failure patterns

- missing DTO validation
- JWT secret mismatch across environments
- shared contract updates without downstream test updates

## 10. Golden path examples

- Example PR / commit / file path 1: add a login failure error code
- Example PR / commit / file path 2: split session service from auth service

## 11. Current AI-readiness gaps

- the area-only test command is known informally but not surfaced everywhere it should be
- session-management contract examples are too thin
- common failure notes are not stored in a structured location
