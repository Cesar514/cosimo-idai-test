---
name: suggest-improve
description: Deep codebase optimization review that produces up to 10 ranked, actionable suggestions (no new features) to improve maintainability, performance, reliability, security, and developer experience. Use when the user asks to refactor/clean up/optimize a repository, reduce tech debt, improve tests/linting/typing, speed up builds, simplify architecture, remove duplication, or do a general "codebase health check" without shipping new product functionality.
---

# Suggest Improve

## Goal

Perform a structured, evidence-based review of an existing codebase and return **up to 10** concrete improvement suggestions ranked **★ to ★★★** (★★★ = highest-impact).

## Guardrails (must follow)

- Do **not** implement changes unless the user explicitly asks you to (this skill is “suggestions only”).
- Do **not** propose new product features or behavior changes (bug fixes are OK only if clearly correctness/safety and not “new functionality”).
- Prefer recommendations that are **observable** in the repo (cite file paths, configs, commands run, or specific patterns).
- Avoid speculative micro-optimizations; focus on high-leverage improvements.
- If you need to interact with GitHub (issues/search/list/create), use **only** GitHub MCP tools (`mcp__github__*`). Do **not** use `gh`, `curl`, direct GitHub API calls, or web browsing for GitHub operations.

## Workflow

### 0) (Optional) De-duplicate against existing GitHub issues

Do this step first **only if** GitHub MCP tools are available (tools named like `mcp__github__*`) **and** you can determine the target GitHub repo (owner/name).

- Determine `owner` + `repo`:
  - Prefer parsing the local git remote URL (usually `origin`) to infer `owner/repo`.
  - If you can’t infer it confidently, ask the user for `owner` + `repo`.
- Pull existing issues to avoid repeating suggestions:
  - Prefer `mcp__github__list_issues` for a first pass (open issues, most recent; paginate if needed).
  - For each potential suggestion title/keywords, run `mcp__github__search_issues` to find related issues (e.g., “eslint”, “flaky tests”, “typecheck”, module names).
- Use findings:
  - If an existing issue already covers the suggestion, either skip it or reframe as an incremental follow-up.
  - When you keep a suggestion that overlaps, explicitly link it to the existing issue in the suggestion’s **Why (evidence)**.

### 1) Collect “signals” quickly (read-only)

Prefer running the bundled script; fall back to manual commands if needed.

**Option A (preferred):** run the signal collector script

- Run `python3 scripts/collect_repo_signals.py --format md` from this skill folder, or run it by absolute path if you can locate the skill install directory.
- If the repo is huge, add `--max-files 50000` (or smaller) to keep it snappy.

**Option B (manual):** minimally capture

- Repo entry points: `README*`, `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod`, `tsconfig.json`, CI config.
- Test/lint/typecheck/build commands available (from `package.json` scripts or project docs).
- “Hotspots”: biggest directories/files, obvious duplication, TODO/FIXME density.
- Dependency/tooling posture: formatter, linter, type checker, test runner, security scanning.

### 2) Deep-dive on the top 3–5 opportunities

Pick a few areas with the best ROI, such as:

- Repeated patterns / duplicated utilities
- “God files” (large, many responsibilities)
- Error handling and boundaries between layers
- Type safety gaps, nullability, unsafe casts, `any`
- Performance hotspots (heavy loops, unnecessary re-renders, N+1 calls, expensive startup work)
- Tests: flaky/slow, missing unit tests for core logic, missing contract tests, missing fixtures
- Tooling: lint/format inconsistencies, CI gaps, missing pre-commit, slow builds

Keep notes tied to evidence (paths, snippets, commands).

### 3) Produce up to 10 ranked suggestions

Each suggestion must be:

- **Actionable** (what to change, where, how to validate)
- **Scoped** (no sweeping rewrites unless clearly justified)
- **Ranked** (★ / ★★ / ★★★)
- **Non-feature** (optimization/quality only)

## Star ranking rubric

- ★★★ High-impact, high-confidence improvements with clear evidence and a good cost/benefit ratio (often: reliability, build/test speed, removing systemic duplication, tightening boundaries, security posture).
- ★★ Solid medium-impact improvements (often: refactors that reduce complexity, improve APIs, add missing tests for core logic, docs/architecture clarity).
- ★ Small/local improvements that are still worthwhile but not transformative (often: minor cleanup, small perf wins, naming, small config tweaks).

## Output format (use exactly)

Start with:

1) **What I reviewed**: 3–8 bullets (commands run, files examined, constraints/assumptions).
2) **Top suggestions (max 10)**: numbered list, each item formatted as:

**N. [★/★★/★★★] Title (Effort: S/M/L, Risk: Low/Med/High)**
- **Why (evidence):** cite concrete repo evidence (paths/patterns/configs).
- **What to do:** concise steps; prefer “do X, then Y”.
- **Where:** file(s)/directories/modules to touch.
- **How to validate:** exact command(s) or checks.

End with (optional):

- **Quick wins I intentionally skipped:** 1–3 bullets (only if relevant).
- **Follow-up questions:** only if truly blocking higher-quality suggestions.

If you need a quick reference for formatting, load `references/example-output.md`.

## GitHub issue publishing (optional, requires GitHub MCP)

If GitHub MCP tools are available and you know the target `owner` + `repo`, add this **exact** question at the very end of your answer (after the suggestions):

> Which of this suggestion would you like me to publish to github as issues?

Then include the list of suggestions (numbered 1..N) so the user can reply with:
- `all`, or
- a list like `1,3,4`, or
- ranges like `2-5` (interpret inclusive ranges).

### Follow-up turn behavior (after user answers)

When the user selects suggestions to publish:
- Create **one GitHub issue per selected suggestion** using `mcp__github__issue_write` (`method: create`).
- Titles: keep short; include the star rating prefix, e.g. `★★★ Tighten TypeScript boundaries in src/...`.
- Bodies: make them **as detailed as possible** so a new contributor can understand the context and fix path without extra back-and-forth. Reuse the suggestion content and expand it into a full issue write-up (see template below). Include any related existing issue numbers you found.
- Do not create duplicates:
  - Before creating each issue, run `mcp__github__search_issues` with the title keywords; if a near-duplicate exists, ask whether to skip or link as a comment instead.
- Never publish issues via any non-MCP mechanism (no `gh`, no `curl`, no direct HTTP calls).

#### Issue body template (use Markdown headings)

Use this structure (fill everything that applies):

- `## Summary`
- `## Why this matters`
  - Impact (DX/bugs/perf/security/maintainability) and who it affects
- `## Evidence`
  - Concrete pointers: file paths, symbols, snippets (short), configs, logs, or signal outputs
  - Links to related issues (if any): `#123`
- `## Proposed approach`
  - Step-by-step changes; include 1–2 alternative approaches if there are tradeoffs
  - Call out risks/edge cases and mitigations
- `## Acceptance criteria`
  - Bullet list of “done means…” (observable outcomes)
- `## Validation`
  - Exact commands/checks to run (tests, lint, typecheck, build, benchmarks if relevant)
- `## Notes`
  - Optional: estimated effort (S/M/L), rollout plan, follow-ups
