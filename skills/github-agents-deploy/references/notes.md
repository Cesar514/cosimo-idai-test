# Notes (implementation assumptions)

## Copilot issue assignment
- Prefer using the GitHub MCP tool `mcp__github__assign_copilot_to_issue` to deploy Copilot to an issue.
- When detecting “already in progress”, look for Copilot as an assignee (commonly `copilot-swe-agent`) and/or explicit `@copilot` comments.
- If the issue is no longer assigned to Copilot but has an agent-deploy marker comment, treat it as “previously deployed” and do not re-deploy unless explicitly requested.

## Jules issue assignment
- This skill assumes “Jules” is triggered by the presence of a `jules` label on an issue (org-specific convention).
- Since GitHub MCP does not include a label-create tool, ensure the label exists before attempting to apply it.
- Add a durable marker comment when assigning Jules so future runs can detect prior deployments even if the label is later removed.

## Codex PR review assignment
- This skill assumes the repo has an integration that triggers a Codex review when a PR comment contains exactly `@codex review`.
- To avoid duplicate requests, check PR comments for that exact string before posting.
- Treat the presence of a Codex review (from `get_reviews`) as “completed”; do not re-request unless explicitly asked.
