# Agent 14 Path Pattern Privacy Audit

## Scope
- Repository-wide text scan under `.` (including hidden files, excluding `.git`).
- Pattern classes scanned:
  - Absolute Unix home paths: `/Users/<...>`, `/home/<...>`
  - Windows absolute paths: `C:\...` style
  - Home traces: `~/`, `$HOME`, `${HOME}`, `%USERPROFILE%`, `%HOMEPATH%`, `%APPDATA%`
  - Machine-specific local dirs: `/tmp/...`, `/var/folders/...`, `/private/var/...`, `/opt/homebrew/...`, `/Volumes/...`, `/mnt/...`
- Constraint followed: no source files modified; only this report written.

## Summary
- Concrete user-home absolute paths were found, but only inside existing `artifacts_prompts/privacy_audit/` reports.
- No concrete `/Users/<name>` or `/home/<name>` paths were found outside prior audit artifacts.
- Non-audit machine-local paths were found in robotics testing/checklist/report docs, all under `/tmp/...`.
- No non-audit Windows absolute paths, no non-audit `~/` or `$HOME` traces, and no `file:///` hits.

## Counts
- Global `/Users` or `/home` matches: 17 matches across 12 files.
- Global concrete `/Users/<name>` or `/home/<name>` matches: 8 matches across 6 files.
- Global machine-local dir matches (`/tmp`, `/var/folders`, `/private/var`, `/opt/homebrew`, `/Volumes`, `/mnt`): 32 matches across 6 files.
- Global Windows absolute path matches: 7 matches across 6 files.
- Global `~/` or `$HOME`/equivalents matches: 1 match in 1 file.
- Non-audit concrete `/Users` or `/home` matches: 0.
- Non-audit machine-local dir matches: 16 matches across 4 files.
- Non-audit Windows absolute path matches: 0.
- Non-audit `~/`/`$HOME`/equivalents matches: 0.

## Findings

### 1) Concrete user-home absolute paths (audit-artifact only)
All concrete user-home paths below are in prior audit docs, not in active source/testing scripts outside `artifacts_prompts/privacy_audit/`:

- `artifacts_prompts/privacy_audit/agent_05_robotics_src.md:13`
- `artifacts_prompts/privacy_audit/agent_10_paper_coordination.md:32`
- `artifacts_prompts/privacy_audit/agent_10_paper_coordination.md:34`
- `artifacts_prompts/privacy_audit/agent_10_paper_coordination.md:36`
- `artifacts_prompts/privacy_audit/agent_12_secret_patterns.md:4`
- `artifacts_prompts/privacy_audit/agent_15_network_endpoints.md:4`
- `artifacts_prompts/privacy_audit/agent_16_media_metadata.md:4`
- `artifacts_prompts/privacy_audit/agent_18_dotfiles_config.md:4`

### 2) Non-audit machine-specific local paths (`/tmp/...`)
Concrete `/tmp/...` paths appear in test logs/checklists and coordination reports:

- `robotics_maze/testing/SIM_QA_CHECKLIST.md:92`
- `robotics_maze/testing/SIM_QA_CHECKLIST.md:102`
- `robotics_maze/testing/SIM_QA_CHECKLIST.md:124`
- `robotics_maze/testing/SIM_QA_CHECKLIST.md:131`
- `robotics_maze/testing/TEST_RUN_LOG.md:167`
- `robotics_maze/testing/TEST_RUN_LOG.md:172`
- `robotics_maze/testing/TEST_RUN_LOG.md:173`
- `robotics_maze/testing/TEST_RUN_LOG.md:184`
- `robotics_maze/testing/TEST_RUN_LOG.md:185`
- `robotics_maze/testing/TEST_RUN_LOG.md:219`
- `robotics_maze/coordination/agent_reports/test_run_log_refresh.md:10`
- `robotics_maze/coordination/agent_reports/test_run_log_refresh.md:15`
- `robotics_maze/coordination/agent_reports/test_run_log_refresh.md:16`
- `robotics_maze/coordination/agent_reports/task10_benchmark_harness.md:39`
- `robotics_maze/coordination/agent_reports/task10_benchmark_harness.md:43`
- `robotics_maze/coordination/agent_reports/task10_benchmark_harness.md:44`

### 3) Windows-style and home-trace patterns
- Windows absolute path syntax matches are placeholder/example strings in existing privacy audit docs (for example `C:\Users\...`), not concrete machine paths in non-audit files.
- `~/...` appears once as a placeholder/example in `artifacts_prompts/privacy_audit/agent_10_paper_coordination.md:18`.
- No `$HOME`, `${HOME}`, `%USERPROFILE%`, `%HOMEPATH%`, `%APPDATA%` hits in non-audit files.

## Risk Note
- Current non-audit leakage is low-to-moderate and operational (temporary local paths in logs/docs), not direct user-home identity leakage.
