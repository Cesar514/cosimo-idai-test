# Agent 19: Cryptographic/Auth Material Scan

Date: 2026-02-27
Scope: Full repository scan (excluding `.git/`, `node_modules/`, and prior audit output under `artifacts_prompts/` to avoid recursive keyword hits).

## Objective
Identify potential cryptographic/authentication material in-repo:
- Certificate/private-key blocks
- SSH keys
- Bearer tokens
- Cookies / `Set-Cookie` headers
- Auth headers and token-like literals

## Methods
Used `rg` pattern scans for:
- PEM/key block markers: `-----BEGIN ...-----`
- SSH key markers: `ssh-rsa`, `ssh-ed25519`, `BEGIN OPENSSH PRIVATE KEY`, etc.
- Authorization/cookie markers: `Authorization`, `Bearer`, `Cookie`, `Set-Cookie`
- Token/header fields: `x-api-key`, `api_key`, `access_token`, `refresh_token`, `id_token`, `jwt`
- Known secret prefixes: `ghp_`, `github_pat_`, `sk-`, `AKIA`, `AIza`, `xox*`
- Literal secret assignment heuristics (`token|secret|password|api_key` assigned quoted values)

## Findings
### 1. Direct cryptographic material
- No certificate blocks found.
- No private key blocks found.
- No SSH key material found.
- No `.pem/.key/.crt/.p12/.pfx/.jks` files found.

### 2. Bearer tokens / cookies / auth headers with embedded secrets
- No hardcoded bearer token literals found.
- No concrete `Authorization: Bearer <token>` literals found.
- No `Cookie:` / `Set-Cookie:` header literals with session-like values found.
- No known secret-format tokens (`ghp_`, `sk-`, `AKIA...`, etc.) found.

### 3. Auth-related code references (non-secret)
Two files contain API-key plumbing via runtime input/env vars, not hardcoded secrets:
- `skills/literature-review/scripts/fetch_pubmed.py`
  - Uses `api_key` parameter and `NCBI_API_KEY` env var.
- `skills/literature-review/scripts/fetch_semantic_scholar.py`
  - Sets request header `x-api-key` from `api_key` parameter and `SEMANTIC_SCHOLAR_API_KEY` env var.

Assessment: these are expected auth integrations and not credential leakage.

## Ownership
`git blame` on the auth-relevant lines in both files attributes authorship to:
- `Cesar514` (commit `77a4b1f9`, dated 2026-02-27)

## Conclusion
No exposed cryptographic material or hardcoded auth secrets detected in this repository based on the requested pattern classes.
