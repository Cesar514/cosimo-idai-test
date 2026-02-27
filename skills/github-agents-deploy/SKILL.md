---
name: github-agents-deploy
description: GitHub triage + deployment planner for AI agents across issues and pull requests using GitHub MCP only. Use ONLY when the user explicitly invokes "github-agents-deploy". Scans open issues to see which are already being worked by agents, recommends assigning Copilot (low complexity) or Jules (high complexity) within concurrency limits, and scans open PRs to ensure reviews are assigned and optionally request Codex review by commenting "@codex review" (MCP only). Produces a per-issue/per-PR plan first, then executes only after user confirmation.
---

# Github Agents Deploy

## Goal

Inspect the current repo’s open issues and PRs and suggest the best way to “deploy” AI agents (Copilot, Jules, Codex review) without duplicating work or exceeding concurrency limits. Execute assignments only after the user approves the plan.

## Non-negotiables

- Use **only** GitHub MCP tools (`mcp__github__*`) for all GitHub operations (list/search/read/update/comment/assign).
- Do **not** use `gh`, `gitHub.com` web browsing, `curl`, or direct GitHub API calls.
- Before making any changes, show the user an explicit plan grouped by **[ISSUES]** and **[PR]**.
- After executing, report updated remaining capacity for each agent.

## Early exit

- If there are **no open issues** and **no open PRs**, stop after the initial list calls and tell the user there is nothing to do (do not fetch comments/reviews).

## Agent definitions + limits (treat as config)

- **Copilot (issues):** best for lower-complexity issues; capacity **5** concurrent issues.
- **Jules (issues):** best for higher-complexity issues; capacity **10** concurrent issues.
- **Codex (PR reviews):** can review up to **10** PRs concurrently.

If these limits differ in a specific org, the user should tell you; otherwise assume them.

## “Agent already working on it” signals

- **Copilot on an issue:** treat as “in progress” if the issue is assigned to Copilot (assignee login matches the Copilot SWE agent bot, e.g. `copilot-swe-agent`), or if comments include an explicit `@copilot` deployment/acknowledgement.
- **Jules on an issue:** treat as “in progress” if the issue has the label `jules`.
- **Codex on a PR:** treat as “in progress” if PR comments include `@codex review` or if there is already a Codex review present.

If the repo uses different conventions (different label name, different mention text), ask the user before proceeding.

## “Agent stopped working” heuristics (best-effort)

GitHub MCP does not expose the full Copilot/Jules session UI. Use only repo-visible artifacts to infer state:

- **Copilot on an issue**
  - **In progress:** still assigned to the Copilot bot (`copilot-swe-agent`), or recent bot activity.
  - **Handoff/completed:** a PR exists authored by the Copilot bot that references/closes the issue (search PRs by issue number; prefer `mcp__github__search_pull_requests`).
  - **Stalled/unknown:** Copilot was previously deployed (marker comment exists) but the issue is no longer assigned to the Copilot bot and there is no related PR.
- **Jules on an issue**
  - **In progress:** `jules` label present.
  - **Stalled/unknown:** marker comment exists but `jules` label is not present (do not re-deploy by default).
- **Codex on a PR**
  - **In progress:** `@codex review` comment exists but no Codex review yet.
  - **Completed:** a Codex review exists (`mcp__github__pull_request_read` `get_reviews`).
  - **Stalled/unknown:** `@codex review` exists but there is no Codex review after a long time; do not re-request unless user explicitly asks.

## Workflow

### 0) Confirm explicit invocation

If the user did not explicitly request `github-agents-deploy` by name, stop and ask them to confirm they want this skill to run (and which `owner/repo`).

### 1) Identify target GitHub repo (owner/repo)

- If you are running inside the repo, infer from git remote (local inspection is OK; no GitHub calls needed).
- Otherwise ask the user for `owner` + `repo`.

### 2) Pull current workload via GitHub MCP

First, fetch lists only (cheap):

- Open issues: `mcp__github__list_issues` (`state: open`)
- Open PRs: `mcp__github__list_pull_requests` (`state: open`)

If both lists are empty: exit early (no further checks).

Then, fetch details only as needed:

**Issues (details)**
- For each issue that might be a candidate for deployment (i.e., not obviously already in progress by a human/agent), fetch:
  - comments: `mcp__github__issue_read` `method: get_comments` (scan for `@copilot`, `<!-- agent-deploy: ... -->`, or other agent markers)
  - labels: `mcp__github__issue_read` `method: get_labels` (if labels are not already available)

Compute:
- `copilot_in_flight`: count open issues that match Copilot “in progress” signals
- `jules_in_flight`: count open issues labeled `jules`
- remaining capacity:
  - `copilot_remaining = 5 - copilot_in_flight`
  - `jules_remaining = 10 - jules_in_flight`

**Pull requests (details)**
- For each PR that might need review assignment, fetch:
  - `mcp__github__pull_request_read` `method: get`
  - `mcp__github__pull_request_read` `method: get_comments` (scan for `@codex review`)
  - `mcp__github__pull_request_read` `method: get_reviews` (detect Codex review completion)

Compute:
- `codex_in_flight`: count open PRs that already have `@codex review` comment or existing Codex review
- `codex_remaining = 10 - codex_in_flight`

### 3) Classify issue complexity (to choose Copilot vs Jules)

Use a simple rubric (best-effort, evidence-based):
- **Low complexity (Copilot):** clearly-scoped, limited blast radius, docs/tests/chore, “good first issue”, small bugfix, small config tweak.
- **High complexity (Jules):** cross-cutting refactors, architecture changes, concurrency/race conditions, performance, large scope, unclear requirements, many comments, or touching multiple subsystems.

### 4) Draft a deployment plan (no changes yet)

Output **exactly**:

`[ISSUES]`
- `i1 {issue_number} "{issue_title}" will get assigned to {copilot|jules|none} because {reason}`
- …

`[PR]`
- `p1 {pr_number} "{pr_title}" will be assigned to codex for review because {reason}`
- …

Then:
- `You have X copilot, Y jules, and Z codex agents still available to use.`

Ask the user which to implement:
- `all`, or
- a list of issue IDs/pr IDs (e.g. `i1,i3,p2`), or
- ranges (e.g. `i2-i5`).

### 5) Execute approved actions via GitHub MCP only

#### “Previously deployed agent” rule (must follow)

Never deploy an agent to an issue/PR that has **previously used an agent** unless the user explicitly tells you to re-deploy on that specific item.

Detect “previously used an agent” via durable markers:
- Issues: comments containing `<!-- agent-deploy: copilot -->` or `<!-- agent-deploy: jules -->`, or an assignee matching the Copilot bot, or the `jules` label.
- PRs: comments containing `@codex review`.

If an agent appears to have stopped/stalled:
- Do **not** assign a different agent as a “retry” by default.
- Instead, report it as “stalled after agent deployment” and recommend a human follow-up or explicit “re-deploy” instruction.

**Copilot assignment**
- Prefer the dedicated tool: `mcp__github__assign_copilot_to_issue` for each selected issue.
- After assigning, add a durable marker comment with `mcp__github__add_issue_comment`:
  - Include `<!-- agent-deploy: copilot -->`
  - Include a short human-readable line like `Deployed Copilot to this issue.`

**Jules assignment (label-based)**
- Ensure the `jules` label exists via `mcp__github__get_label`.
- Add the `jules` label by:
  - reading current labels, then
  - updating issue labels via `mcp__github__issue_write` (`method: update`) with the union of labels (do not drop existing labels).
- After labeling, add a durable marker comment with `mcp__github__add_issue_comment`:
  - Include `<!-- agent-deploy: jules -->`
  - Include a short human-readable line like `Deployed Jules to this issue via label.`

**Codex PR review request**
- Before commenting, confirm the PR does not already have `@codex review` in comments.
- If not present, add a PR comment using `mcp__github__add_issue_comment` with body exactly `@codex review`.

### 6) Report results + remaining capacity

After changes, re-compute remaining capacity (or update counts based on actions taken) and print:
- `At the moment you have X copilot, Y jules, and Z codex agents still available to use.`

If you need reminders about assumptions/conventions, load `references/notes.md`.
