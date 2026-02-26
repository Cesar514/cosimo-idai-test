# Screenshot Debug TODOs

Date: 2026-02-26

## Current Status

- No active screenshot blockers in this run (`6/6 PASS`).
- No visibility/overlay anomalies currently flagged.
- Prior MuJoCo overlay gap (missing start/goal/path) remains resolved.

## Actionable Debug Playbook (Use When A Flag Appears)

- [ ] `FRAME_NEAR_SOLID` (FAIL)
  Trigger: screenshot is near-monochrome or low-variance.
  Action: verify renderer/camera setup first, then rerun both screenshot generators and compare fresh outputs.
- [ ] `PATH_OVERLAY_MISSING` (WARN)
  Trigger: path overlay pixel signal is absent or near-zero.
  Action: check planner output path length and `draw.line(...)` path overlay branch in both generators.
- [ ] `START_GOAL_MISSING` (FAIL)
  Trigger: start or goal marker is not detected.
  Action: verify marker draw calls/colors and ensure marker coordinates are still inside projected image bounds.
- [ ] `ROBOT_MARKER_MISSING` (FAIL)
  Trigger: robot marker not detected or fully occluded.
  Action: inspect robot sampling index and projection mapping; confirm marker draw order occurs after maze/path rendering.
- [ ] `OVERLAY_CLIPPED_AT_EDGE` (WARN)
  Trigger: overlay pixels touch frame border.
  Action: increase projection margins/reduce span; in MuJoCo also review camera distance/elevation/lookat.

## Quick Repro Commands

- `python3 robotics_maze/scripts/generate_mujoco_screenshots.py`
- `python3 robotics_maze/scripts/generate_sim_screenshots.py`
- `bash robotics_maze/testing/run_sim_tests.sh`

## Optional Follow-up

- [ ] Add a compact on-frame legend (`start`, `goal`, `robot`, `path`) to remove marker-role ambiguity during fast triage.
- [ ] Automate pixel-signal QA in CI (flag path/start/goal/robot missing and edge clipping before report publish).
