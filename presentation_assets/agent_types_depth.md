# Codex Agent Types and Spawn Depth

## Agent Types

| Type | Primary role | Best use |
| --- | --- | --- |
| `default` | Orchestrator | Break down work, route tasks, and merge final outputs. |
| `worker` | Implementer | Make code changes, run checks, and deliver concrete artifacts. |
| `explorer` | Investigator | Answer focused codebase questions quickly with read-heavy analysis. |
| `awaiter` | Watcher | Track long-running jobs and report completion/status back. |

## Spawn Depth (Delegation Levels)

- **Depth 0**: Root coordinator (main agent).
- **Depth 1**: Specialists spawned by root (`worker`, `explorer`, `awaiter`).
- **Depth 2+**: Nested delegation where a specialist spawns another specialist.

Practical heuristic:
- Keep most work at depth 1.
- Use depth 2 only for clearly isolated subproblems.
- Treat depth 3+ as an exception that needs explicit justification.

## Why Depth Helps Orchestration

- **Limits failure blast radius**: shallow trees are easier to debug and recover.
- **Improves ownership clarity**: each branch has a narrow, auditable scope.
- **Reduces coordination overhead**: fewer hops means less context loss.
- **Controls cost and latency**: prevents uncontrolled fan-out of agents and tool calls.
- **Strengthens aggregation checkpoints**: parents can validate branch outputs before merge.

## Slide-Ready Copy

- Type your agents: `default` coordinates, `worker` ships, `explorer` investigates, `awaiter` waits.
- Depth is a control knob: root at 0, specialists at 1, nested delegation only when needed.
- Shallow trees outperform deep trees for reliability, speed, and reviewability.
- Orchestration quality improves when depth, ownership, and checkpoints are explicit.
