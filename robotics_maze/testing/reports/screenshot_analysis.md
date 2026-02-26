# Screenshot Analysis

Date: 2026-02-26
Scope: `robotics_maze/testing/screenshots/` (6 images)
Checks: blank frame, clipping, label readability, robot visibility, maze integrity, overlay presence

## Visibility/Overlay Anomaly Rules

| Flag | Severity | Trigger |
|---|---|---|
| `FRAME_NEAR_SOLID` | FAIL | Very low frame variance or near-monochrome image (renderer/camera likely failed). |
| `PATH_OVERLAY_MISSING` | WARN | Path overlay pixel signal is missing or near-zero. |
| `START_GOAL_MISSING` | FAIL | Start or goal marker signal is missing. |
| `ROBOT_MARKER_MISSING` | FAIL | Robot marker signal is missing. |
| `OVERLAY_CLIPPED_AT_EDGE` | WARN | Overlay pixels touch frame border (possible clipping/out-of-frame projection). |

## Per-image Results

| Image | Resolution | Overlay signal (px): path/start/goal/robot | Anomaly flags | Status | Findings |
|---|---:|---:|---|---|---|
| `fallback_sim_snapshot_1_astar.png` | 570x626 | `3020 / 129 / 177 / 97` | `none` | PASS | All key overlays detected and visible; no clipping. |
| `fallback_sim_snapshot_2_weighted_astar.png` | 570x626 | `3876 / 129 / 177 / 97` | `none` | PASS | Path and markers are present with healthy signal; no edge-touch anomalies. |
| `fallback_sim_snapshot_3_fringe_search.png` | 570x626 | `12436 / 129 / 177 / 97` | `none` | PASS | Strong path signal; start/goal/robot markers visible; maze frame intact. |
| `mujoco_sim_mujoco_1_astar.png` | 960x720 | `1634 / 129 / 177 / 197` | `none` | PASS | MuJoCo overlay path + markers present; no border clipping detected. |
| `mujoco_sim_mujoco_2_weighted_astar.png` | 960x720 | `6482 / 129 / 177 / 203` | `none` | PASS | Overlay coverage is strong; start/goal/robot markers are visible. |
| `mujoco_sim_mujoco_3_fringe_search.png` | 960x720 | `1922 / 129 / 177 / 198` | `none` | PASS | Overlays remain visible and in-frame; no visibility regressions found. |

## Summary

- PASS: 6
- WARN: 0
- FAIL: 0
- Total issues flagged: 0
- Visibility anomalies: 0
- Overlay anomalies: 0
- Overlay warning from prior run: RESOLVED

## Actionable Debug Notes

- If `PATH_OVERLAY_MISSING`: check planner path extraction and the `draw.line(...)` overlay branch in screenshot generators.
- If `START_GOAL_MISSING` or `ROBOT_MARKER_MISSING`: validate marker draw order/color and confirm marker coordinates are within projected frame bounds.
- If `OVERLAY_CLIPPED_AT_EDGE`: inspect projection scaling/insets (`maze_span`, margins) and camera distance/elevation before regenerating screenshots.
- If `FRAME_NEAR_SOLID`: verify renderer initialization and camera target, then regenerate using:
  - `python3 robotics_maze/scripts/generate_mujoco_screenshots.py`
  - `python3 robotics_maze/scripts/generate_sim_screenshots.py`
