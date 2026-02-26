# Robotics Maze Planner Recommendations

This module documents recommended path-planning algorithms for mobile-robot maze navigation tasks.
Each method is listed with a brief rationale and implementation notes.

## Recommended Planners

### 1. A\* (A-Star)
- **Category**: Heuristic best-first graph search
- **Use case**: Optimal path finding on known, static grid maps
- **Status**: Docs-only — no implementation present in this repository
- **Notes**: Uses an admissible heuristic (e.g. Manhattan or Euclidean distance) to guide search toward the goal. Guarantees optimality when the heuristic does not overestimate.

### 2. Dijkstra's Algorithm
- **Category**: Uniform-cost graph search
- **Use case**: Optimal path finding when no heuristic is available; benchmark comparison
- **Status**: Docs-only — no implementation present in this repository
- **Notes**: Special case of A\* with zero heuristic. Explores all directions uniformly; slower than A\* on large maps.

### 3. D\*-Lite (Dynamic A\*)
- **Category**: Incremental replanning on dynamic maps
- **Use case**: Environments where obstacles appear/disappear during navigation
- **Status**: Docs-only — no implementation present in this repository
- **Notes**: Extends A\* with efficient incremental updates; widely used in real-world mobile-robot applications.

### 4. RRT (Rapidly-exploring Random Tree)
- **Category**: Sampling-based motion planning
- **Use case**: High-dimensional or continuous configuration spaces; robot arms, car-like robots
- **Status**: Docs-only — no implementation present in this repository
- **Notes**: Builds a space-filling tree by random sampling; does not require discretization.

### 5. Wavefront / Breadth-First Search (BFS) Planner
- **Category**: Complete graph search
- **Use case**: Small, fully known grid mazes; guarantees shortest path in unweighted graphs
- **Status**: Docs-only — no implementation present in this repository
- **Notes**: Propagates a wave from goal to start; simple to implement and proves correctness.

### 6. Bug Algorithms (Bug0, Bug1, Bug2, Tangent Bug)
- **Category**: Reactive/sensor-based navigation
- **Use case**: Resource-constrained robots with range sensors; no prior map needed
- **Status**: Docs-only — no implementation present in this repository
- **Notes**: Follow-wall and leave-wall behaviors; provably complete for simply connected obstacles.

### 7. Potential Field Method
- **Category**: Reactive continuous navigation
- **Use case**: Real-time obstacle avoidance in dynamic environments
- **Status**: Docs-only — no implementation present in this repository
- **Notes**: Attractive potential to goal, repulsive potential from obstacles; susceptible to local minima.

## Directory Layout

```
robotics_maze/
├── README.md               # This file — planner recommendations
└── results/
    └── method_recommendation_verification_pre2021.md
```
