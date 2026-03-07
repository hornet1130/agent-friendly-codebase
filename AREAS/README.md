# AREAS

Each work area should usually follow this structure:

```text
AREAS/<area>/
  PROFILE.md
  tasks/
  reports/
  metrics/
```

Meaning:

- `PROFILE.md`: boundary, commands, contracts, examples, and known failures
- `tasks/`: representative tasks used for baseline and transformed comparisons
- `reports/`: human-readable evaluation reports
- `metrics/`: machine-readable numeric inputs for the score script

Prefer names based on features or subsystems.

Good examples:

- `auth-api`
- `checkout-web`
- `shared-http-client`

Bad examples:

- `misc`
- `common`
- `utils2`
