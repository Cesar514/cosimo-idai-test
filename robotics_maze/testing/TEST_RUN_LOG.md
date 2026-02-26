# Robotics Maze Simulation Test Run Log

- Date (UTC): 2026-02-26T22:05:41Z
- Working directory: /Users/cesar514/Documents/agent_programming/cosimi-idai-test
- PYTHONHASHSEED: 0

## Deterministic run: astar

**Command**
```bash
python3 robotics_maze/src/main.py --planner astar --episodes 3 --maze-size 11 --seed 42 
```

**Output**
```text
[INFO] Maze generator loaded from maze.create_maze_generator
[INFO] Planner loaded from planners registry: astar
[INFO] Simulator loaded from sim.create_simulator
[START] planner=astar episodes=3 maze_size=11x11 seed=42 gui=False backend=auto urdf=default(husky/husky.urdf) gui_hold_s=8.0
[WARN] PyBullet is unavailable; falling back to MuJoCo.
[EP 1/3] status=ok steps=89 elapsed_s=0.0039
[WARN] PyBullet is unavailable; falling back to MuJoCo.
[EP 2/3] status=ok steps=93 elapsed_s=0.0026
[WARN] PyBullet is unavailable; falling back to MuJoCo.
[EP 3/3] status=ok steps=137 elapsed_s=0.0030
[DONE] success=3/3 avg_steps=106.33 avg_elapsed_s=0.0032

```

**Exit status:** 0

## Deterministic run: weighted_astar

**Command**
```bash
python3 robotics_maze/src/main.py --planner weighted_astar --episodes 3 --maze-size 11 --seed 42 
```

**Output**
```text
[INFO] Maze generator loaded from maze.create_maze_generator
[INFO] Planner loaded from alt planner module: alt_planners.r1_weighted_astar.plan_weighted_astar
[INFO] Simulator loaded from sim.create_simulator
[START] planner=weighted_astar episodes=3 maze_size=11x11 seed=42 gui=False backend=auto urdf=default(husky/husky.urdf) gui_hold_s=8.0
[WARN] PyBullet is unavailable; falling back to MuJoCo.
[EP 1/3] status=ok steps=89 elapsed_s=0.0038
[WARN] PyBullet is unavailable; falling back to MuJoCo.
[EP 2/3] status=ok steps=93 elapsed_s=0.0027
[WARN] PyBullet is unavailable; falling back to MuJoCo.
[EP 3/3] status=ok steps=137 elapsed_s=0.0032
[DONE] success=3/3 avg_steps=106.33 avg_elapsed_s=0.0032

```

**Exit status:** 0

## Deterministic run: fringe_search

**Command**
```bash
python3 robotics_maze/src/main.py --planner fringe_search --episodes 3 --maze-size 11 --seed 42 
```

**Output**
```text
[INFO] Maze generator loaded from maze.create_maze_generator
[INFO] Planner loaded from alt planner module: alt_planners.r8_fringe_search.plan_fringe_search
[INFO] Simulator loaded from sim.create_simulator
[START] planner=fringe_search episodes=3 maze_size=11x11 seed=42 gui=False backend=auto urdf=default(husky/husky.urdf) gui_hold_s=8.0
[WARN] PyBullet is unavailable; falling back to MuJoCo.
[EP 1/3] status=ok steps=89 elapsed_s=0.0039
[WARN] PyBullet is unavailable; falling back to MuJoCo.
[EP 2/3] status=ok steps=93 elapsed_s=0.0027
[WARN] PyBullet is unavailable; falling back to MuJoCo.
[EP 3/3] status=ok steps=137 elapsed_s=0.0031
[DONE] success=3/3 avg_steps=106.33 avg_elapsed_s=0.0032

```

**Exit status:** 0

## Capture regression screenshots

**Command**
```bash
python3 robotics_maze/scripts/capture_regression_screenshots.py --output-dir /Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots --require-mujoco 
```

**Output**
```text
[INFO] running: /Library/Developer/CommandLineTools/usr/bin/python3 /Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/scripts/generate_mujoco_screenshots.py --output-dir /Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots --filename-prefix mujoco_
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/mujoco_sim_mujoco_1_astar.png
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/mujoco_sim_mujoco_2_weighted_astar.png
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/mujoco_sim_mujoco_3_fringe_search.png
[INFO] running: /Library/Developer/CommandLineTools/usr/bin/python3 /Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/scripts/generate_sim_screenshots.py --output-dir /Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots --filename-prefix fallback_
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/fallback_sim_snapshot_1_astar.png
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/fallback_sim_snapshot_2_weighted_astar.png
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/fallback_sim_snapshot_3_fringe_search.png
[INFO] generated screenshots:
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/fallback_sim_snapshot_1_astar.png
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/fallback_sim_snapshot_2_weighted_astar.png
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/fallback_sim_snapshot_3_fringe_search.png
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/mujoco_sim_mujoco_1_astar.png
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/mujoco_sim_mujoco_2_weighted_astar.png
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/mujoco_sim_mujoco_3_fringe_search.png

```

**Exit status:** 0

## Collect regression screenshots

**Command**
```bash
find /Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots -maxdepth 1 -type f -name '*.png' | sort
```

**Output**
```text
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/fallback_sim_snapshot_1_astar.png
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/fallback_sim_snapshot_2_weighted_astar.png
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/fallback_sim_snapshot_3_fringe_search.png
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/mujoco_sim_mujoco_1_astar.png
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/mujoco_sim_mujoco_2_weighted_astar.png
/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/mujoco_sim_mujoco_3_fringe_search.png
```

**Exit status:** 0

## Summary

| Step | Status | Notes |
|---|---|---|
| Deterministic run: astar | PASS | PASS |
| Deterministic run: weighted_astar | PASS | PASS |
| Deterministic run: fringe_search | PASS | PASS |
| Capture regression screenshots | PASS | PASS |
| Collect regression screenshots | PASS | PASS: found 6 file(s) |

### Produced Screenshots

- /Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/fallback_sim_snapshot_1_astar.png
- /Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/fallback_sim_snapshot_2_weighted_astar.png
- /Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/fallback_sim_snapshot_3_fringe_search.png
- /Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/mujoco_sim_mujoco_1_astar.png
- /Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/mujoco_sim_mujoco_2_weighted_astar.png
- /Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/testing/screenshots/mujoco_sim_mujoco_3_fringe_search.png

**Overall status:** PASS
