# Simulation QA Checklist (Deterministic)

## Scope
Validate deterministic simulation behavior for:
- GUI visibility
- URDF loading and fallback behavior
- dynamics realism
- physics backend fallback order

## Test Setup
1. Run from repository root: `.`.
2. Export deterministic env vars:
```bash
export PYTHONHASHSEED=0
export TZ=UTC
```
3. Use `--no-gui-setup` for all CLI runs to avoid Tk dialog nondeterminism.
4. Capture each command output with `tee` and keep logs under `robotics_maze/testing/`.

## Case 00: Backend Fingerprint (Required)
Command:
```bash
python3 - <<'PY'
import importlib.util
print(f"PYBULLET_AVAILABLE={int(bool(importlib.util.find_spec('pybullet')))}")
print(f"MUJOCO_AVAILABLE={int(bool(importlib.util.find_spec('mujoco')))}")
PY
```
Pass criteria:
- Output contains both `PYBULLET_AVAILABLE=<0|1>` and `MUJOCO_AVAILABLE=<0|1>`.
- Record the tuple `(P, M)` for expected results in later cases.

## Case 01: Deterministic Visual Visibility Artifacts (Required)
If `M=1`:
```bash
python3 robotics_maze/scripts/capture_regression_screenshots.py \
  --output-dir robotics_maze/testing/screenshots \
  --require-mujoco
```
If `M=0`:
```bash
python3 robotics_maze/scripts/capture_regression_screenshots.py \
  --output-dir robotics_maze/testing/screenshots
```
Then:
```bash
find robotics_maze/testing/screenshots -maxdepth 1 -type f -name '*.png' | sort
```
Pass criteria:
- `M=1`: exactly 6 PNGs exist, with exact names:
  - `mujoco_sim_mujoco_1_astar.png`
  - `mujoco_sim_mujoco_2_weighted_astar.png`
  - `mujoco_sim_mujoco_3_fringe_search.png`
  - `fallback_sim_snapshot_1_astar.png`
  - `fallback_sim_snapshot_2_weighted_astar.png`
  - `fallback_sim_snapshot_3_fringe_search.png`
- `M=0`: exactly 3 PNGs exist, with exact names:
  - `fallback_sim_snapshot_1_astar.png`
  - `fallback_sim_snapshot_2_weighted_astar.png`
  - `fallback_sim_snapshot_3_fringe_search.png`
- No blank/near-solid frames in generated screenshots.

## Case 02: GUI Visibility Runtime Path (Required)
Command:
```bash
python3 robotics_maze/src/main.py \
  --planner astar --episodes 1 --maze-size 11 --seed 42 \
  --gui --physics-backend pybullet --gui-hold-seconds 2 --no-gui-setup
```
Pass criteria:
- `P=1`: PyBullet window opens, robot/path remain visible, process exits `0`.
- `P=0, M=1`: warning includes `Requested physics_backend='pybullet'` and GUI warning includes `running MuJoCo headless fallback`, process exits `0`.
- `P=0, M=0`: warning includes `Neither PyBullet nor MuJoCo is available`, process exits `0`.

## Case 03: URDF Validation - Invalid Extension (Required)
Command:
```bash
python3 robotics_maze/src/main.py \
  --planner astar --episodes 1 --maze-size 11 --seed 42 \
  --robot-urdf not_a_urdf.txt --no-gui-setup
```
Pass criteria:
- Warning contains `expected a .urdf file`.
- `[START]` line shows `urdf=default(husky/husky.urdf)`.
- Run completes with `[DONE] success=1/1`.

## Case 04: URDF Validation - Missing .urdf File (Required)
Command:
```bash
python3 robotics_maze/src/main.py \
  --planner astar --episodes 1 --maze-size 11 --seed 42 \
  --robot-urdf /tmp/qa_missing_robot.urdf --no-gui-setup
```
Pass criteria:
- Warning contains `file not found`.
- `[START]` line shows `urdf=default(husky/husky.urdf)`.
- Run completes with `[DONE] success=1/1`.

## Case 05: URDF Validation - Existing Local URDF Path (Required)
Command:
```bash
TMP_URDF="$(mktemp /tmp/qa_robot_XXXXXX.urdf)"
cat > "$TMP_URDF" <<'URDF'
<?xml version="1.0"?>
<robot name="qa_box">
  <link name="base_link">
    <inertial>
      <origin xyz="0 0 0"/>
      <mass value="1"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
    <visual><geometry><box size="0.2 0.2 0.2"/></geometry></visual>
    <collision><geometry><box size="0.2 0.2 0.2"/></geometry></collision>
  </link>
</robot>
URDF
python3 robotics_maze/src/main.py \
  --planner astar --episodes 1 --maze-size 11 --seed 42 \
  --robot-urdf "$TMP_URDF" --physics-backend auto --no-gui-setup
rm -f "$TMP_URDF"
```
Pass criteria:
- No warning starts with `Ignoring robot URDF`.
- `[START]` line includes `urdf=/tmp/qa_robot_` absolute path.
- Run completes with `[DONE] success=1/1`.

## Case 06: URDF Runtime Fallback for Malformed URDF (Conditional)
Run only if `P=1`.
Command:
```bash
BAD_URDF="$(mktemp /tmp/qa_bad_XXXXXX.urdf)"
printf '%s\n' '<robot name="broken">' > "$BAD_URDF"
python3 robotics_maze/src/main.py \
  --planner astar --episodes 1 --maze-size 11 --seed 42 \
  --robot-urdf "$BAD_URDF" --physics-backend pybullet --no-gui-setup
rm -f "$BAD_URDF"
```
Pass criteria:
- Warning contains `Unable to load custom robot URDF`.
- Warning contains `Falling back to defaults ('husky/husky.urdf' then 'r2d2.urdf')`.
- Run completes with `[DONE] success=1/1`.
Skip criteria:
- If `P=0`, mark `SKIP (PyBullet unavailable)`.

## Case 07: Dynamics Realism Baseline (Required)
Command:
```bash
python3 robotics_maze/src/main.py \
  --planner astar --episodes 3 --maze-size 11 --seed 42 \
  --physics-backend mujoco --no-gui-setup
```
Pass criteria:
- `M=1`: deterministic episode steps are exactly `89`, `93`, `137` and `[DONE] success=3/3`.
- `M=0, P=1`: warning contains `Requested physics_backend='mujoco'` and all episode steps satisfy `1 <= steps <= 5000` with `[DONE] success=3/3`.
- `M=0, P=0`: warning contains `Neither PyBullet nor MuJoCo is available` and deterministic episode steps are exactly `88`, `92`, `136`.

## Case 08: Forced Final Fallback Path (Required)
Command:
```bash
python3 - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, str(Path('robotics_maze/src').resolve()))
import main
import sim
sim.p = None
sim.pybullet_data = None
sim.mujoco = None
raise SystemExit(main.main([
    '--planner', 'astar', '--episodes', '1', '--maze-size', '11', '--seed', '42',
    '--physics-backend', 'auto', '--no-gui-setup',
]))
PY
```
Pass criteria:
- Warning contains `Neither PyBullet nor MuJoCo is available; using deterministic kinematic fallback.`
- Episode line contains `steps=88`.
- Exit code is `0`.

## Case 09: Backend Fallback Matrix Smoke (Required)
Command:
```bash
for backend in auto pybullet mujoco; do
  echo "=== backend=${backend} ==="
  python3 robotics_maze/src/main.py \
    --planner astar --episodes 1 --maze-size 11 --seed 42 \
    --physics-backend "$backend" --no-gui-setup
  echo
 done
```
Pass criteria:
- `backend=auto`: uses preferred available backend or warns with `falling back` text.
- `backend=pybullet`: if `P=0, M=1`, warns `Requested physics_backend='pybullet'...falling back to MuJoCo.`
- `backend=mujoco`: if `M=0, P=1`, warns `Requested physics_backend='mujoco'...falling back to PyBullet.`
- Every run ends with `[DONE] success=1/1`.

## Sign-off Rules
- Required cases must be `PASS`.
- `Case 06` may be `SKIP` only when `P=0`.
- Any missing warning line, missing screenshot artifact, or non-deterministic step mismatch is `FAIL`.
