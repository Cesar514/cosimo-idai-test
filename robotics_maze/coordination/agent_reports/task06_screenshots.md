# Task 06/36 - Screenshot Pipeline

## Scope
Owned files:
- `robotics_maze/scripts/capture_regression_screenshots.py`
- `robotics_maze/testing/*` (validation artifacts only)
- `robotics_maze/coordination/agent_reports/task06_screenshots.md`

Goal:
- Improve automated simulation screenshot capture into `robotics_maze/testing/screenshots`.
- Enforce deterministic filenames for regression outputs.

## Script Updates
Updated `robotics_maze/scripts/capture_regression_screenshots.py` with a deterministic filename contract:

1. Added per-step expected filename suffixes in `CaptureStep` and computed deterministic names via `expected_filenames()`.
2. Added strict post-run validation for generated files:
   - Missing expected filenames now fail the run (or warn for optional MuJoCo step when MuJoCo is not required).
   - Unexpected prefix-matching filenames fail the run during clean runs (`--no-clean` keeps this relaxed).
3. Added `--dry-run` mode to print planned commands + deterministic output filenames without executing generation.
4. Kept default output directory as `robotics_maze/testing/screenshots` and preserved optional MuJoCo behavior.
5. Made final printed screenshot list stable by preserving deterministic step/order output instead of set+sort reordering.

Deterministic target filenames are now explicitly enforced as:
- `mujoco_sim_mujoco_1_astar.png`
- `mujoco_sim_mujoco_2_weighted_astar.png`
- `mujoco_sim_mujoco_3_fringe_search.png`
- `fallback_sim_snapshot_1_astar.png`
- `fallback_sim_snapshot_2_weighted_astar.png`
- `fallback_sim_snapshot_3_fringe_search.png`

## Example Capture Run
Command:
```bash
python3 robotics_maze/scripts/capture_regression_screenshots.py \
  --output-dir robotics_maze/testing/screenshots \
  --require-mujoco
```

Result:
- Exit code: `0`
- Generated files:
  - `robotics_maze/testing/screenshots/mujoco_sim_mujoco_1_astar.png`
  - `robotics_maze/testing/screenshots/mujoco_sim_mujoco_2_weighted_astar.png`
  - `robotics_maze/testing/screenshots/mujoco_sim_mujoco_3_fringe_search.png`
  - `robotics_maze/testing/screenshots/fallback_sim_snapshot_1_astar.png`
  - `robotics_maze/testing/screenshots/fallback_sim_snapshot_2_weighted_astar.png`
  - `robotics_maze/testing/screenshots/fallback_sim_snapshot_3_fringe_search.png`

Verification command:
```bash
find robotics_maze/testing/screenshots -maxdepth 1 -type f -name '*.png' | sort
```

Observed set matched the deterministic contract exactly.

## Dry-Run Path (GUI/Dependency-safe)
Command:
```bash
python3 robotics_maze/scripts/capture_regression_screenshots.py \
  --output-dir robotics_maze/testing/screenshots \
  --dry-run
```

Result:
- Exit code: `0`
- Printed planned commands and all six deterministic target filenames without rendering.
