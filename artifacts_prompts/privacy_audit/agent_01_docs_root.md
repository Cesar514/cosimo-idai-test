# Privacy Audit Report - Agent 01 (Docs Root Scope)

## Scope
- `README.md`
- `CHANGELOG_SESSION.md`
- `docs/` (recursive)

## Findings

### 1. Potential username exposure
- **File/line:** `CHANGELOG_SESSION.md:121`
- **Evidence:** `Cesar514/cosimo-idai-test`
- **Why it matters:** `Cesar514` appears to be an individual username and may be considered identifying information.
- **Severity:** Low

## Checks with no leaks found
- Absolute local filesystem paths (for example `/Users/...`, `/home/...`, Windows drive paths): **none found**
- Email addresses: **none found**
- Secrets/tokens/key signatures (for example `AKIA...`, `ghp_...`, `github_pat_...`, `sk-...`, private key blocks): **none found**
- Machine-specific host/runtime fingerprints: **none found**

## Status
- **Not fully clean** due to the username exposure candidate above.
