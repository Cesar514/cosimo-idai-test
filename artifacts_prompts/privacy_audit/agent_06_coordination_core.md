# Privacy Audit: Coordination Core (`robotics_maze/coordination/`)

Date: 2026-02-27
Owner scope: `robotics_maze/coordination/` (excluding `robotics_maze/coordination/agent_reports/`)

## Executive Summary

- No direct secrets found (no API keys, passwords, private keys, bearer tokens, emails, phone numbers, or machine-local absolute paths).
- Multiple machine/session fingerprint vectors are present in coordination logs and dashboard notes.
- Overall risk: **moderate** for internal logs shared outside the trusted team.

## Findings

### F1 (Medium): Persistent agent/session UUIDs enable cross-log correlation

Stable UUID-like IDs appear repeatedly and can be used to correlate workstreams across files and sessions.

Evidence:
- `robotics_maze/coordination/session_event_log.csv:36`
- `robotics_maze/coordination/session_event_log.csv:64`
- `robotics_maze/coordination/agent_task_log.csv:4`
- `robotics_maze/coordination/agent_task_log.csv:29`
- `robotics_maze/coordination/AGENT_DASHBOARD.md:10`
- `robotics_maze/coordination/AGENT_DASHBOARD.md:35`

Recommended handling:
- Replace persisted agent IDs with per-export pseudonyms (for example `agent_A`, `agent_B`).
- Keep real IDs only in a restricted internal map.

### F2 (Medium): Account/repository identifiers expose owner identity context

Logs/notes reference a specific account/repo namespace and issue URLs, creating direct project-owner linkage.

Evidence:
- `robotics_maze/coordination/session_event_log.csv:47`
- `robotics_maze/coordination/session_event_log.csv:79`
- `robotics_maze/coordination/BACKLOG_SUMMARY.md:4`
- `robotics_maze/coordination/BACKLOG_SUMMARY.md:10`

Recommended handling:
- Redact exported owner/repo strings to placeholders (for example `ORG/REPO`).
- Keep issue numbers, but strip full URL host + namespace in public artifacts.

### F3 (Low): High-precision timestamps and timezone fragments leak workflow fingerprint

Exact second-level UTC timestamps and timezone offset fragments can fingerprint working cadence and locale hints.

Evidence:
- `robotics_maze/coordination/session_event_log.csv:20`
- `robotics_maze/coordination/session_event_log.csv:35`
- `robotics_maze/coordination/session_event_log.csv:79`
- `robotics_maze/coordination/SESSION_TIMELINE.md:22`
- `robotics_maze/coordination/SESSION_TIMELINE.md:46`

Recommended handling:
- For externally shared logs, coarsen to date or hour buckets.
- Remove partial timezone strings like `-05:00` unless operationally required.

### F4 (Low): Environment/toolchain markers reveal host profile details

Operational notes include stack/OS clues that can contribute to fingerprinting when combined with other metadata.

Evidence:
- `robotics_maze/coordination/session_event_log.csv:39`
- `robotics_maze/coordination/session_event_log.csv:52`
- `robotics_maze/coordination/SESSION_TIMELINE.md:28`

Recommended handling:
- Keep failure class (`dependency install failure`) but drop specific OS/toolchain details in external exports.

## Explicit Non-Findings

- No machine-local absolute paths found (`/Users/...`, `/home/...`, Windows home paths).
- No credential-like material found (API keys, passwords, tokens, private keys).
- No direct personal contact identifiers found (email/phone).

## Suggested Redaction Profile for External Sharing

1. Replace all UUIDs with one-time aliases per document.
2. Replace owner/repo namespace and GitHub URLs with placeholders.
3. Coarsen timestamps to day-level unless exact timing is necessary.
4. Remove environment-specific strings (`macOS`, detailed toolchain notes).

