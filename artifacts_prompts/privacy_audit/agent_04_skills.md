# Privacy Audit Report: `skills/` (Agent 04)

## Scope
- Directory audited: `skills/`
- File types reviewed: `SKILL.md`, `references/*.md`, `scripts/*.py`, `scripts/*.sh`, `agents/*.yaml`
- Objective: detect private paths, local usernames, secrets, and auth data exposure

## Method
- Searched for common leak indicators: absolute home paths (`/Users/`, `/home/`, `C:\\Users\\`), credential/token patterns, private key blocks, and email-like strings.
- Reviewed contextual lines for all candidate hits to distinguish placeholders and configuration hooks from real secret exposure.

## Findings

### 1) Placeholder credentials in documentation examples (Low)
- Evidence:
  - `skills/playwright/SKILL.md:98` uses `"password123"` in a form-fill example.
  - `skills/playwright/references/workflows.md:22` uses `"password123"` in a form-fill example.
  - `skills/playwright/SKILL.md:97`, `skills/playwright/references/workflows.md:21`, `skills/playwright/references/cli.md:28` use `"user@example.com"`.
- Assessment:
  - These are clearly example placeholders, not exposed real credentials.
  - Residual risk is copy/paste misuse by operators in real environments.

### 2) Auth-capable scripts rely on env vars / CLI args, with no hardcoded secrets (Informational)
- Evidence:
  - `skills/literature-review/scripts/fetch_pubmed.py:105-106` reads `NCBI_API_KEY` and `NCBI_EMAIL` via `os.getenv`.
  - `skills/literature-review/scripts/fetch_semantic_scholar.py:63` reads `SEMANTIC_SCHOLAR_API_KEY` via `os.getenv`.
  - `skills/literature-review/scripts/fetch_pubmed.py:39,64` and `fetch_semantic_scholar.py:28` attach keys to outbound API requests when provided.
- Assessment:
  - No secret values are embedded in the repo.
  - Current pattern is standard and acceptable for scripts that call external APIs.

### 3) Private paths / local usernames: none found
- Searched for user-home absolute paths and user-specific local identifiers.
- No concrete private path strings (e.g., `/Users/<name>/...`, `/home/<name>/...`) or local usernames were found in `skills/`.

## Summary
- No hardcoded secrets, tokens, private keys, or local user paths were found in `skills/`.
- Only low-risk placeholder credential examples were identified in Playwright docs.
