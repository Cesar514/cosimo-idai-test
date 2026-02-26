# Speaker Notes (Final Deck Order)

Source order: `agents.pptx` as of 2026-02-26 (`41` slides).
Narrative spine: `role clarity -> guarded execution -> artifact-backed validation`.

## Slide 1 - Multi-agentic Workflows
- Open with the thesis: agents are production-usable when bounded by roles and checkpoints.
- Set expectation: this is an operating playbook, not a product pitch.

## Slide 2 - Event Details and Scope
- Confirm logistics quickly, then lock the objective for the hour.
- State the outcome: attendees leave with a reusable team workflow.

## Slide 3 - Agenda (60 Minutes)
- Preview three acts: foundations, execution mechanics, and risk-managed deployment.
- Signal that Q&A will focus on adoption tradeoffs and governance.

## Slide 4 - Why 2026 Is Different
- Explain the shift from assistant chat to delegated task completion.
- Name the two drivers: stronger reasoning and standardized tool protocols.

## Slide 5 - What Multi-agent Workflow Means
- Define it as specialist roles with explicit contracts and handoffs.
- Stress that orchestration quality matters as much as model quality.

## Slide 6 - Reference Architecture
- Walk left to right: request, plan, execute, verify, release.
- Mark human approval gates at side-effect and merge boundaries.

## Slide 7 - Tool Landscape (As of Feb 26, 2026)
- Date-stamp the comparison to keep claims time-bounded.
- Position tools by workflow fit, not by brand preference.

## Slide 8 - Codex CLI: High-Leverage Features
- Emphasize local repo autonomy, instruction fidelity, and tool breadth.
- Highlight approval modes and typed agents as control primitives.

## Slide 9 - GitHub Copilot Coding Agent
- Position Copilot for asynchronous issue-to-PR throughput.
- Note that success depends on strong acceptance tests and review rigor.

## Slide 10 - Google Jules
- Frame Jules as delegated background execution with checkpoints.
- Reinforce that delegation still requires explicit verification.

## Slide 11 - Gemini CLI in Multi-agent Stacks
- Present Gemini CLI as script-friendly and integration-oriented.
- Contrast flexibility with stricter guardrail-first operator styles.

## Slide 12 - Codex vs Gemini CLI vs Claude: Choice Matters
- Use decision criteria: control strictness, initiative level, and edit behavior.
- Recommend selecting by task risk profile, not headline capability.

## Slide 13 - Using GPT-5.2 Pro (Why It Helps)
- Reserve premium reasoning for hard, branching, high-stakes tasks.
- Tie model routing to leverage, not blanket default usage.

## Slide 14 - Planning Mode: Codex and Gemini
- Describe planning mode as a read-first alignment step before edits.
- Require acceptance criteria before switching to execution mode.

## Slide 15 - Subscription Prices Snapshot (US, Feb 26, 2026)
- Treat pricing as an operating constraint in workflow design.
- Connect spend control to routing policy and role assignment.

## Slide 16 - Local Models: When and Why to Use Them
- Use local models for privacy, latency, and predictable cost.
- Keep a hybrid stack: local for routine, hosted for hard reasoning.

## Slide 17 - Role Split: Planner vs Implementer vs Reviewer
- Define deliverables per role so handoffs are testable.
- Keep reviewer independence to reduce correlated blind spots.

## Slide 18 - Codex Spawn Tree: Agents, Subagents, Max Depth
- Explain depth limits as anti-chaos controls.
- Favor shallow trees with explicit aggregation checkpoints.

## Slide 19 - Codex Agent Types and Why This Is Marvelous
- Map `default`, `worker`, and `explorer` to concrete responsibilities.
- Show typed prompting as a reliability and velocity multiplier.

## Slide 20 - Hardcore Orchestration Pattern
- Present the pattern as a deterministic execution recipe.
- Emphasize branch isolation, automated checks, and evidence gates.

## Slide 21 - skills.md / SKILL.md Patterns
- Define skills as reusable operational packets with clear triggers.
- Stress narrow scope, examples, and script-backed repeatability.

## Slide 22 - How to Create a Skill (skill-creator Workflow)
- Walk the lifecycle: scope, contract, validate, iterate.
- Highlight boundaries and trigger clarity as the main quality levers.

## Slide 23 - Skill Spotlight: create-plan
- Use only when explicit planning is requested.
- Output should reduce rework by clarifying dependencies and success criteria.

## Slide 24 - Skill Spotlight: github-agents-deploy
- Position as portfolio triage with capacity-aware assignment.
- Reinforce plan-first behavior before any automated action.

## Slide 25 - Skill Spotlight: openai-docs
- Frame this as a primary-source gate for OpenAI implementation guidance.
- Emphasize citation discipline to reduce speculative API advice.

## Slide 26 - Skill Spotlight: suggest-improve
- Use for no-new-feature health audits with ranked actions.
- Convert findings into a sequenced engineering backlog.

## Slide 27 - Skill Spotlight: playwright
- Explain deterministic browser validation for UI workflows.
- Capture screenshots, traces, and repro steps as merge evidence.

## Slide 28 - Skill Spotlight: literature-review
- Describe structured search, screening, and synthesis workflows.
- Emphasize deduplication and citation validation for research quality.

## Slide 29 - Skill Spotlight: scientific-report-editor
- Present multi-pass editing as the core quality mechanism.
- Keep math formatting and citation integrity as explicit checks.

## Slide 30 - Skill Spotlight: pr-merger
- Cover end-to-end PR closure with minimal corrective edits.
- Require test validation and explicit merge reasoning.

## Slide 31 - AGENTS.md as Behavioral Control Plane
- Explain AGENTS.md as durable repo policy for agent behavior.
- Cover precedence rules and why they reduce repeated review drift.

## Slide 32 - MCP Basics: Why It Matters
- Define MCP primitives and their interoperability value.
- Connect standardization to faster, reusable tool integration.

## Slide 33 - MCP in Practice: Trust and Safety
- Enforce least privilege, trusted servers, and scoped credentials.
- Keep approval gates and audit trails mandatory for side effects.

## Slide 34 - Live Walkthrough: Blank Repo to PoC
- Narrate the full loop: plan, parallel execution, review, integrate.
- Timebox live steps and pivot to artifacts if any command stalls.

## Slide 35 - Cesar's Real Workflow (Control Loop)
- Share practical operator habits: depth control, cadence, and git hygiene.
- Distill these habits into team-adoptable rules.

## Slide 36 - Debug Loop with Agents
- Run the loop: reproduce, diagnose, patch, verify, document.
- Keep minimal repros and targeted tests before broader reruns.

## Slide 37 - Testing Workflows with Agents
- Cover edge-case generation, flake detection, and CI gate enforcement.
- Prioritize test stability and signal quality over raw test count.

## Slide 38 - Research and Writing Workflows
- Show parallelism from source triage to draft refinement.
- Treat reproducibility artifacts as required outputs, not extras.

## Slide 39 - Experimental Robotics: Real World as Tools
- Model hardware, sensors, and controllers as tool interfaces.
- Feed real telemetry into the loop and keep sim-to-real transitions conservative.

## Slide 40 - High Risk, High Reward in Robot Agent Systems
- Balance upside against safety, governance, and actuation risk.
- Require staged autonomy and explicit failure containment.

## Slide 41 - Ralph Wiggum Technique (Actual Definition)
- Close with the loop: fresh context runs plus externalized state.
- Land the principle: simple deterministic loops beat fragile choreography.
