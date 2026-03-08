# Go Service Reference

Use this reference when the target area belongs to a Go service, package, or backend module.

## Good fit signals

- `go.mod` at the repo root or service root
- `cmd/`, `internal/`, `pkg/`, or `api/` directories
- tests run with `go test`
- contracts expressed through handlers, structs, interfaces, or protobuf/OpenAPI artifacts

## Work-area heuristics

- Prefer a bounded package or vertical slice, not the whole service.
- Identify entrypoints in `cmd/` or HTTP/router registration early.
- Separate domain package changes from transport or infra changes in the profile.

Good examples:

- `internal/auth`
- `internal/orders`
- `pkg/httpclient`

## Common contract surfaces

- HTTP handlers and router wiring
- request and response structs
- interfaces used as ports
- protobuf or OpenAPI generated contracts
- config structs and env parsing

## Common command patterns

- install: `go mod download`
- build: `go build ./...`
- test: `go test ./...`
- area-local test: `go test ./internal/auth/...`
- lint: project-specific, often `golangci-lint run`

## Common blast-radius risks

- shared interface changes
- generated client or server code drift
- config struct changes
- package import cycles introduced by refactors

## Exploration hints worth storing

- starting packages and router registration points
- grep seeds such as handler names, struct names, or config keys
- package dependency direction for the area
