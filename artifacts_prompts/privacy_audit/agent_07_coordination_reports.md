# Privacy Audit - Agent 07 - Coordination Reports

Date: 2026-02-27
Scope: `robotics_maze/coordination/agent_reports/*.md` (50 files, 2006 lines)

## Audit Focus
- Private filesystem paths
- Hostnames and machine-identifying network details
- Usernames / user-identifying local account details
- API keys, tokens, secrets, passwords
- Local environment details that should be sanitized before external sharing

## Findings

### High/Critical
- None.

### Medium
- None.

### Low
1. Local runtime package path and OS fingerprint in sample output.
   - File: `robotics_maze/coordination/agent_reports/task04_backends.md:21`
   - File: `robotics_maze/coordination/agent_reports/task04_backends.md:22`
   - File: `robotics_maze/coordination/agent_reports/task04_backends.md:23`
   - Detail: exposes `.pixi/envs/default/lib/python3.11/site-packages/...` and `darwin` ABI marker.
   - Risk: reveals local stack/runtime characteristics.

2. Local temporary filesystem paths in command examples and artifact locations.
   - File: `robotics_maze/coordination/agent_reports/task10_benchmark_harness.md:39`
   - File: `robotics_maze/coordination/agent_reports/task10_benchmark_harness.md:43`
   - File: `robotics_maze/coordination/agent_reports/task10_benchmark_harness.md:44`
   - File: `robotics_maze/coordination/agent_reports/test_run_log_refresh.md:10`
   - File: `robotics_maze/coordination/agent_reports/test_run_log_refresh.md:15`
   - File: `robotics_maze/coordination/agent_reports/test_run_log_refresh.md:16`
   - Detail: `/tmp/cosimi_*` paths.
   - Risk: low; not user-identifying, but still local-env leakage.

### Informational
1. Machine-context phrasing.
   - File: `robotics_maze/coordination/agent_reports/task32_run_command.md:27`
   - Detail: "tasks on this machine".

2. Workspace-specific runtime schema note.
   - File: `robotics_maze/coordination/agent_reports/task17_facts.md:27`
   - Detail: references workspace schema behavior (`awaiter` role exposure).

## Negative Checks (No Matches Found)
- No private home-directory paths (no `/Users/<name>`, `/home/<name>`, `C:\\Users\\<name>`).
- No hostnames/IP disclosures like `localhost`, `127.0.0.1`, private LAN hosts, or internal FQDNs.
- No local usernames found in report content.
- No API keys/tokens/secrets detected (`sk-*`, `ghp_*`, `AKIA*`, bearer tokens, private key blocks, password assignments).

## Recommended Sanitization
1. Replace environment-specific path details with placeholders, for example `<env_site_packages_path>`.
2. Replace `/tmp/cosimi_*` examples with neutral placeholders, for example `<tmp_output_dir>`.
3. Keep functional command semantics while removing machine-context wording when docs are intended for broad distribution.

## Final Verdict
- Reports are clear of direct credential leakage and direct personal identifiers.
- Residual exposure is limited to low-risk local environment context and can be sanitized with lightweight text edits before external publication.
