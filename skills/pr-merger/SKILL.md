---
name: pr-merger
description: >
  Review, fix, and merge GitHub pull requests end-to-end using GitHub MCP: inspect PR diff/reviews,
  make minimal corrective commits on the PR branch, run relevant tests, comment on what changed
  (with reasoning), merge (usually squash), and close any linked issues. Automatically use when the
  user asks to “check/review PR #…”, “fix this PR so it can merge”, “merge PR …”, “close the issue
  after merging”, or similar PR-triage/merge requests.
---

# PR Merger

## Overview

Make a PR mergeable with minimal, targeted changes; validate locally when possible; then merge and document the work clearly (PR comment + issue closure).

## Workflow

0. Commit local `main` work + sync with `origin/main` (required)
1. Read PR state and intent (GitHub MCP)
2. Reproduce/validate locally (git + tests) when possible
3. Implement fixes on the PR branch (keep scope tight)
4. Add/update tests (or the smallest validation available)
5. Push, summarize, merge, and close linked issues
6. Return local repo to `main`, fully sync, and clean up

### 0) Commit any local work on `main`, then fully sync with `origin/main` (required)

- Start from `main`:
  - `git checkout main`
- If `main` has uncommitted changes, **commit them before doing anything else**:
  - `git status --porcelain`
  - If non-empty: `git add -A && git commit -m "WIP: local changes before PR work"`
    - If this repo has a strong commit-message convention, follow it; otherwise keep it short and factual.
- If there are stashes from earlier work, do **not** drop them silently:
  - Prefer to apply them onto `main` and commit if they apply cleanly.
  - If they don’t apply cleanly (or are clearly obsolete), create a backup branch pointing at the stash commit and keep a note:
    - `git branch backup/stash-<desc> stash@{0}`
    - Only then consider `git stash drop` (after user confirmation, if needed).
- Sync with `origin/main`:
  - `git fetch origin`
  - `git pull --ff-only`
- Confirm sync:
  - `git rev-parse main` equals `git rev-parse origin/main`

If `git pull --ff-only` fails, stop and ask how to proceed (rebase vs merge vs reset). Do not continue PR work from a stale or diverged `main`.

If you created new commits on `main`, push them so local and origin are fully synced:
- `git push origin main`

### 1) Inspect the PR (GitHub MCP first)

- Use MCP to load:
  - PR metadata (`get`) for base/head branches, draft state, linked issues
  - changed files (`get_files`) and the unified diff (`get_diff`)
  - review comments/threads (`get_review_comments`) and PR comments (`get_comments`)
  - CI status (`get_status`) and/or checks if available
- Identify the *minimum* set of changes required to merge (build failure, failing tests, style, missing docs, etc).

### 2) Sync locally (preferred when possible)

- Fetch and checkout the PR branch locally, then diff vs `main`:
  - `git fetch origin pull/<PR_NUMBER>/head:pr-<PR_NUMBER>`
  - `git checkout pr-<PR_NUMBER>`
  - `git diff origin/main...HEAD`
- Run the narrowest tests first, then widen:
  - `./pixiw run -q python -m pytest -q path/to/test.py::test_name`
  - `./pixiw run -q python -m pytest -q`

If local git access isn’t possible, fall back to MCP-only edits:
- Read file contents via MCP
- Push fixes with `push_files` to the PR head branch
- Prefer small, reviewable commits

### 3) Implement fixes (keep scope tight)

- Fix the root cause (not symptoms), but avoid unrelated refactors.
- Keep PR behavior aligned with existing patterns in `main`.
- If the PR drifted significantly from `main`, rebase the PR branch onto `main` (or merge `main` into the PR branch) before final validation.

### 4) Validate

- Add/adjust tests for the bugfix when a nearby test suite exists.
- If validation is impossible (e.g., flaky UI snapshots), document what was run and what remains.

### 5) Comment + merge + close issues (GitHub MCP)

- Add a detailed PR comment that includes:
  - what was broken
  - what changed (files + key logic)
  - why this approach was chosen
  - how it was validated (tests run)
- If PR is draft and ready: mark it ready for review.
- Merge (default: **squash**) with a clear commit title + message.
- Verify linked issues are closed (often auto-closed by “Fixes #…”, but confirm); close manually if not.

### 6) Return local checkout to `main` + delete branch (default)

- Always end by putting the local repo back on `main` and syncing fully:
  - `git checkout main`
  - `git fetch origin`
  - `git pull --ff-only`
- Confirm sync:
  - `git rev-parse main` equals `git rev-parse origin/main`
- Delete the local PR branch by default:
  - `git branch -D pr-<PR_NUMBER>`
- Delete the remote PR branch by default after merge (unless user requests not to):
  - `git push origin --delete <PR_HEAD_BRANCH>`

If the PR is from a fork or branch deletion is restricted, skip deletion and note it in the final summary.

#### PR comment template (copy/paste)

Use as a structure; keep it factual and specific:

```
Summary
- …

What Changed
- `path/to/file.py`: …

Why
- …

Validation
- `./pixiw run -q python -m pytest -q …`
```

## Notes

- Prefer GitHub MCP for PR/issue operations (reading diffs, commenting, merging, closing issues).
- Prefer local execution for tests and conflict resolution when git network access is available.
