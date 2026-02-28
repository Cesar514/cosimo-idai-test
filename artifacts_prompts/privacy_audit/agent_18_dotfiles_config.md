# Privacy Audit: Dotfiles and Repo Config Docs (Agent 18)

Date: 2026-02-27
Scope: hidden files (dotfiles) and repository config docs in `/Users/cesar514/Documents/agent_programming/cosimi-idai-test`.

## Files Reviewed
- Hidden tracked files: `.gitignore`, `.DS_Store` variants, `.gitkeep`, `paper/ieee_tro_robotics_maze/.gitignore`
- Config artifacts: `pixi.toml`, `pixi.lock`, `robotics_maze/pixi.toml`, `robotics_maze/pixi.lock`, `robotics_maze/pyproject.toml`
- Skill config YAMLs: `skills/*/agents/openai.yaml`
- Local git metadata checked for personal leakage surface: `.git/config`, `.git/FETCH_HEAD`

## Findings

### 1) Medium: Tracked `.DS_Store` files leak personal/system metadata surface
Tracked macOS Finder metadata files are present:
- `.DS_Store`
- `docs/.DS_Store`
- `paper/.DS_Store`
- `paper/ieee_tro_robotics_maze/.DS_Store`
- `paper/ieee_tro_robotics_maze/coordination/.DS_Store`
- `robotics_maze/.DS_Store`
- `robotics_maze/testing/.DS_Store`

Risk:
- `.DS_Store` can encode local Finder/view metadata and file/folder attributes not intended for sharing.
- Presence in git history increases accidental disclosure of workstation-level metadata.

### 2) Medium: Root `.gitignore` is effectively empty
Evidence:
- `.gitignore:1` is blank.

Risk:
- With no ignore policy at repo root, sensitive local artifacts (for example `.env`, credential files, editor/system files) are easier to accidentally stage and commit.
- Existing tracked `.DS_Store` files are a concrete indicator of this risk.

### 3) Low (local only): Personal identifier in git remote URL
Evidence:
- `.git/config:9` includes `https://github.com/Cesar514/cosimo-idai-test.git`
- `.git/FETCH_HEAD` references the same remote.

Risk:
- GitHub handle exposure (`Cesar514`) is a personal identifier in local git metadata.
- This is not a repository-tracked secret by itself, but should not be published from local metadata snapshots/log exports without intent.

## Negative Findings (What was NOT found)
- No API keys, tokens, passwords, private keys, or `.env*` secrets detected in reviewed tracked config files.
- No credential-bearing config files (for example `.npmrc`, `.pypirc`, `.netrc`, key/pem files) found in active repo paths outside generated audit artifacts.

## Recommended Remediation (not applied in this task)
1. Remove tracked `.DS_Store` files from version control and ignore them globally/repo-wide.
2. Populate root `.gitignore` with standard OS/editor/secret patterns (at minimum: `.DS_Store`, `.env`, `.env.*`, `*.pem`, `*.key`, `.venv/`, local cache dirs).
3. Avoid sharing raw `.git/config` or `.git/FETCH_HEAD` in public artifacts unless identifiers are intentionally disclosed.
