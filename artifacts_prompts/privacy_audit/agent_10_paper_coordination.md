# Privacy Audit Report: `paper/ieee_tro_robotics_maze/coordination/` and `paper/ieee_tro_robotics_maze/submission/`

## Scope
- Audited directories:
  - `paper/ieee_tro_robotics_maze/coordination/`
  - `paper/ieee_tro_robotics_maze/submission/`
- File classes audited:
  - metadata/text artifacts (`.md`, `.bib`, `.csv`, `.tex`, `.txt`, `.yml`, `.yaml`, `.json`, `.xml`)
  - text extracted from submission PDF
  - text/metadata inside `ieee_tro_robotics_maze_source.zip`
- Constraints followed:
  - no source files modified
  - output written only to this report file

## Method
- Enumerated files in scope.
- Ran regex scans for:
  - private filesystem paths (`/Users/...`, `/home/...`, `C:\Users\...`, `~/...`)
  - username indicators (`cesar514`, path-embedded usernames)
  - secrets/tokens (`api key`, `secret`, `token`, `password`, `ghp_...`, `github_pat_...`, `sk-...`, `AKIA...`)
  - email addresses
- Inspected:
  - `submission/ieee_tro_robotics_maze_main.pdf` text via `pdftotext`
  - extracted text/metadata files from `submission/ieee_tro_robotics_maze_source.zip`

## Findings

### 1. Direct private path + username leakage in submission source ZIP
The packaged source ZIP contains hard-coded absolute local paths with the local username (`cesar514`):

- `ieee_tro_robotics_maze_source.zip::coordination/agent_reports/build_audit_awaiter.md:33`
  - ``python3 /Users/cesar514/.codex/skills/paper-forge/scripts/paperforge.py audit --root paper/ieee_tro_robotics_maze``
- `ieee_tro_robotics_maze_source.zip::coordination/agent_reports/build_audit_awaiter.md:39`
  - ``Paper Forge audit: /Users/cesar514/Documents/agent_programming/cosimi-idai-test/paper/ieee_tro_robotics_maze``
- `ieee_tro_robotics_maze_source.zip::coordination/agent_reports/final_qa_awaiter.md:23`
  - ``python3 /Users/cesar514/.codex/skills/paper-forge/scripts/paperforge.py audit --root paper/ieee_tro_robotics_maze``

Impact:
- Exposes local OS username and workstation directory layout in distributed submission artifacts.

Severity:
- **Medium** (privacy/identity metadata leakage; not credential leakage).

### 2. No credential/secret leakage found
- No high-confidence API keys, auth tokens, passwords, or cloud credential signatures detected in scoped text/metadata files.
- No secret-like matches detected in extracted PDF text.

### 3. No additional username/email leakage found outside ZIP findings
- No email-address leakage detected in scoped text/metadata files.
- No `/Users/...` or `/home/...` paths detected in the live `coordination/` working-tree text files during this audit.

## Risk Assessment
- Overall risk: **Medium** due to username/path disclosure in the submission source ZIP.
- Credential compromise risk: **Low** (no secrets detected).

## Recommended Remediation
- Regenerate `ieee_tro_robotics_maze_source.zip` after sanitizing embedded coordination logs/reports:
  - Replace absolute paths with relative placeholders (for example: `<LOCAL_CODEX_HOME>`, `<REPO_ROOT>`).
  - Remove local machine usernames from command transcripts.
- Add a pre-packaging grep check on submission bundles for:
  - `/Users/`
  - `/home/`
  - `C:\Users\`
  - known username strings

## Final Verdict
- **Fail (privacy hygiene)** for distribution readiness of current `ieee_tro_robotics_maze_source.zip` due to identifiable local path leakage.
- **Pass (secret hygiene)** for credential/token exposure in audited scope.
