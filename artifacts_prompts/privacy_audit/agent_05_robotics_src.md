# Privacy Audit Report: `robotics_maze/src/` (Agent 05)

## Scope
- Audited path: `robotics_maze/src/`
- File types reviewed: `.py`, `.md`, and tracked `.pyc` under `__pycache__/`
- Focus: private info leakage in code/comments/strings (local paths, credentials, internal endpoints)

## Findings

### 1) High: Local machine absolute path leakage in committed bytecode
Tracked Python bytecode files (`.pyc`) contain embedded absolute local filesystem paths including username and workspace layout:

- Leaked prefix observed: `/Users/cesar514/Documents/agent_programming/cosimi-idai-test/robotics_maze/src/...`

Affected tracked files with evidence of `/Users/...` strings:
- `robotics_maze/src/__pycache__/benchmark.cpython-311.pyc`
- `robotics_maze/src/__pycache__/geometry.cpython-311.pyc`
- `robotics_maze/src/__pycache__/heuristics.cpython-311.pyc`
- `robotics_maze/src/__pycache__/maze.cpython-311.pyc`
- `robotics_maze/src/__pycache__/planners.cpython-311.pyc`
- `robotics_maze/src/__pycache__/robot.cpython-311.pyc`
- `robotics_maze/src/__pycache__/sim.cpython-311.pyc`
- `robotics_maze/src/alt_planners/__pycache__/r1_weighted_astar.cpython-311.pyc`
- `robotics_maze/src/alt_planners/__pycache__/r2_bidirectional_astar.cpython-311.pyc`
- `robotics_maze/src/alt_planners/__pycache__/r3_theta_star.cpython-311.pyc`
- `robotics_maze/src/alt_planners/__pycache__/r4_idastar.cpython-311.pyc`
- `robotics_maze/src/alt_planners/__pycache__/r5_jump_point_search.cpython-311.pyc`
- `robotics_maze/src/alt_planners/__pycache__/r6_lpa_star.cpython-311.pyc`
- `robotics_maze/src/alt_planners/__pycache__/r7_beam_search.cpython-311.pyc`
- `robotics_maze/src/alt_planners/__pycache__/r8_fringe_search.cpython-311.pyc`
- `robotics_maze/src/alt_planners/__pycache__/r9_bidirectional_bfs.cpython-311.pyc`

Risk:
- Exposes local username (`cesar514`) and machine directory structure.
- Increases reconnaissance value of public/internal repository artifacts.

Recommended remediation:
1. Stop committing bytecode artifacts: add `__pycache__/` and `*.pyc` to `.gitignore`.
2. Remove tracked `.pyc` files from the repository and regenerate locally as needed.
3. If this repository has been distributed externally, consider history cleanup for those artifacts.

## No Additional Sensitive Findings in Source Text
Across non-bytecode source text under `robotics_maze/src/` (`.py`, `.md`):
- No hardcoded credentials/tokens/secrets detected.
- No internal/private endpoints detected (`localhost`, RFC1918 IPs, `.internal/.corp/.local` domains).
- No hardcoded local filesystem paths detected.

## Notes
- This report is audit-only and intentionally does not modify source files.
