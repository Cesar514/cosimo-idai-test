# Run Simulation from Repo Root (`pixi`)

Validated on 2026-02-26 from:
`.`

## 1) Default GUI mode

```bash
pixi run sim
```

What this task currently expands to (from `pixi.toml`):
```bash
python scripts/sim_runner.py --gui-setup --gui --planner astar --episodes 1 --maze-size 15 --seed 42 --physics-backend auto --gui-hold-seconds 20
```

## 2) GUI mode without setup popup (CI/automation-friendly)

```bash
pixi run sim --no-gui-setup --gui-hold-seconds 0 --episodes 1 --maze-size 9 --seed 7
```

Validated result included:
- `[START] ... gui=True backend=auto ...`
- `[DONE] success=1/1 ...`

## 3) No-GUI mode (headless)

Use root-level `pixi` Python execution (the `sim` task hardcodes `--gui`):

```bash
pixi run python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 9 --seed 7 --no-gui-setup --physics-backend auto
```

Validated result included:
- `[START] ... gui=False backend=auto ...`
- `[DONE] success=1/1 ...`

## 4) Backend selection from repo root

PyBullet (headless):

```bash
pixi run python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 9 --seed 7 --no-gui-setup --physics-backend pybullet
```

Validated result included:
- `[START] ... gui=False backend=pybullet ...`
- `[DONE] success=1/1 ...`

MuJoCo (headless):

```bash
pixi run python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 9 --seed 7 --no-gui-setup --physics-backend mujoco
```

Validated result included:
- `[START] ... gui=False backend=mujoco ...`
- `[DONE] success=1/1 ...`

PyBullet GUI with explicit backend:

```bash
pixi run sim --no-gui-setup --physics-backend pybullet --gui-hold-seconds 0
```

## 5) Quick environment sanity checks

List root tasks:

```bash
pixi task list
```

Probe backend availability in current pixi env:

```bash
pixi run python robotics_maze/scripts/check_backends.py
```

Validated probe output on this setup:
- `pybullet available=yes`
- `mujoco available=yes`
- resolution orders:
  - `auto -> pybullet -> mujoco`
  - `pybullet -> pybullet -> mujoco`
  - `mujoco -> mujoco -> pybullet`
