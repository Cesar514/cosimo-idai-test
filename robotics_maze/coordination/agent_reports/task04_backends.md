# Task 04 - Physics Backend Reliability

## Ownership Deliverables
- Added backend check utility: `robotics_maze/scripts/check_backends.py`
- Added this report with sample output: `robotics_maze/coordination/agent_reports/task04_backends.md`

## Utility Behavior
`check_backends.py` verifies:
- `pybullet`, `pybullet_data`, and `mujoco` availability
- Backend resolution order for `--physics-backend {auto,pybullet,mujoco}` (mirrors `robotics_maze/src/sim.py`)
- Recommended runtime flags for this project (headless default + GUI recommendation when PyBullet is available)

## Run Command
```bash
pixi run python robotics_maze/scripts/check_backends.py
```

## Sample Output
```text
Physics backend probe:
  pybullet      available=yes version=3.2.5        detail=/Users/cesar514/Documents/agent_programming/cosimi-idai-test/.pixi/envs/default/lib/python3.11/site-packages/pybullet.cpython-311-darwin.so
  pybullet_data available=yes version=n/a          detail=/Users/cesar514/Documents/agent_programming/cosimi-idai-test/.pixi/envs/default/lib/python3.11/site-packages/pybullet_data/__init__.py
  mujoco        available=yes version=3.5.0        detail=/Users/cesar514/Documents/agent_programming/cosimi-idai-test/.pixi/envs/default/lib/python3.11/site-packages/mujoco/__init__.py

Effective backend availability: pybullet=1 mujoco=1

Resolution order by --physics-backend:
  auto     pybullet -> mujoco
  pybullet pybullet -> mujoco
  mujoco   mujoco -> pybullet

Recommended runtime flags:
  default_headless: --no-gui-setup --physics-backend auto
  gui_visual: --gui --physics-backend pybullet --gui-hold-seconds 8 --no-gui-setup
```
