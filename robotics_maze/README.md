# Robotics Maze Run Guide

Run all commands from the repository root (`cosimi-idai-test`) unless noted.

## Environment

```bash
pixi install
```

## GUI run

```bash
pixi run sim
```

The root `sim` task runs this exact command:

```bash
python scripts/sim_runner.py --gui-setup --planner astar --episodes 1 --maze-size 15 --seed 42 --gui --physics-backend pybullet --gui-hold-seconds 20
```

## CLI run (headless)

```bash
pixi run sim-cli
```

The root `sim-cli` task runs this exact command:

```bash
python scripts/sim_runner.py --planner astar --episodes 3 --maze-size 15 --seed 42
```

## Backend switching

Force PyBullet (GUI-capable):

```bash
python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 15 --seed 42 --gui --physics-backend pybullet
```

Force MuJoCo (headless in this project):

```bash
python scripts/sim_runner.py --planner astar --episodes 3 --maze-size 15 --seed 42 --physics-backend mujoco
```

Auto fallback order (PyBullet then MuJoCo):

```bash
python scripts/sim_runner.py --planner astar --episodes 3 --maze-size 15 --seed 42 --physics-backend auto
```

## URDF selection

Select a specific robot URDF (example uses built-in `pybullet_data` asset):

```bash
python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 15 --seed 42 --gui --physics-backend pybullet --robot-urdf r2d2.urdf
```

Use an external URDF file path (optional assets):

```bash
./robotics_maze/scripts/fetch_urdfs.sh turtlebot3
python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 15 --seed 42 --gui --physics-backend pybullet --robot-urdf robotics_maze/urdfs/external/turtlebot3/turtlebot3_description/urdf/turtlebot3_burger.urdf
```

If a provided URDF fails to load, the simulator logs a warning and falls back to the default robot.

## Note on custom args with root Pixi tasks

For custom flags, call `python scripts/sim_runner.py ...` directly.
Avoid `pixi run sim-cli -- --...` because the literal `--` is forwarded to `argparse` and causes an unrecognized-arguments error.
