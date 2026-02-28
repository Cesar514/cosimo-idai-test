# Agent 20 Adversarial Privacy Sweep (Consolidated)

Date: 2026-02-27
Scope: whole-repo adversarial re-check (including generated artifacts and local repo metadata under `.git/`)

## Priority List

### P0

1. **Committed bytecode leaks local username + absolute workstation paths**
- Evidence:
  - `robotics_maze/src/__pycache__/sim.cpython-311.pyc:6` contains `/Users/cesar514/Documents/agent_programming/cosimi-idai-test/...`
  - `robotics_maze/src/alt_planners/__pycache__/r1_weighted_astar.cpython-311.pyc:6` contains same absolute prefix
  - `robotics_maze/tests/__pycache__/test_core.cpython-311-pytest-9.0.2.pyc:11` contains same absolute prefix
  - `git ls-files '*.pyc'` shows 20 tracked `.pyc` files; 17 currently match the leaked absolute prefix
  - `.gitignore:1` is effectively empty (no guard against re-committing bytecode)
- Impact: direct deanonymization of local account (`cesar514`) and host directory topology; high reconnaissance value if shared externally.
- Why likely missed: many prior scans excluded binary files and focused on text/markdown.

2. **Raw session transcript is committed and includes sensitive operational chat content**
- Evidence:
  - `artifacts_prompts/session_prompt_raw_from_history.md:13`-`16` includes personal event metadata (date/time/location/lead)
  - `artifacts_prompts/session_prompt_raw_from_history.md:215`-`223` and `:231` includes full operational prompts and explicit `codex resume <session-id>` material
  - `artifacts_prompts/repo_prompt_step_results_slideshow.md:140`-`146` explicitly points readers to the full verbatim prompt log
- Impact: exposes full user instruction history and session-level operational details; this is a primary privacy boundary breach if repo/artifacts are shared.
- Why likely missed: prior checks treated session UUID exposure as informational, but not the combined effect of verbatim transcript + resume/session references.

### P1

1. **Personal/event-identifying details are duplicated across multiple deliverables**
- Evidence:
  - `agents.pptx` extracted XML: `ppt/slides/slide1.xml:70` (`Cesar Contreras | Friday 27 February 2026`)
  - `agents.pptx` extracted XML: `ppt/slides/slide2.xml:56` and `:63` (exact date/time and location)
  - `agents_factual_risk_audit.md:41`, `:47`, `:48`, `:49` repeats name + event metadata
  - `artifacts_prompts/session_prompt_raw_from_history.md:13`-`16` repeats same tuple
- Impact: creates a strong identity + schedule + location linkage surface.

2. **Session and subagent identifiers are broadly exposed, enabling cross-log correlation**
- Evidence:
  - `artifacts_prompts/session_chat_prompt_ledger.md:3` (session id)
  - `artifacts_prompts/PAPER_WRITING_PLAN_USED.md:3` (session id)
  - `artifacts_prompts/repo_prompt_step_results_slideshow.md:11` (session id)
  - `robotics_maze/coordination/session_event_log.csv:36`-`44`, `:64`-`73` (many subagent UUIDs)
- Impact: improves traceability/correlation of internal activity across logs and artifacts.

3. **Local git reflogs expose a personal email address**
- Evidence:
  - `.git/logs/HEAD:1`-`6` contains `Cesar514 <c-alan@hotmail.com>`
  - `.git/logs/refs/heads/main:1`-`6` contains same email
  - `.git/logs/refs/remotes/origin/main:1`-`6` contains same email
- Impact: direct PII exposure if the repository directory (including `.git/`) is archived/shared.
- Note: local `.git` metadata is not normally published to GitHub, but is still a whole-repo privacy risk in local exports.

### P2

1. **Tracked `.DS_Store` files leak host/environment fingerprints**
- Evidence:
  - Tracked entries include `.DS_Store`, `docs/.DS_Store`, `robotics_maze/.DS_Store`, `paper/.DS_Store`, etc.
  - `strings .DS_Store` reveals Finder metadata such as `WindowBounds` and UI state fields.
- Impact: low but unnecessary environment metadata disclosure.

2. **Privacy exposure is amplified by top-level discoverability links**
- Evidence:
  - `README.md:71`-`73` links directly to generated prompt/step ledgers
  - `docs/generated/repo_prompt_step_results_slideshow.md:162`-`166` points to session event CSV and backlog traces
- Impact: increases accidental access probability to sensitive operational narrative artifacts.

## Bottom Line

- **Most severe missed leaks in this adversarial pass:**
  - committed `.pyc` absolute-path deanonymization
  - committed raw verbatim prompt transcript with session-resume reference
- **No hardcoded API keys/private keys found** in tracked text/binary samples reviewed during this pass.
