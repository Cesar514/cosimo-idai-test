# Example output (abridged)

1) **What I reviewed**
- Looked at `README.md`, `package.json`, `tsconfig.json`
- Searched for `TODO`/`FIXME` and obvious duplication
- Checked available `npm` scripts and lint/format configs

2) **Top suggestions (max 10)**

**1. [★★★] Consolidate duplicate config and enforce formatting in CI (Effort: M, Risk: Low)**
- **Why (evidence):** multiple formatter configs and inconsistent formatting in `src/` files.
- **What to do:** pick one formatter config, add a single `format:check` script, run it in CI.
- **Where:** formatter config files; CI workflow; `package.json` scripts.
- **How to validate:** run `npm run format:check` and ensure CI passes.

**2. [★] Remove unused exports and dead code paths (Effort: S, Risk: Low)**
- **Why (evidence):** unused exports in `src/utils/*` and unused dependencies in `package.json`.
- **What to do:** delete unused exports, remove unused deps, rerun typecheck/tests.
- **Where:** `src/utils/`, `package.json`.
- **How to validate:** `npm test` (or the project’s test command) and a clean typecheck.

> Which of this suggestion would you like me to publish to github as issues?

1. [★★★] Consolidate duplicate config and enforce formatting in CI
2. [★] Remove unused exports and dead code paths

## Example GitHub issue body (for suggestion 1)

## Summary
Consolidate formatter/linter configuration and enforce a single formatting check in CI to prevent churn and improve reviewability.

## Why this matters
- Reduces noisy diffs and review time.
- Prevents style regressions and “works on my machine” formatting differences.

## Evidence
- Multiple formatting-related configs detected (see repo config files).
- Formatting inconsistencies observed in `src/` during spot-checks.

## Proposed approach
1. Pick a single formatter config (document the choice in `README.md` or `CONTRIBUTING.md`).
2. Add `format` and `format:check` scripts that run deterministically.
3. Run `format:check` in CI on every PR.
4. (Optional) Add a pre-commit hook to run `format` on staged files.

## Acceptance criteria
- CI fails when formatting differs from the configured standard.
- Running `format` locally produces no diff after a second run (idempotent).

## Validation
- `npm run format:check`
- `npm test` (or project test command)
