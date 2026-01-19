# Contributing

## Creating a new spec

1. Copy `specs/TEMPLATE.md` to `specs/{feature-domain}/spec.md` (use kebab-case for the feature domain, e.g. `user-authentication`, `payment-processing`).
2. Replace all placeholders with your feature’s context, architecture, anti-patterns, definition of done, regression guardrails, and Gherkin scenarios.
3. See `specs/README.md` for **when to create** a spec, **when to update** it, and the **Same-Commit Rule**: if code changes behavior or contracts, update the spec in the same commit.

## Schema validation

If you change files in `commands/` or `mcps/`, run before committing:

```bash
python schemas/validate_all.py
```

CI runs this on pull requests; passing locally avoids validation failures.

## Pull requests

- Link PRs to the relevant Jira or GitHub issue.
- When behavior or contracts change, **update the spec in the same commit** as the code (see `specs/README.md`).
- Ensure `python schemas/validate_all.py` passes when `commands/` or `mcps/` are modified.
