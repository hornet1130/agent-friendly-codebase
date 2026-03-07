# Node Monorepo Reference

Use this reference when the target repository looks like a JavaScript or TypeScript monorepo with app and package boundaries.

## Good fit signals

- top-level `apps/` and `packages/`
- `pnpm`, `turbo`, `npm workspaces`, or `yarn workspaces`
- framework split such as web app plus API service
- shared packages used across multiple apps

## Work-area heuristics

- Prefer one feature or module, not the whole app.
- Name both the primary path and the shared package blast radius.
- Keep app-local and shared-package changes separate in the profile.

Good examples:

- `apps/web/src/features/checkout`
- `apps/api/src/modules/auth`
- `packages/shared/http-client`

## Common contract surfaces

- route handlers, controllers, API schemas
- DTOs, validators, Zod schemas, TypeScript interfaces
- environment variables and config loaders
- shared package exports and public entrypoints

## Common command patterns

- install: `pnpm install`
- build app: `pnpm turbo run build --filter=<app>`
- test app: `pnpm turbo run test --filter=<app>`
- lint app: `pnpm turbo run lint --filter=<app>`
- area-local test: app-specific test command scoped to the feature or module

## Common blast-radius risks

- shared package export changes
- env/config shape changes
- schema drift across frontend and backend
- generated types or codegen outputs going stale

## Exploration hints worth storing

- hottest app-local files
- shared packages most likely to be touched
- search seeds such as route names, DTO names, feature names, or env keys
