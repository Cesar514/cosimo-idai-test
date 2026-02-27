# Root Pixi Guide Refresh Report

## Scope
- Owned file updated: `robotics_maze/coordination/ROOT_PIXI.md`
- Reference source of truth: root `pixi.toml`

## Verification Performed
- Checked task registry:
  - `pixi task list` -> `benchmark`, `sim`
- Confirmed stale task behavior:
  - `pixi run sim-cli` -> task not found (`sim-cli: command not found`)
- Confirmed argument passthrough behavior:
  - `pixi run sim --help` works and displays `robotics_maze/src/main.py` CLI help
  - `pixi run sim -- --help` also works (wrapper strips `--`)
  - `pixi run benchmark --help` works
  - `pixi run benchmark -- --help` fails with unrecognized args (`-- --help`)

## Changes Made to `ROOT_PIXI.md`
- Removed stale `sim-cli` task mention.
- Updated task list to exactly match root `pixi.toml` (`sim`, `benchmark`).
- Added concrete root command expansions for both tasks.
- Corrected CLI argument guidance:
  - Use direct flag passing after task name.
  - `sim` supports optional `--` separator due to `scripts/sim_runner.py` normalization.
  - `benchmark` should not use `--` separator.
- Replaced outdated examples with currently valid command examples.

## Result
- `ROOT_PIXI.md` now reflects current root task definitions and observed runtime behavior.
