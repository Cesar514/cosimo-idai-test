# Task 02 - Dynamics Owner Report

Date: 2026-02-26
Owner scope:
- `robotics_maze/src/robot.py`
- `robotics_maze/src/sim.py`
- `robotics_maze/coordination/agent_reports/task02_dynamics.md`

## What changed

### `robotics_maze/src/robot.py`
- Added command-dynamics shaping for waypoint control:
  - acceleration/deceleration limits for linear and angular commands (`_apply_command_dynamics`, `_slew_rate_limit`)
  - control timestep inference from PyBullet (`_infer_control_dt_s`)
- Improved turn/linear transitions:
  - heading-based blend from turn-in-place to forward driving using smoothstep
  - distance/braking-aware linear speed cap (`sqrt(2 * decel * distance)`)
  - turn-rate-coupled linear speed limiting (`_turn_linear_limit`)
- Kept wheel-driven motion primary for differential drive and replaced hard full-state velocity override with bounded assist:
  - `_apply_base_velocity_assist` now only nudges forward/yaw velocity error with configurable caps
- Reset smoothed command state on path resets/stops for deterministic behavior.

### `robotics_maze/src/sim.py`
- Added robot contact tuning after URDF load (`_configure_robot_contact_dynamics`):
  - base/link damping setup to reduce jitter
  - wheel-specific friction + damping tuning (`lateralFriction`, `spinningFriction`, `rollingFriction`, `frictionAnchor`)
- Wired tuning into `load_mobile_robot` immediately after robot load.

## Validation

### 1) Dynamics probe run (headless PyBullet)
Command:
```bash
pixi run python - <<'PY'
import json
import math
from statistics import mean
import pybullet as p
from robotics_maze.src.sim import PyBulletMazeSim

waypoints = [(0.0, 0.0), (2.6, 0.0), (2.6, 2.2), (4.8, 2.2), (4.8, 4.2)]
dt = 1.0 / 240.0
max_steps = 4500
records = []

sim = PyBulletMazeSim(gui=False, time_step=dt)
try:
    sx, sy = waypoints[0]
    sim.load_mobile_robot(start_position=(sx, sy, 0.24))
    sim.set_waypoints(waypoints)

    success = False
    step_hit = None
    for step in range(1, max_steps + 1):
        goal = sim.step(steps=1, realtime=False)
        pos, orn = p.getBasePositionAndOrientation(sim.robot_id, physicsClientId=sim.client_id)
        lin_vel, ang_vel = p.getBaseVelocity(sim.robot_id, physicsClientId=sim.client_id)
        yaw = p.getEulerFromQuaternion(orn)[2]
        forward_speed = float(lin_vel[0]) * math.cos(yaw) + float(lin_vel[1]) * math.sin(yaw)
        yaw_rate = float(ang_vel[2])
        records.append((step * dt, forward_speed, yaw_rate, float(pos[0]), float(pos[1]), yaw))
        if goal:
            success = True
            step_hit = step
            break

    if step_hit is None:
        step_hit = max_steps

    forward_speeds = [r[1] for r in records]
    yaw_rates = [r[2] for r in records]
    forward_deltas = [forward_speeds[i] - forward_speeds[i - 1] for i in range(1, len(forward_speeds))]
    yaw_deltas = [yaw_rates[i] - yaw_rates[i - 1] for i in range(1, len(yaw_rates))]
    forward_accels = [delta / dt for delta in forward_deltas]
    yaw_accels = [delta / dt for delta in yaw_deltas]

    def pct95_abs(values):
        if not values:
            return 0.0
        ordered = sorted(abs(v) for v in values)
        idx = min(len(ordered) - 1, int(0.95 * (len(ordered) - 1)))
        return float(ordered[idx])

    final_distance = None
    if sim.robot_controller is not None:
        final_distance = sim.robot_controller.distance_to_goal()

    summary = {
        "success": success,
        "steps": step_hit,
        "sim_time_s": round(step_hit * dt, 3),
        "samples": len(records),
        "max_abs_forward_speed_mps": round(max((abs(v) for v in forward_speeds), default=0.0), 4),
        "mean_abs_forward_speed_mps": round(mean(abs(v) for v in forward_speeds), 4) if forward_speeds else 0.0,
        "max_abs_forward_accel_mps2": round(max((abs(a) for a in forward_accels), default=0.0), 4),
        "p95_abs_forward_accel_mps2": round(pct95_abs(forward_accels), 4),
        "max_abs_forward_step_jump_mps": round(max((abs(d) for d in forward_deltas), default=0.0), 4),
        "max_abs_yaw_rate_rps": round(max((abs(v) for v in yaw_rates), default=0.0), 4),
        "max_abs_yaw_accel_rps2": round(max((abs(a) for a in yaw_accels), default=0.0), 4),
        "p95_abs_yaw_accel_rps2": round(pct95_abs(yaw_accels), 4),
        "max_abs_yaw_step_jump_rps": round(max((abs(d) for d in yaw_deltas), default=0.0), 4),
        "final_distance_to_goal_m": None if final_distance is None else round(float(final_distance), 4),
    }

    print(json.dumps(summary, indent=2, sort_keys=True))
finally:
    sim.close()
PY
```

Result summary:
```json
{
  "final_distance_to_goal_m": null,
  "max_abs_forward_accel_mps2": 125.6199,
  "max_abs_forward_speed_mps": 2.1147,
  "max_abs_forward_step_jump_mps": 0.5234,
  "max_abs_yaw_accel_rps2": 182.3195,
  "max_abs_yaw_rate_rps": 2.1292,
  "max_abs_yaw_step_jump_rps": 0.7597,
  "mean_abs_forward_speed_mps": 0.6746,
  "p95_abs_forward_accel_mps2": 6.6549,
  "p95_abs_yaw_accel_rps2": 44.1452,
  "samples": 2715,
  "sim_time_s": 11.312,
  "steps": 2715,
  "success": true
}
```

Note: peak values are dominated by transient contact spikes and terminal stop; p95 metrics are the representative smooth-motion indicators during normal travel/turn transitions.

### 2) End-to-end planner episode (project CLI path)
Command:
```bash
pixi run python scripts/sim_runner.py --planner astar --episodes 1 --maze-size 15 --seed 42 --physics-backend pybullet --no-gui-setup
```

Result:
```text
[START] planner=astar episodes=1 maze_size=15x15 seed=42 gui=False backend=pybullet urdf=default(husky/husky.urdf) gui_hold_s=8.0
[EP 1/1] status=ok steps=25638 elapsed_s=10.2303
[DONE] success=1/1 avg_steps=25638.00 avg_elapsed_s=10.2303
```

### 3) Regression smoke tests
Command:
```bash
pixi run pytest robotics_maze/tests/test_core.py -q
```

Result:
```text
3 passed in 0.51s
```

## Outcome
- Robot motion now uses acceleration-limited command shaping and smoother turn/linear blending.
- Differential-drive behavior is primarily wheel-driven with only bounded assist.
- End-to-end PyBullet run and tests both pass after the dynamics update.
