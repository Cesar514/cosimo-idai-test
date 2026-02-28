# Privacy Audit: `scripts/`, `pixi.toml`, `pixi.lock`, `robotics_maze/pixi.toml`

## Scope
- `scripts/`
- `pixi.toml`
- `pixi.lock`
- `robotics_maze/pixi.toml`

## Summary
- No hardcoded credentials or access tokens were found in scope.
- No hardcoded private absolute paths were found in source/config literals.
- Low-risk privacy and portability issues exist around path handling and logging behavior.

## Findings

### 1. Low: absolute local paths can be emitted in logs/errors
When these scripts run on developer machines, log output can include full absolute filesystem paths (which may contain usernames and private directory structure).

Evidence:
- `scripts/apply_ppt_assets.py:49` (`Missing asset: {path}`)
- `scripts/apply_ppt_assets.py:77` (`updated: {PPT_PATH}`)
- `scripts/fix_ppt_full.py:320` (`updated: {PPT_PATH}`)
- `scripts/sim_runner.py:58` (`Missing simulation entrypoint: {target}`)
- `scripts/run_repo_smoke.sh:16` (`[smoke] repo=${ROOT_DIR}`)
- `scripts/run_repo_smoke.sh:71`, `73`, `75`, `82`, `92`, `148`, `169`, `182`, `291`, `320`, `351` (error messages print resolved `Path` values)
- `scripts/validate_deck_assets.py:78`, `80`, `100`, `102`, `157`, `161`, `203` (error paths are rendered directly)

Risk:
- If CI logs or shared artifacts are published, local machine path details can leak.

Recommendation:
- Log repo-relative paths where possible.
- Keep absolute paths behind a debug flag (for example `DEBUG_PATHS=1`).

### 2. Low: external absolute paths and `~` expansion are accepted for image references
Multiple code paths explicitly accept absolute and home-expanded paths from data files. This can create machine-specific behavior and accidental ingestion/validation of files outside the repo.

Evidence:
- `scripts/fix_ppt_full.py:58-60` (`Path(raw).expanduser()` then `is_absolute()` handling)
- `scripts/run_repo_smoke.sh:133-136` and `305-307` (same pattern in embedded Python checks)
- `scripts/validate_deck_assets.py:70-73` and `165-170` (absolute path passthrough + resolve)

Risk:
- Deck/image mapping artifacts can depend on local filesystem layout.
- Private local files could be referenced unintentionally.

Recommendation:
- Enforce repo-relative paths for slide image maps.
- Reject absolute inputs and `~` expansion for project artifacts unless explicitly whitelisted.

### 3. Informational: local-machine execution assumptions in tasks
Some task defaults are optimized for local interactive runs and specific OS sets.

Evidence:
- `pixi.toml:4` and `robotics_maze/pixi.toml:4` (platform matrix excludes Windows)
- `pixi.toml:19` (default `sim` task enables GUI workflow)
- `scripts/sim_runner.py:32-47` (interactive GUI defaults depend on TTY presence)

Impact:
- Not a credential/privacy leak by itself, but can cause machine-dependent behavior and reduce reproducibility in headless environments.

Recommendation:
- Keep non-interactive defaults for CI tasks, and move GUI behavior to explicit opt-in tasks.

## Credential Scan Result
Pattern-based scans across scoped files found no matches for common secrets (API keys, tokens, private key blocks, passwords).

## Notes on `pixi.lock`
- `pixi.lock` contains public package/index URLs (Conda/PyPI) and package hashes.
- No embedded credentials, local file URLs, or private host paths were identified.
