# Agent 13 PII Pattern Audit

## Scope
- Repository-wide regex scan across all files, including hidden paths (`.git`, `.pixi`) with `rg --no-config -uu`.
- Identifier classes scanned: emails, phone numbers, usernames/login handles, full names, and address-like strings.

## Raw Match Volume
| Pattern class | Total hits | `.git` | `.pixi` (any level) | Other paths |
|---|---:|---:|---:|---:|
| Email-like | 1566 | 18 | 1544 | 4 |
| Phone-like | 62551 | 18 | 61995 | 538 |
| Username/login-like | 260 | 0 | 260 | 0 |
| Full-name-like | 124 | 0 | 122 | 2 |
| Address-like | 22 | 0 | 22 | 0 |

## Findings (With Confidence)

1. **Likely real personal email + username in git history metadata**  
Confidence: **High**
- `./.git/logs/HEAD:1` through `:6` contain `Cesar514 <c-alan@hotmail.com>`.
- Same identity appears in:
  - `./.git/logs/refs/heads/main:1` through `:6`
  - `./.git/logs/refs/remotes/origin/main:1` through `:6`
- Assessment: this is real contributor metadata (not placeholder text).

2. **Project-authored placeholder email examples (non-personal)**  
Confidence: **High (for placeholder/non-sensitive classification)**
- `./skills/playwright/SKILL.md:97` contains `user@example.com`.
- `./skills/playwright/references/workflows.md:21` contains `user@example.com`.
- `./skills/playwright/references/cli.md:28` contains `user@example.com`.
- `./artifacts_prompts/privacy_audit/agent_04_skills.md:18` references the same placeholder.
- Assessment: clearly sample values, not personal identifiers.

3. **Large amount of third-party maintainer/contact PII in vendored environment files**  
Confidence: **Medium**
- Mostly under `.pixi` trees, e.g.:
  - `./.pixi/envs/default/share/icu/78.2/LICENSE:468`
  - `./robotics_maze/.pixi/envs/default/share/man/man1/bzip2.1:430`
  - `./robotics_maze/.pixi/envs/default/include/curses.h:31`
- Assessment: names/emails/addresses appear to be upstream license/header metadata, not app user data.

4. **No confirmed phone numbers in project-owned content after triage**  
Confidence: **Medium**
- Broad phone regex produced many false positives from hashes/timestamps (`pixi.lock`, LaTeX aux/bib artifacts).
- Refined separator-required phone pattern on non-vendor paths returned zero matches.
- Assessment: no credible direct phone number exposure found in project-authored files.

5. **No confirmed hardcoded usernames, full names, or addresses in project-owned source/config**  
Confidence: **Medium**
- Non-vendor scan (`!**/.pixi/**`, `!.git/**`) returned:
  - Username/login assignments: 0
  - Full-name assignments: 0
  - Address-like strings: 0
- Two non-vendor full-name-like hits were false positives in screenshot labels:
  - `./robotics_maze/scripts/capture_regression_screenshots.py:140`
  - `./robotics_maze/scripts/capture_regression_screenshots.py:151`

