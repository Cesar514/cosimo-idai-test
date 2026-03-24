# Multi-Agent Task Board: Robotics Maze Planner

## Goal
Build a runnable Python mobile-robot simulation (mac-friendly) that:
- Loads a URDF mobile robot in a 3D simulation environment.
- Generates mathematical labyrinth maps.
- Solves each map with A* to the center as fast as possible.
- Regenerates a new map each time the robot reaches center.
- Benchmarks multiple alternative planners and reports the fastest.

## Shared Rules
- Each agent writes progress to its own log file in this folder.
- Never edit files owned by another agent unless explicitly asked.
- Keep implementation deterministic and testable.
- Prefer pure-Python + pybullet + numpy for mac compatibility.

## Build Agents (6)
- B1: Project scaffold + CLI runner + dependency files.
- B2: Maze math generation + 3D wall conversion.
- B3: PyBullet sim loop + URDF loading + robot reset/control.
- B4: A* planner and baseline planner interfaces.
- B5: URDF fetch/clone scripts + asset docs.
- B6: Benchmark harness + report generation + basic tests.

## Research Agents (10)
- R1..R10: Alternative methods to A* (SOTA + practical) with runnable candidates.

## Supervisor
- S1: Read all logs, track blockers, and write integration priority.
