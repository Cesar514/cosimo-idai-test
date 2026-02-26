# Factual Risk Audit — agents.pptx

Legend: `stable` = generally durable; `needs-date` = time-sensitive/version-sensitive; `uncertain` = subjective, unverified, or likely to be contested without source.

## Slide 1: Multi-agentic Workflows
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Orchestrating Coding Agents with CLI Tools, skills.md, and MCPs | `stable` | Use this pattern: orchestrating Coding Agents with CLI Tools, skills.md, and MCPs. |
| Cesar Contreras \| Friday 27 February 2026 \| Elm House 214 + Teams | `needs-date` | As of Feb 26, 2026, cesar Contreras \| Friday 27 February 2026 \| Elm House 214 + Teams; confirm current docs/pricing/status before publication. |
| Lunch at 12:00 | `needs-date` | As of Feb 26, 2026, lunch at 12:00; confirm current docs/pricing/status before publication. |

## Slide 2: Event Details and Scope
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Date: Friday 27 February 2026 \| Time: 11:00 (lunch at 12:00) | `needs-date` | As of Feb 26, 2026, date: Friday 27 February 2026 \| Time: 11:00 (lunch at 12:00); confirm current docs/pricing/status before publication. |
| Location: Elm House 214 + Teams | `stable` | Use this pattern: location: Elm House 214 + Teams. |
| Lead: Cesar Contreras | `stable` | Use this pattern: lead: Cesar Contreras. |
| Goal: practical multi-agent workflows for research code | `stable` | Use this pattern: goal: practical multi-agent workflows for research code. |
| Outcome: repeatable path from idea to tested proof-of-concept | `stable` | Use this pattern: outcome: repeatable path from idea to tested proof-of-concept. |

## Slide 3: Agenda (60 Minutes)
| Claim | Flag | Safer alternative wording |
|---|---|---|
| 11:00-11:10: Why agents now + key definitions | `needs-date` | As of Feb 26, 2026, 11:00-11:10: Why agents now + key definitions; confirm current docs/pricing/status before publication. |
| 11:10-11:25: Tooling landscape (Codex, Copilot, Jules, Gemini, MCP) | `needs-date` | As of Feb 26, 2026, 11:10-11:25: Tooling landscape (Codex, Copilot, Jules, Gemini, MCP); confirm current docs/pricing/status before publication. |
| 11:25-11:45: Live repo walkthrough with role-split agents | `needs-date` | As of Feb 26, 2026, 11:25-11:45: Live repo walkthrough with role-split agents; confirm current docs/pricing/status before publication. |
| 11:45-11:55: Debug, testing, research, and writing workflows | `needs-date` | As of Feb 26, 2026, 11:45-11:55: Debug, testing, research, and writing workflows; confirm current docs/pricing/status before publication. |
| 11:55-12:00: Robotics risk/reward, adoption plan, Q&A | `needs-date` | As of Feb 26, 2026, 11:55-12:00: Robotics risk/reward, adoption plan, Q&A; confirm current docs/pricing/status before publication. |

## Slide 4: Why 2026 Is Different
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Coding agents moved from chat help to autonomous PR-style execution | `uncertain` | Coding agents moved from chat help to autonomous PR-style execution; validate with your own benchmark or documented source. |
| MCP-style protocols made tool integrations composable | `stable` | Use this pattern: mCP-style protocols made tool integrations composable. |
| Larger context + stronger reasoning enable longer task chains | `stable` | Use this pattern: larger context + stronger reasoning enable longer task chains. |
| Teams can parallelize exploration, implementation, and review | `stable` | Use this pattern: teams can parallelize exploration, implementation, and review. |
| Bottleneck shifted from typing speed to orchestration quality | `uncertain` | Bottleneck shifted from typing speed to orchestration quality; validate with your own benchmark or documented source. |

## Slide 5: What Multi-agent Workflow Means
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Multiple specialized agents coordinate on one objective | `stable` | Use this pattern: multiple specialized agents coordinate on one objective. |
| Planner decomposes work into parallelizable tasks | `stable` | Use this pattern: planner decomposes work into parallelizable tasks. |
| Implementers execute code, tests, and integrations | `stable` | Use this pattern: implementers execute code, tests, and integrations. |
| Reviewer/critic validates correctness and regression risk | `stable` | Use this pattern: reviewer/critic validates correctness and regression risk. |
| Human sets priorities, trust boundaries, and final approvals | `stable` | Use this pattern: human sets priorities, trust boundaries, and final approvals. |

## Slide 6: Reference Architecture
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Inputs: issue statement, repo state, tests, constraints | `stable` | Use this pattern: inputs: issue statement, repo state, tests, constraints. |
| Planner agent: task graph + acceptance criteria | `stable` | Use this pattern: planner agent: task graph + acceptance criteria. |
| Implementer agents: code changes + local validation | `stable` | Use this pattern: implementer agents: code changes + local validation. |
| Reviewer agent: risk scan + quality bar checks | `stable` | Use this pattern: reviewer agent: risk scan + quality bar checks. |
| Operator (human): checkpoint approvals + merge decisions | `stable` | Use this pattern: operator (human): checkpoint approvals + merge decisions. |

## Slide 7: Tool Landscape (As of Feb 26, 2026)
| Claim | Flag | Safer alternative wording |
|---|---|---|
| OpenAI Codex CLI: local coding agent with multi-agent + MCP | `stable` | Use this pattern: openAI Codex CLI: local coding agent with multi-agent + MCP. |
| GitHub Copilot coding agent: issue-to-PR automation in GitHub | `stable` | Use this pattern: gitHub Copilot coding agent: issue-to-PR automation in GitHub. |
| Google Jules/Jules API: asynchronous coding agent + API automation | `stable` | Use this pattern: google Jules/Jules API: asynchronous coding agent + API automation. |
| Gemini CLI: open-source terminal agent with MCP extensibility | `stable` | Use this pattern: gemini CLI: open-source terminal agent with MCP extensibility. |
| Shared denominator: prompts + tools + policy + eval loops | `stable` | Use this pattern: shared denominator: prompts + tools + policy + eval loops. |

## Slide 8: Codex CLI: High-Leverage Features
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Local repo read/edit/run with explicit approval modes | `stable` | Use this pattern: local repo read/edit/run with explicit approval modes. |
| Non-interactive automation via codex exec workflows | `stable` | Use this pattern: non-interactive automation via codex exec workflows. |
| Experimental multi-agent orchestration with specialized roles | `stable` | Use this pattern: experimental multi-agent orchestration with specialized roles. |
| First-party web search (cached or live modes) | `stable` | Use this pattern: first-party web search (cached or live modes). |
| Built-in MCP support for external tools and context providers | `stable` | Use this pattern: built-in MCP support for external tools and context providers. |

## Slide 9: GitHub Copilot Coding Agent
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Strong fit for issue-driven asynchronous implementation | `stable` | Use this pattern: strong fit for issue-driven asynchronous implementation. |
| Operates directly in GitHub pull request workflows | `stable` | Use this pattern: operates directly in GitHub pull request workflows. |
| Useful for repetitive backlog and maintenance tasks | `stable` | Use this pattern: useful for repetitive backlog and maintenance tasks. |
| Current constraints: preview status and restricted execution model | `needs-date` | As of Feb 26, 2026, current constraints: preview status and restricted execution model; confirm current docs/pricing/status before publication. |
| Best used as implementer with independent reviewer checks | `uncertain` | Recommended used as implementer with independent reviewer checks; validate with your own benchmark or documented source. |

## Slide 10: Google Jules
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Jules targets asynchronous coding tasks on codebases | `stable` | Use this pattern: jules targets asynchronous coding tasks on codebases. |
| Good pattern: dispatch tasks, collect artifacts, review diffs | `stable` | Use this pattern: good pattern: dispatch tasks, collect artifacts, review diffs. |
| Useful for long-running background work | `stable` | Use this pattern: useful for long-running background work. |
| Needs strict acceptance tests before delegated execution | `stable` | Use this pattern: needs strict acceptance tests before delegated execution. |

## Slide 11: Gemini CLI in Multi-agent Stacks
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Open-source terminal agent for coding and scripting workflows | `stable` | Use this pattern: open-source terminal agent for coding and scripting workflows. |
| Useful for rapid implementation and repository exploration | `stable` | Use this pattern: useful for rapid implementation and repository exploration. |
| Extensible with MCP for custom integrations | `stable` | Use this pattern: extensible with MCP for custom integrations. |
| Can be paired with Gemini Code Assist for IDE workflows | `stable` | Use this pattern: can be paired with Gemini Code Assist for IDE workflows. |
| Treat outputs as proposals and enforce test/eval gates | `stable` | Use this pattern: treat outputs as proposals and enforce test/eval gates. |

## Slide 12: Codex vs Gemini CLI vs Claude: Choice Matters
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Codex: strongest when you want strict rule-following (AGENTS.md, skills, explicit constraints). | `uncertain` | Codex: often strongest in our tests when you want strict rule-following (AGENTS.md, skills, explicit constraints); validate with your own benchmark or documented source. |
| Gemini CLI: often takes more initiative and may deviate if your guardrails are loose. | `stable` | Gemini CLI: often takes more initiative and may deviate if your guardrails can be loose. |
| Claude: tends to over-improve and expand scope beyond the exact ask. | `stable` | Use this pattern: claude: tends to over-improve and expand scope beyond the exact ask. |
| Operational takeaway: same prompt can produce very different behaviors across agents. | `stable` | Use this pattern: operational takeaway: same prompt can produce very different behaviors across agents. |
| Your choice matters: pick the agent by control needs, risk tolerance, and review bandwidth. | `stable` | Use this pattern: your choice matters: pick the agent by control needs, risk tolerance, and review bandwidth. |

## Slide 13: Using GPT-5.2 Pro (Why It Helps)
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Best for hardest tasks: deep reasoning, multi-step code edits, and agentic tool-use chains. | `uncertain` | Recommended for hardest tasks: deep reasoning, multi-step code edits, and agentic tool-use chains; validate with your own benchmark or documented source. |
| OpenAI positions GPT-5.2 Pro as the highest-capability GPT-5.2 tier (Responses API only). | `uncertain` | OpenAI positions GPT-5.2 Pro as the highest-capability GPT-5.2 tier (Responses API only); validate with your own benchmark or documented source. |
| High leverage in your workflow: architecture decisions, risky refactors, and root-cause analysis. | `uncertain` | High leverage in your workflow: architecture decisions, risky refactors, and root-cause analysis; validate with your own benchmark or documented source. |
| Pattern: use GPT-5.2 Pro for planning/critical reviews; use faster models for implementation loops. | `stable` | Use this pattern: pattern: use GPT-5.2 Pro for planning/critical reviews; use faster models for implementation loops. |
| When uncertainty and downside risk are high, paying for stronger reasoning is usually net-positive. | `uncertain` | When uncertainty and downside risk can be high, paying for stronger reasoning can be usually net-positive; validate with your own benchmark or documented source. |

## Slide 14: Planning Mode: Codex and Gemini
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Codex: collaboration modes include plan mode (useful for design-first, read-before-write workflows). | `stable` | Use this pattern: codex: collaboration modes include plan mode (useful for design-first, read-before-write workflows). |
| Gemini CLI: `/plan` switches to read-only planning mode (feature marked experimental). | `stable` | Use this pattern: gemini CLI: `/plan` switches to read-only planning mode (feature marked experimental). |
| Gemini also supports `--approval-mode=plan` and explicit plan artifact generation before coding. | `stable` | Use this pattern: gemini also supports `--approval-mode=plan` and explicit plan artifact generation before coding. |
| Common benefit: better approach selection, fewer blind edits, cleaner handoff to implementer agents. | `stable` | Use this pattern: common benefit: better approach selection, fewer blind edits, cleaner handoff to implementer agents. |
| Note: in Gemini docs, enter-plan tool is unavailable while running in YOLO mode. | `stable` | Note: in Gemini docs, enter-plan tool can be unavailable while running in YOLO mode. |

## Slide 15: Subscription Prices Snapshot (US, Feb 26, 2026)
| Claim | Flag | Safer alternative wording |
|---|---|---|
| OpenAI ChatGPT: Plus $20/mo, Pro $200/mo, Business $25/user/mo (annual) (Enterprise: contact sales). | `needs-date` | As of Feb 26, 2026, openAI ChatGPT: Plus $20/mo, Pro $200/mo, Business $25/user/mo (annual) (Enterprise: contact sales); confirm current docs/pricing/status before publication. |
| Codex CLI: no separate subscription; included with ChatGPT Plus/Pro/Business/Edu/Enterprise. | `stable` | Use this pattern: codex CLI: no separate subscription; included with ChatGPT Plus/Pro/Business/Edu/Enterprise. |
| GitHub Copilot: Pro $10/mo, Pro+ $39/mo, Business $19/user/mo, Enterprise $39/user/mo. | `needs-date` | As of Feb 26, 2026, gitHub Copilot: Pro $10/mo, Pro+ $39/mo, Business $19/user/mo, Enterprise $39/user/mo; confirm current docs/pricing/status before publication. |
| Google AI plans: AI Pro $19.99/mo; AI Ultra launched at $249.99/mo in the US (pricing/promos can change). | `needs-date` | As of Feb 26, 2026, google AI plans: AI Pro $19.99/mo; AI Ultra launched at $249.99/mo in the US (pricing/promos can change); confirm current docs/pricing/status before publication. |
| Jules: no separate public subscription on its own page; usage limits are tied to AI Pro/Ultra tiers. | `stable` | Jules: no separate public subscription on its own page; usage limits can be tied to AI Pro/Ultra tiers. |

## Slide 16: Local Models: When and Why to Use Them
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Codex supports local OSS providers (`--oss`) via Ollama or LM Studio in config. | `stable` | Use this pattern: codex supports local OSS providers (`--oss`) via Ollama or LM Studio in config. |
| OpenAI open-weight options: `gpt-oss-20b` (local/specialized) and `gpt-oss-120b` (single H100 class). | `stable` | Use this pattern: openAI open-weight options: `gpt-oss-20b` (local/specialized) and `gpt-oss-120b` (single H100 class). |
| Cost model shift: lower subscription dependence, higher compute/ops responsibility. | `stable` | Use this pattern: cost model shift: lower subscription dependence, higher compute/ops responsibility. |
| Best fit: privacy-sensitive data, air-gapped workflows, custom fine-tunes, deterministic local tooling. | `uncertain` | Recommended fit: privacy-sensitive data, air-gapped workflows, custom fine-tunes, deterministic local tooling; validate with your own benchmark or documented source. |
| Practical strategy: hybrid stack (local models for bulk loops, frontier models for critical reasoning). | `stable` | Use this pattern: practical strategy: hybrid stack (local models for bulk loops, frontier models for critical reasoning). |

## Slide 17: Role Split: Planner vs Implementer vs Reviewer
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Planner: defines task DAG, dependencies, and rollback logic | `stable` | Use this pattern: planner: defines task DAG, dependencies, and rollback logic. |
| Implementer: ships smallest safe patches per task node | `stable` | Use this pattern: implementer: ships smallest safe patches per task node. |
| Reviewer: adversarial check for bugs, security, regressions | `stable` | Use this pattern: reviewer: adversarial check for bugs, security, regressions. |
| Release agent (optional): changelog, versioning, deployment notes | `stable` | Use this pattern: release agent (optional): changelog, versioning, deployment notes. |
| Human remains accountable for risk decisions and shipping | `stable` | Use this pattern: human remains accountable for risk decisions and shipping. |

## Slide 18: Codex Spawn Tree: Agents, Subagents, Max Depth
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Root session starts at depth 0; parent can spawn child agents for parallel tasks. | `stable` | Use this pattern: root session starts at depth 0; parent can spawn child agents for parallel tasks. |
| Children can spawn subagents recursively only when depth budget allows. | `stable` | Use this pattern: children can spawn subagents recursively only when depth budget allows. |
| `agents.max_depth` limits nesting: default 1 = root -> child only (no grandchild). | `stable` | Use this pattern: `agents.max_depth` limits nesting: default 1 = root -> child only (no grandchild). |
| `agents.max_threads` limits concurrent open agent threads to avoid overload. | `needs-date` | As of Feb 26, 2026, `agents.max_threads` limits concurrent open agent threads to avoid overload; confirm current docs/pricing/status before publication. |
| Parent orchestrates lifecycle with spawn/send_input/wait/resume/close and merges outputs. | `stable` | Use this pattern: parent orchestrates lifecycle with spawn/send_input/wait/resume/close and merges outputs. |

## Slide 19: Codex Agent Types and Why This Is Marvelous
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Built-in roles: `default`, `worker`, `explorer`, and `monitor` (plus custom roles). | `stable` | Use this pattern: built-in roles: `default`, `worker`, `explorer`, and `monitor` (plus custom roles). |
| `worker` focuses on execution/fixes; `explorer` on read-heavy code discovery; `monitor` on long waits/polling. | `stable` | Use this pattern: `worker` focuses on execution/fixes; `explorer` on read-heavy code discovery; `monitor` on long waits/polling. |
| Each role can have its own model, reasoning effort, sandbox mode, and instructions. | `stable` | Use this pattern: each role can have its own model, reasoning effort, sandbox mode, and instructions. |
| Marvelous effect: role specialization + parallelism reduces context rot and increases throughput. | `uncertain` | Marvelous effect: role specialization + parallelism reduces context rot and increases throughput; validate with your own benchmark or documented source. |
| You keep control with depth/thread limits and permissions while still moving much faster. | `stable` | Use this pattern: you keep control with depth/thread limits and permissions while still moving much faster. |

## Slide 20: Hardcore Orchestration Pattern
| Claim | Flag | Safer alternative wording |
|---|---|---|
| 1) Set measurable goal and explicit stop conditions | `stable` | Use this pattern: 1) Set measurable goal and explicit stop conditions. |
| 2) Spawn parallel implementers on isolated branches | `stable` | Use this pattern: 2) Spawn parallel implementers on isolated branches. |
| 3) Run automated checks after every patch | `stable` | Use this pattern: 3) Run automated checks after every patch. |
| 4) Reviewer compares alternatives with evidence | `stable` | Use this pattern: 4) Reviewer compares alternatives with evidence. |
| 5) Approve based on test artifacts, not model confidence | `stable` | Use this pattern: 5) Approve based on test artifacts, not model confidence. |

## Slide 21: skills.md / SKILL.md Patterns
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Package repeatable workflows as skills: instructions + scripts + assets | `stable` | Use this pattern: package repeatable workflows as skills: instructions + scripts + assets. |
| Keep skills narrow: setup, test triage, docs, release notes | `stable` | Use this pattern: keep skills narrow: setup, test triage, docs, release notes. |
| Embed deterministic scripts in scripts/ for repeatability | `stable` | Use this pattern: embed deterministic scripts in scripts/ for repeatability. |
| Use clear descriptions for reliable triggering | `stable` | Use this pattern: use clear descriptions for reliable triggering. |
| Version and review skills with normal PR discipline | `stable` | Use this pattern: version and review skills with normal PR discipline. |

## Slide 22: How to Create a Skill (skill-creator Workflow)
| Claim | Flag | Safer alternative wording |
|---|---|---|
| 1) Define concrete usage examples and identify reusable resources (scripts, references, assets). | `stable` | Use this pattern: 1) Define concrete usage examples and identify reusable resources (scripts, references, assets). |
| 2) Initialize scaffold with `scripts/init_skill.py <skill-name> --path <dir> --resources ...`. | `stable` | Use this pattern: 2) Initialize scaffold with `scripts/init_skill.py <skill-name> --path <dir> --resources ...`. |
| 3) Write `SKILL.md`: frontmatter only `name` + `description`; keep body concise and imperative. | `stable` | Use this pattern: 3) Write `SKILL.md`: frontmatter only `name` + `description`; keep body concise and imperative. |
| 4) Add deterministic scripts, needed references, and optional assets; generate `agents/openai.yaml` metadata. | `stable` | Use this pattern: 4) Add deterministic scripts, needed references, and optional assets; generate `agents/openai.yaml` metadata. |
| 5) Validate with `scripts/quick_validate.py <skill-folder>`, test scripts, then iterate from real usage feedback. | `stable` | Use this pattern: 5) Validate with `scripts/quick_validate.py <skill-folder>`, test scripts, then iterate from real usage feedback. |

## Slide 23: Skill Spotlight: create-plan
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Purpose: generate a concise, actionable plan when planning is explicitly requested. | `stable` | Purpose: generate a concise, actionable plan when planning can be explicitly requested. |
| Core behavior: fast read-only context scan + only blocking follow-up questions. | `stable` | Use this pattern: core behavior: fast read-only context scan + only blocking follow-up questions. |
| Output contract: #Plan with scope, ordered checklist, and open questions. | `stable` | Use this pattern: output contract: #Plan with scope, ordered checklist, and open questions. |
| Why it matters here: aligns planner-agent behavior before parallel execution. | `stable` | Use this pattern: why it matters here: aligns planner-agent behavior before parallel execution. |
| Best use: kickoff for complex coding/research tasks with clear acceptance criteria. | `uncertain` | Recommended use: kickoff for complex coding/research tasks with clear acceptance criteria; validate with your own benchmark or documented source. |

## Slide 24: Skill Spotlight: github-agents-deploy
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Purpose: triage open GitHub issues/PRs and deploy Copilot/Jules/Codex review strategically. | `stable` | Use this pattern: purpose: triage open GitHub issues/PRs and deploy Copilot/Jules/Codex review strategically. |
| Core behavior: MCP-only GitHub operations, capacity-aware assignment, no duplicate deployment. | `stable` | Use this pattern: core behavior: MCP-only GitHub operations, capacity-aware assignment, no duplicate deployment. |
| Safety pattern: draft per-issue/per-PR plan first, execute only after user approval. | `stable` | Use this pattern: safety pattern: draft per-issue/per-PR plan first, execute only after user approval. |
| Why it matters here: operationalizes your issue-to-agent dispatch workflow at scale. | `stable` | Use this pattern: why it matters here: operationalizes your issue-to-agent dispatch workflow at scale. |
| Best use: weekly triage to keep agent workloads balanced and visible. | `uncertain` | Recommended use: weekly triage to keep agent workloads balanced and visible; validate with your own benchmark or documented source. |

## Slide 25: Skill Spotlight: openai-docs
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Purpose: fetch current OpenAI guidance from official docs with citations. | `needs-date` | As of Feb 26, 2026, purpose: fetch current OpenAI guidance from official docs with citations; confirm current docs/pricing/status before publication. |
| Core behavior: search + fetch via OpenAI Docs MCP before any web fallback. | `stable` | Use this pattern: core behavior: search + fetch via OpenAI Docs MCP before any web fallback. |
| Output quality: source-grounded API/tooling guidance with reduced speculation risk. | `stable` | Use this pattern: output quality: source-grounded API/tooling guidance with reduced speculation risk. |
| Why it matters here: keeps agent architecture choices aligned with latest platform reality. | `stable` | Use this pattern: why it matters here: keeps agent architecture choices aligned with latest platform reality. |
| Best use: model/tool capability checks before implementing new workflow patterns. | `uncertain` | Recommended use: model/tool capability checks before implementing new workflow patterns; validate with your own benchmark or documented source. |

## Slide 26: Skill Spotlight: suggest-improve
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Purpose: deep codebase health review with ranked, actionable improvements (no new features). | `stable` | Use this pattern: purpose: deep codebase health review with ranked, actionable improvements (no new features). |
| Core behavior: evidence-based analysis and up to 10 prioritized suggestions (★ to ★★★). | `stable` | Use this pattern: core behavior: evidence-based analysis and up to 10 prioritized suggestions (★ to ★★★). |
| Output contract: why/evidence, what to change, where to change, and how to validate. | `stable` | Use this pattern: output contract: why/evidence, what to change, where to change, and how to validate. |
| Why it matters here: acts as reviewer/critic mode for technical debt and reliability. | `stable` | Use this pattern: why it matters here: acts as reviewer/critic mode for technical debt and reliability. |
| Best use: post-sprint optimization and hardening before broad agent rollout. | `uncertain` | Recommended use: post-sprint optimization and hardening before broad agent rollout; validate with your own benchmark or documented source. |

## Slide 27: Skill Spotlight: playwright
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Purpose: automate real browser flows from terminal for testing and debugging. | `stable` | Use this pattern: purpose: automate real browser flows from terminal for testing and debugging. |
| Core behavior: open -> snapshot -> interact by refs -> re-snapshot -> capture artifacts. | `stable` | Use this pattern: core behavior: open -> snapshot -> interact by refs -> re-snapshot -> capture artifacts. |
| Operational guardrail: CLI-first automation with reproducible interaction loops. | `stable` | Use this pattern: operational guardrail: CLI-first automation with reproducible interaction loops. |
| Why it matters here: closes the test loop for UI paths that coding agents modify. | `stable` | Use this pattern: why it matters here: closes the test loop for UI paths that coding agents modify. |
| Best use: regression checks, bug repros, and evidence capture in agent pipelines. | `uncertain` | Recommended use: regression checks, bug repros, and evidence capture in agent pipelines; validate with your own benchmark or documented source. |

## Slide 28: Skill Spotlight: literature-review
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Purpose: systematic literature review across multiple academic databases. | `stable` | Use this pattern: purpose: systematic literature review across multiple academic databases. |
| Core behavior: scoped search strategy, dedup/screening, thematic synthesis, verified citations. | `stable` | Use this pattern: core behavior: scoped search strategy, dedup/screening, thematic synthesis, verified citations. |
| Deliverables: publication-grade markdown/PDF outputs with reproducible search traces. | `stable` | Use this pattern: deliverables: publication-grade markdown/PDF outputs with reproducible search traces. |
| Why it matters here: enables agent-assisted research discovery for issue ideation. | `stable` | Use this pattern: why it matters here: enables agent-assisted research discovery for issue ideation. |
| Best use: state-of-the-art surveys before launching new experiment or implementation tracks. | `uncertain` | Recommended use: state-of-the-art surveys before launching new experiment or implementation tracks; validate with your own benchmark or documented source. |

## Slide 29: Skill Spotlight: scientific-report-editor
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Purpose: draft and quality-gate scientific/technical reports in publication-grade style. | `stable` | Use this pattern: purpose: draft and quality-gate scientific/technical reports in publication-grade style. |
| Core behavior: multi-pass workflow (draft, micro-reviews, controlled rewrite, final review). | `stable` | Use this pattern: core behavior: multi-pass workflow (draft, micro-reviews, controlled rewrite, final review). |
| Quality controls: math-aware formatting, evidence-linked claims, layout validation. | `stable` | Use this pattern: quality controls: math-aware formatting, evidence-linked claims, layout validation. |
| Why it matters here: turns agent outputs into coherent, defensible research communication. | `stable` | Use this pattern: why it matters here: turns agent outputs into coherent, defensible research communication. |
| Best use: transform experiment logs and notes into clean reports and summaries. | `uncertain` | Recommended use: transform experiment logs and notes into clean reports and summaries; validate with your own benchmark or documented source. |

## Slide 30: Skill Spotlight: pr-merger
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Purpose: review, fix, validate, and merge PRs end-to-end with tight scope control. | `stable` | Use this pattern: purpose: review, fix, validate, and merge PRs end-to-end with tight scope control. |
| Core behavior: inspect PR signals, patch minimally, run tests, comment rationale, merge/close. | `stable` | Use this pattern: core behavior: inspect PR signals, patch minimally, run tests, comment rationale, merge/close. |
| Workflow discipline: keep main synced, verify fixes, and clean branch state after merge. | `stable` | Use this pattern: workflow discipline: keep main synced, verify fixes, and clean branch state after merge. |
| Why it matters here: final integration step for work produced by multiple agents. | `stable` | Use this pattern: why it matters here: final integration step for work produced by multiple agents. |
| Best use: converging parallel agent branches into safe, merge-ready outcomes. | `uncertain` | Recommended use: converging parallel agent branches into safe, merge-ready outcomes; validate with your own benchmark or documented source. |

## Slide 31: AGENTS.md as Behavioral Control Plane
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Encodes persistent repo rules: build/test/style/review expectations | `stable` | Use this pattern: encodes persistent repo rules: build/test/style/review expectations. |
| Supports layered precedence: global -> repo -> subdirectory | `stable` | Use this pattern: supports layered precedence: global -> repo -> subdirectory. |
| Turn repeated reviewer feedback into durable instructions | `stable` | Use this pattern: turn repeated reviewer feedback into durable instructions. |
| Pair with linters and pre-commit hooks for enforcement | `stable` | Use this pattern: pair with linters and pre-commit hooks for enforcement. |
| Treat AGENTS.md as living policy, not static docs | `stable` | Use this pattern: treat AGENTS.md as living policy, not static docs. |

## Slide 32: MCP Basics: Why It Matters
| Claim | Flag | Safer alternative wording |
|---|---|---|
| MCP standardizes model access to tools and context | `stable` | Use this pattern: mCP standardizes model access to tools and context. |
| Core primitives: tools, resources, prompts | `stable` | Use this pattern: core primitives: tools, resources, prompts. |
| Transports: local STDIO and remote HTTP | `stable` | Use this pattern: transports: local STDIO and remote HTTP. |
| Decouples orchestration logic from vendor-specific integrations | `stable` | Use this pattern: decouples orchestration logic from vendor-specific integrations. |
| Enables reusable agent workflows across different hosts | `stable` | Use this pattern: enables reusable agent workflows across different hosts. |

## Slide 33: MCP in Practice: Trust and Safety
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Connect only to trusted and verified MCP servers | `stable` | Use this pattern: connect only to trusted and verified MCP servers. |
| Minimize tool scopes; separate read-only and mutating actions | `stable` | Use this pattern: minimize tool scopes; separate read-only and mutating actions. |
| Require explicit approvals for high-impact tool calls | `stable` | Use this pattern: require explicit approvals for high-impact tool calls. |
| Apply OAuth/token hygiene and audience validation | `stable` | Use this pattern: apply OAuth/token hygiene and audience validation. |
| Log every tool call for auditability and incident response | `stable` | Use this pattern: log every tool call for auditability and incident response. |

## Slide 34: Live Walkthrough: Blank Repo to PoC
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Task: research pipeline from raw data to baseline model | `stable` | Use this pattern: task: research pipeline from raw data to baseline model. |
| Planner writes milestones and acceptance criteria | `stable` | Use this pattern: planner writes milestones and acceptance criteria. |
| Implementers split ingestion, modeling, evaluation, docs | `stable` | Use this pattern: implementers split ingestion, modeling, evaluation, docs. |
| Reviewer runs risk checklist and regression pass | `stable` | Use this pattern: reviewer runs risk checklist and regression pass. |
| Output: tested PoC branch with metrics and documentation | `stable` | Use this pattern: output: tested PoC branch with metrics and documentation. |

## Slide 35: Cesar's Real Workflow (Control Loop)
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Codex CLI is the control plane: parent/subagent orchestration at explicit depth levels. | `stable` | Codex CLI can be the control plane: parent/subagent orchestration at explicit depth levels. |
| Default operating mode is `--yolo` to maximize autonomy, speed, and exploration breadth. | `uncertain` | Default operating mode can be `--yolo` to maximize autonomy, speed, and exploration breadth; validate with your own benchmark or documented source. |
| Codex git skills convert lateral ideas and research asks directly into GitHub issues. | `stable` | Use this pattern: codex git skills convert lateral ideas and research asks directly into GitHub issues. |
| Dispatch in GitHub: tag for Jules or assign to Copilot, often with parallel approaches. | `stable` | Use this pattern: dispatch in GitHub: tag for Jules or assign to Copilot, often with parallel approaches. |
| Gemini CLI critiques outputs and files difficulty-tagged bugs; Codex /review is the final gate. | `uncertain` | Gemini CLI critiques outputs and files difficulty-tagged bugs; Codex /review can be the final gate; validate with your own benchmark or documented source. |

## Slide 36: Debug Loop with Agents
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Reproduce: isolate failing test and create minimal repro | `stable` | Use this pattern: reproduce: isolate failing test and create minimal repro. |
| Diagnose: trace logs, data flow, and dependency graph | `stable` | Use this pattern: diagnose: trace logs, data flow, and dependency graph. |
| Patch: propose fix with backward compatibility checks | `stable` | Use this pattern: patch: propose fix with backward compatibility checks. |
| Verify: rerun targeted and full suite tests | `stable` | Use this pattern: verify: rerun targeted and full suite tests. |
| Document: root cause, fix rationale, and prevention steps | `stable` | Use this pattern: document: root cause, fix rationale, and prevention steps. |

## Slide 37: Testing Workflows with Agents
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Generate edge-case tests and mutation-style checks | `stable` | Use this pattern: generate edge-case tests and mutation-style checks. |
| Triage flaky tests with repeated run variance reports | `stable` | Use this pattern: triage flaky tests with repeated run variance reports. |
| Use CI autofix loops for lint/build breakages | `stable` | Use this pattern: use CI autofix loops for lint/build breakages. |
| Run adversarial review prompts for correctness/security | `stable` | Use this pattern: run adversarial review prompts for correctness/security. |
| Track regression rate per agent and task class | `stable` | Use this pattern: track regression rate per agent and task class. |

## Slide 38: Research and Writing Workflows
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Parallel literature triage and synthesis by topic | `stable` | Use this pattern: parallel literature triage and synthesis by topic. |
| Experiment design support for ablations and controls | `stable` | Use this pattern: experiment design support for ablations and controls. |
| Auto-build reproducibility artifacts (env, seeds, scripts) | `stable` | Use this pattern: auto-build reproducibility artifacts (env, seeds, scripts). |
| Writing loop: draft -> critique -> revise -> citation audit | `stable` | Use this pattern: writing loop: draft -> critique -> revise -> citation audit. |
| Prism (OpenAI, Jan 27 2026): AI-native LaTeX scientific workspace | `needs-date` | As of Feb 26, 2026, prism (OpenAI, Jan 27 2026): AI-native LaTeX scientific workspace; confirm current docs/pricing/status before publication. |

## Slide 39: Experimental Robotics: Real World as Tools
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Any system connected to a computer can be wrapped as an agent tool interface. | `stable` | Use this pattern: any system connected to a computer can be wrapped as an agent tool interface. |
| With GPT-5.3-Codex orchestration, cameras/sensors can feed real-world context into workflows. | `stable` | Use this pattern: with GPT-5.3-Codex orchestration, cameras/sensors can feed real-world context into workflows. |
| Agents can run your own scripts as tools for control, logging, and data quality checks. | `stable` | Use this pattern: agents can run your own scripts as tools for control, logging, and data quality checks. |
| Real-world data collection can be agent-assisted with safety gates and human supervision. | `stable` | Use this pattern: real-world data collection can be agent-assisted with safety gates and human supervision. |
| Pattern: scriptable interface -> MCP/tool wrapper -> agent policy -> monitored execution. | `stable` | Use this pattern: pattern: scriptable interface -> MCP/tool wrapper -> agent policy -> monitored execution. |

## Slide 40: High Risk, High Reward in Robot Agent Systems
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Reward: faster robotics iteration, larger design search, and continuous real-world data loops. | `stable` | Use this pattern: reward: faster robotics iteration, larger design search, and continuous real-world data loops. |
| Operating doctrine: run in `--yolo` mode by default for maximum autonomous action space. | `stable` | Use this pattern: operating doctrine: run in `--yolo` mode by default for maximum autonomous action space. |
| Risk: unsafe actuation, sensor misreads, and over-trusting autonomous decisions. | `stable` | Use this pattern: risk: unsafe actuation, sensor misreads, and over-trusting autonomous decisions. |
| Counterbalance controls: kill-switches, hard interrupts, telemetry, and post-run forensics. | `stable` | Use this pattern: counterbalance controls: kill-switches, hard interrupts, telemetry, and post-run forensics. |
| Core metrics: incident/near-miss rate, rollback frequency, and data quality drift. | `stable` | Use this pattern: core metrics: incident/near-miss rate, rollback frequency, and data quality drift. |

## Slide 41: Ralph Wiggum Technique (Actual Definition)
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Core loop: run the same prompt repeatedly (`while :; do cat PROMPT.md \| agent; done`) until completion signal. | `uncertain` | Core loop: run the same prompt repeatedly (`while :; do cat PROMPT.md \| agent; done`) until completion signal; validate with your own benchmark or documented source. |
| State is externalized to files + git, not chat history; each iteration can start with a fresh context window. | `stable` | State can be externalized to files + git, not chat history; each iteration can start with a fresh context window. |
| Operational rule: one concrete item per loop to reduce context pollution and drift. | `stable` | Use this pattern: operational rule: one concrete item per loop to reduce context pollution and drift. |
| Add backpressure gates (tests, type checks, linters, scanners) so bad code is automatically rejected. | `stable` | Add backpressure gates (tests, type checks, linters, scanners) so bad code can be automatically rejected. |
| Tune iteratively with explicit guardrail instructions (“signs”) when failure patterns appear. | `stable` | Use this pattern: tune iteratively with explicit guardrail instructions (“signs”) when failure patterns appear. |

## Slide 42: Adoption Plan and Closing
| Claim | Flag | Safer alternative wording |
|---|---|---|
| Week 1: AGENTS.md baseline, skill templates, MCP policy | `needs-date` | As of Feb 26, 2026, week 1: AGENTS.md baseline, skill templates, MCP policy; confirm current docs/pricing/status before publication. |
| Week 2: pilot one workflow (bugfix or experiment setup) | `needs-date` | As of Feb 26, 2026, week 2: pilot one workflow (bugfix or experiment setup); confirm current docs/pricing/status before publication. |
| Weeks 3-4: reviewer agent, eval metrics, CI integration | `stable` | Use this pattern: weeks 3-4: reviewer agent, eval metrics, CI integration. |
| Success = faster cycle time, fewer escapes, better docs | `stable` | Use this pattern: success = faster cycle time, fewer escapes, better docs. |
| Q&A now \| Lunch at 12:00 \| Tool status validated on Feb 26, 2026 | `needs-date` | As of Feb 26, 2026, q&A now \| Lunch at 12:00 \| Tool status validated on Feb 26, 2026; confirm current docs/pricing/status before publication. |
