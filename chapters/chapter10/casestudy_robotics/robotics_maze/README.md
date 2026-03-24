# Robotics Maze Run Guide

Run commands from repository root (`cosimi-idai-test`) unless noted.

## Setup

```bash
pixi install
pixi task list
```

Current root Pixi tasks:

- `sim`
- `benchmark`

## GUI simulation (root task)

Default interactive GUI run:

```bash
pixi run sim
```

Automation-friendly GUI run (no setup dialog, short hold):

```bash
pixi run sim --no-gui-setup --gui-hold-seconds 0 --episodes 1 --maze-size 9 --seed 7
```

## Headless simulation (CLI)

There is no root `sim-cli` task. Use the root wrapper directly:

```bash
pixi run python scripts/sim_runner.py --planner astar --episodes 3 --maze-size 15 --seed 42 --no-gui-setup --physics-backend auto
```

## Backend selection

PyBullet (headless):

```bash
pixi run python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 9 --seed 7 --no-gui-setup --physics-backend pybullet
```

MuJoCo (headless):

```bash
pixi run python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 9 --seed 7 --no-gui-setup --physics-backend mujoco
```

PyBullet GUI:

```bash
pixi run sim --no-gui-setup --physics-backend pybullet --gui-hold-seconds 0 --episodes 1 --maze-size 9 --seed 7
```

Note: in this project, MuJoCo runs headless; GUI visualization is provided by PyBullet.

## Benchmarking

Run default root benchmark task:

```bash
pixi run benchmark
```

Run benchmark with explicit overrides:

```bash
pixi run benchmark --mazes 1 --width 9 --height 9 --seed 7 --algorithm backtracker --output-dir robotics_maze/results
```

## URDF selection

Use built-in `pybullet_data` URDF:

```bash
pixi run python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 15 --seed 42 --gui --physics-backend pybullet --robot-urdf r2d2.urdf
```

Use downloaded external URDF:

```bash
./robotics_maze/scripts/fetch_urdfs.sh turtlebot3
pixi run python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 15 --seed 42 --gui --physics-backend pybullet --robot-urdf robotics_maze/urdfs/external/turtlebot3/turtlebot3_description/urdf/turtlebot3_burger.urdf
```

If a provided URDF is invalid or missing, runtime logs a warning and falls back to the default robot.

## Argument passing note

When adding extra flags to root Pixi tasks, append them directly (for example, `pixi run sim --episodes 1 ...`).
