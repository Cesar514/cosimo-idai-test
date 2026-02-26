# Task 07 - Dijkstra Planner Owner

## Scope
- `robotics_maze/src/alt_planners/r11_dijkstra.py`
- `robotics_maze/src/planners.py`
- `robotics_maze/coordination/agent_reports/task07_dijkstra.md`

## Implementation
- Added a new alternative planner module: `alt_planners/r11_dijkstra.py`.
- Implemented `plan_dijkstra(grid, start, goal, allow_diagonal=False)` with Dijkstra search and benchmark-style metrics.
- Added `R11DijkstraPlanner` + `create_planner(...)` so `main.py` can load it with `--planner r11_dijkstra` through module discovery.
- Registered Dijkstra aliases in `planners.py` so it is selectable from the core planner registry:
  - `r11_dijkstra`
  - `uniform_cost_search`
  - `ucs`

## Usage
- Baseline registry usage:
  - `python3 robotics_maze/src/main.py --planner dijkstra`
- New alias usage:
  - `python3 robotics_maze/src/main.py --planner r11_dijkstra`
  - `python3 robotics_maze/src/main.py --planner uniform_cost_search`
  - `python3 robotics_maze/src/main.py --planner ucs`
- Direct module function:
  - `from alt_planners.r11_dijkstra import plan_dijkstra`

## Minimal Run/Check
Command run (registry + module check):

```bash
cd robotics_maze/src && python3 - <<'PY'
import planners
from alt_planners.r11_dijkstra import plan_dijkstra

grid = [
    [0, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 0, 0, 0],
    [0, 1, 1, 0],
]

res = planners.plan_path("r11_dijkstra", grid, (0, 0), (3, 3))
print("r11_registered", "r11_dijkstra" in planners.list_planners())
print("planner_path_len", len(res["path"]))
print("planner_expanded", res["expanded_nodes"])

path, metrics = plan_dijkstra(grid, (0, 0), (3, 3))
print("module_path_len", len(path))
print("module_status", metrics["status"])
print("module_cost", metrics["path_cost"])
PY
```

Observed output:

```text
r11_registered True
planner_path_len 7
planner_expanded 9
module_path_len 7
module_status ok
module_cost 6.0
```

CLI smoke check:

```bash
python3 robotics_maze/src/main.py --planner r11_dijkstra --episodes 1 --maze-size 6 --seed 7 --physics-backend auto
```

Observed output:

```text
[INFO] Maze generator loaded from maze.create_maze_generator
[INFO] Planner loaded from alt_planners.r11_dijkstra.create_planner
[INFO] Simulator loaded from sim.create_simulator
[START] planner=r11_dijkstra episodes=1 maze_size=6x6 seed=7 gui=False backend=auto urdf=default(husky/husky.urdf) gui_hold_s=8.0
[WARN] PyBullet is unavailable; falling back to MuJoCo.
[EP 1/1] status=ok steps=41 elapsed_s=0.0028
[DONE] success=1/1 avg_steps=41.00 avg_elapsed_s=0.0028
```

Additional syntax check:

```bash
python3 -m py_compile robotics_maze/src/planners.py robotics_maze/src/alt_planners/r11_dijkstra.py
```
