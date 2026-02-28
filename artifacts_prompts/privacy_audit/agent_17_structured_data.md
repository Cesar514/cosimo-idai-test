# Structured Data Privacy Audit (Agent 17)

## Scope
- Repository: `cosimi-idai-test`
- File types audited: `*.json`, `*.csv`, `*.yaml`, `*.yml`, `*.toml`
- Total files scanned: `21`

## Method
- Enumerated all structured data files with `rg --files`.
- Ran pattern scans for:
  - absolute filesystem paths (`/Users/...`, `/home/...`, Windows drive paths)
  - credential/secrets markers (`api_key`, `token`, `password`, `private key`, etc.)
  - common PII indicators (email, SSN, phone patterns)
  - URL credential embedding (`https://user:pass@...`)
  - high-entropy/identifier-like strings (UUIDs, long hashes) for manual review
- Performed targeted manual review of sampled file contents, with emphasis on coordination logs and config files.

## Findings

### 1) Low risk: internal agent identifiers present in coordination CSV logs
- Files:
  - `robotics_maze/coordination/session_event_log.csv`
  - `robotics_maze/coordination/agent_task_log.csv`
- Evidence:
  - UUID-like `agent_id` values and workflow metadata are stored in plain text.
- Privacy impact:
  - No direct personal data found, but these identifiers can expose internal workflow/session linkage if exported outside trusted context.

### 2) Informational: integrity hashes appear in logs/manifests
- Files:
  - `robotics_maze/coordination/session_event_log.csv`
  - `paper/ieee_tro_robotics_maze/coordination/figure_manifest.csv`
  - `paper/ieee_tro_robotics_maze/coordination/claims_traceability.csv`
- Evidence:
  - SHA256 checksum strings are present for reproducibility/integrity tracking.
- Privacy impact:
  - Not a secret by itself; acceptable in most repositories.

## No leakage detected for
- Absolute local filesystem paths (macOS/Linux/Windows)
- API keys, access tokens, passwords, private-key material
- Email addresses, SSNs, phone numbers
- Credential-bearing URLs

## Risk Rating
- Overall rating: **Low**

## Recommendations
1. If coordination artifacts are shared externally, sanitize or pseudonymize `agent_id` values first.
2. Keep coordination logs scoped to internal repositories/artifacts when possible.
3. Add a pre-commit structured-data privacy check (regex-based) to block accidental secret/path leakage.
