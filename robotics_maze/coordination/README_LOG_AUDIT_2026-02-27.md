# README/LOG Staleness Audit (2026-02-27)

## Scope

Scanned all project-level `README*`/`LOG*` files in this repo (excluding runtime/vendor trees such as `.pixi/`, `.pytest_cache/`, and `node_modules/`).

Files audited:
- `README.md`
- `docs/generated/README.md`
- `paper/ieee_tro_robotics_maze/README.md`
- `robotics_maze/README.md`
- `robotics_maze/results/README.md`
- `robotics_maze/urdfs/README.md`
- `skills/README_LOCAL_SKILLS.md`

Project-level `LOG*` matches found: none.

## Checklist (Pass/Fail)

- [PASS] Date markers are current or internally consistent.
  - `README.md:9` (`Last updated: 2026-02-27`)
  - `docs/generated/README.md:4` (`Last refreshed: 2026-02-27`)
  - `paper/ieee_tro_robotics_maze/README.md:82`
  - `paper/ieee_tro_robotics_maze/README.md:83`

- [PASS] Paper README benchmark command context is now explicit and valid.
  - Root-scoped command is documented for repository-root execution.
  - Equivalent relative command from `paper/ieee_tro_robotics_maze` is documented.

- [PASS] Root and robotics README task references align with declared Pixi tasks.
  - Task list references: `README.md:20`, `README.md:22`, `README.md:23`, `robotics_maze/README.md:12`, `robotics_maze/README.md:14`, `robotics_maze/README.md:15`
  - Task definitions: `pixi.toml:18`, `pixi.toml:19`, `pixi.toml:20`

- [PASS] Referenced commands/scripts are present and argument usage is current.
  - `scripts/sim_runner.py` exists and forwards supported flags used in docs: `scripts/sim_runner.py:55`
  - Benchmark CLI flags documented in README match parser options: `robotics_maze/src/benchmark.py:690`, `robotics_maze/src/benchmark.py:711`
  - URDF fetch script/options referenced in docs are implemented: `robotics_maze/scripts/fetch_urdfs.py:211`, `robotics_maze/scripts/fetch_urdfs.py:206`

- [PASS] No references to absent tasks detected in audited README files.
  - Verified task names used in docs: `sim`, `benchmark` (present in `pixi.toml:19` and `pixi.toml:20`)

- [PASS] No outdated issue lists detected.
  - No explicit open-issues/tracker lists found in audited README files.

## Summary

Audit result: **0 FAIL**, **6 PASS**.  
No stale README/LOG blockers detected in scoped files after command-context correction in `paper/ieee_tro_robotics_maze/README.md`.
