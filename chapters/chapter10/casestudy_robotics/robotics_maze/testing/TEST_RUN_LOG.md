# Robotics Maze Simulation Test Run Log

- Date (UTC): 2026-02-26T22:05:41Z
- Working directory: .
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
python3 robotics_maze/scripts/capture_regression_screenshots.py --output-dir robotics_maze/testing/screenshots --require-mujoco 
```

**Output**
```text
[INFO] running: python3 robotics_maze/scripts/generate_mujoco_screenshots.py --output-dir robotics_maze/testing/screenshots --filename-prefix mujoco_
robotics_maze/testing/screenshots/mujoco_sim_mujoco_1_astar.png
robotics_maze/testing/screenshots/mujoco_sim_mujoco_2_weighted_astar.png
robotics_maze/testing/screenshots/mujoco_sim_mujoco_3_fringe_search.png
[INFO] running: python3 robotics_maze/scripts/generate_sim_screenshots.py --output-dir robotics_maze/testing/screenshots --filename-prefix fallback_
robotics_maze/testing/screenshots/fallback_sim_snapshot_1_astar.png
robotics_maze/testing/screenshots/fallback_sim_snapshot_2_weighted_astar.png
robotics_maze/testing/screenshots/fallback_sim_snapshot_3_fringe_search.png
[INFO] generated screenshots:
robotics_maze/testing/screenshots/fallback_sim_snapshot_1_astar.png
robotics_maze/testing/screenshots/fallback_sim_snapshot_2_weighted_astar.png
robotics_maze/testing/screenshots/fallback_sim_snapshot_3_fringe_search.png
robotics_maze/testing/screenshots/mujoco_sim_mujoco_1_astar.png
robotics_maze/testing/screenshots/mujoco_sim_mujoco_2_weighted_astar.png
robotics_maze/testing/screenshots/mujoco_sim_mujoco_3_fringe_search.png

```

**Exit status:** 0

## Collect regression screenshots

**Command**
```bash
find robotics_maze/testing/screenshots -maxdepth 1 -type f -name '*.png' | sort
```

**Output**
```text
robotics_maze/testing/screenshots/fallback_sim_snapshot_1_astar.png
robotics_maze/testing/screenshots/fallback_sim_snapshot_2_weighted_astar.png
robotics_maze/testing/screenshots/fallback_sim_snapshot_3_fringe_search.png
robotics_maze/testing/screenshots/mujoco_sim_mujoco_1_astar.png
robotics_maze/testing/screenshots/mujoco_sim_mujoco_2_weighted_astar.png
robotics_maze/testing/screenshots/mujoco_sim_mujoco_3_fringe_search.png
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

- robotics_maze/testing/screenshots/fallback_sim_snapshot_1_astar.png
- robotics_maze/testing/screenshots/fallback_sim_snapshot_2_weighted_astar.png
- robotics_maze/testing/screenshots/fallback_sim_snapshot_3_fringe_search.png
- robotics_maze/testing/screenshots/mujoco_sim_mujoco_1_astar.png
- robotics_maze/testing/screenshots/mujoco_sim_mujoco_2_weighted_astar.png
- robotics_maze/testing/screenshots/mujoco_sim_mujoco_3_fringe_search.png

**Overall status:** PASS

---

## Verification Cycle: 2026-02-27 (UTC)

- Logged at (UTC): 2026-02-27T10:31:08Z
- Working directory: .
- Scope: Benchmark harness + paper build verification

## Benchmark verification

- Start (UTC): 2026-02-27T10:30:57Z
- End (UTC): 2026-02-27T10:30:58Z
- Status: PASS

**Command**
```bash
python3 robotics_maze/src/benchmark.py --mazes 12 --width 11 --height 11 --seed 7 --algorithm backtracker --output-dir /tmp/cosimi_cycle_benchmark_verify
```

**Output summary**
```text
Wrote: /tmp/cosimi_cycle_benchmark_verify/benchmark_results.csv
Wrote: /tmp/cosimi_cycle_benchmark_verify/benchmark_summary.md
Planner comparison (12 mazes, 11x11, algorithm=backtracker, seed=7):
1) r1_weighted_astar  100.0% (12/12)  comparable_time_ms=0.28
2) r7_beam_search     100.0% (12/12)  comparable_time_ms=0.34
3) greedy_best_first  100.0% (12/12)  comparable_time_ms=0.38
...
12) r4_idastar        100.0% (12/12)  comparable_time_ms=9.04
```

**Artifacts**
```text
/tmp/cosimi_cycle_benchmark_verify/benchmark_results.csv
/tmp/cosimi_cycle_benchmark_verify/benchmark_summary.md
```

**Exit status:** 0

## Paper build verification

- Start (UTC): 2026-02-27T10:31:08Z
- End (UTC): 2026-02-27T10:31:08Z
- Status: PASS

**Command**
```bash
make -C paper/ieee_tro_robotics_maze pdf
```

**Output summary**
```text
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
Latexmk: Nothing to do for 'main.tex'.
Latexmk: All targets (main.pdf) are up-to-date
```

**Artifact check**
```text
paper/ieee_tro_robotics_maze/main.pdf (exists)
```

**Exit status:** 0

## Cycle Summary

| Step | Status | Notes |
|---|---|---|
| Benchmark verification | PASS | 12 planners succeeded on 12/12 mazes; summary + CSV written to `/tmp/cosimi_cycle_benchmark_verify`. |
| Paper build verification | PASS | `make pdf` succeeded; LaTeX target already up-to-date. |

**Overall cycle status:** PASS
