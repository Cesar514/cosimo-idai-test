# Strict Factual Risk Audit — `agents.pptx`

Method: extracted all slide text from the PPTX text layer, then audited each non-title statement.

Flag legend:
- `stable`: low volatility process/definition claim.
- `needs-date`: version-, release-, pricing-, schedule-, or status-sensitive claim.
- `uncertain`: subjective, causal, comparative, or not independently verifiable as written.

Note: this audit only covers text embedded in slide objects; text inside images/charts may need separate OCR review.

Re-check status (Feb 26, 2026):
- Current `agents.pptx` has `41` slides (not 42).
- This pass removes stale claims that no longer appear in the deck text layer.

## Top High-Risk Claims Needing Edits (Priority)
| Priority | Slide | Current claim in deck | Why this is high-risk | Edit direction |
|---|---|---|---|---|
| 1 | 15 | OpenAI/GitHub/Google plan prices listed as exact monthly values. | Prices and promotions are region-specific and can change without notice. | Keep exact prices only with source + verification date, and add "US snapshot; verify live checkout." |
| 2 | 14 | "Planning mode" parity between Codex and Gemini is implied. | Public docs diverge: Gemini has explicit Plan Mode; Codex docs describe approval modes (`Auto`, `Read-only`, `Full Access`) instead. | Split claims by tool, and avoid implying a shared command surface. |
| 3 | 13 | OpenAI positions GPT-5.2 Pro as highest-capability GPT-5.2 tier (Responses API only). | Mostly correct but currently un-cited in deck text; "highest" is easy to challenge if not sourced. | Keep claim with dated citation to the model page ("Reasoning: Highest" + "Responses API only"). |
| 4 | 9 | Current constraints: preview status and restricted execution model. | "Preview status" appears stale in current docs; restrictions are better framed as plan/policy/environment constraints. | Replace "preview" with concrete constraints (plan eligibility, repo policy, ephemeral environment). |
| 5 | 19 | Built-in roles are fixed as `default`/`worker`/`explorer`/`monitor`. | Host implementations differ (`monitor` in public Codex docs vs `awaiter` in this workspace tool schema). | Use a host-specific caveat and avoid presenting role labels as universal. |
| 6 | 18 | `agents.max_depth` default 1 and `agents.max_threads` behavior claims. | Default values are documented but version-sensitive. | Keep default value with version/date qualifier and source link. |
| 7 | 16 | `gpt-oss-20b` / `gpt-oss-120b` with "single H100 class" assertion. | The hardware statement comes from cookbook guidance, not a hard requirement. | Keep the models, but label hardware notes as guidance. |
| 8 | 39 | GPT-5.3-Codex name and sensor-fed orchestration are coupled in one claim. | Model naming is currently verifiable; sensor integration is implementation-dependent and safety-sensitive. | Keep model name with citation; move sensor feed language to "when exposed as tools/MCP with safety gates." |
| 9 | 35 | Default operating mode is `--yolo`; dispatch pattern across Codex/Jules/Copilot. | Public Codex docs state default approval mode is `Auto`, not full-access mode. | Replace "default yolo" with "default Auto; escalate only when required." |
| 10 | 40 | Operating doctrine: run in `--yolo` mode by default for maximum autonomy. | High-risk guidance for robotics and inconsistent with documented safer defaults. | Invert doctrine: default constrained mode, use full autonomy only in sandboxed low-consequence runs. |

### Verification sources (checked Feb 26, 2026)
- OpenAI Codex CLI/features/multi-agent/pricing/models/config pages: `developers.openai.com/codex/*`.
- OpenAI GPT-5.2 Pro model page: `developers.openai.com/api/docs/models/gpt-5.2-pro`.
- GitHub Copilot plans and coding-agent docs: `docs.github.com/en/copilot/...`.
- Google Gemini CLI upstream docs: `github.com/google-gemini/gemini-cli` (`README.md`, `docs/cli/plan-mode.md`, `docs/tools/planning.md`).
- Google AI plan pricing + Jules limits: `blog.google`, `one.google.com`, `jules.google`.

## Slide 1: Multi-agentic Workflows
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Orchestrating Coding Agents with CLI Tools, skills.md, and MCPs | `stable` | Orchestrating Coding Agents with CLI Tools, skills.md, and MCPs. |
| 2 | Cesar Contreras \| Friday 27 February 2026 \| Elm House 214 + Teams | `needs-date` | As of Feb 26, 2026: Cesar Contreras \| Friday 27 February 2026 \| Elm House 214 + Teams. Reconfirm against current official docs, release notes, and pricing pages. |
| 3 | Lunch at 12:00 | `needs-date` | As of Feb 26, 2026: Lunch at 12:00. Reconfirm against current official docs, release notes, and pricing pages. |

## Slide 2: Event Details and Scope
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Date: Friday 27 February 2026 \| Time: 11:00 (lunch at 12:00) | `needs-date` | As of Feb 26, 2026: Date: Friday 27 February 2026 \| Time: 11:00 (lunch at 12:00). Reconfirm against current official docs, release notes, and pricing pages. |
| 2 | Location: Elm House 214 + Teams | `needs-date` | As of Feb 26, 2026: Location: Elm House 214 + Teams. Reconfirm against current official docs, release notes, and pricing pages. |
| 3 | Lead: Cesar Contreras | `needs-date` | As of Feb 26, 2026: Lead: Cesar Contreras. Reconfirm against current official docs, release notes, and pricing pages. |
| 4 | Goal: practical multi-agent workflows for research code | `stable` | Goal: practical multi-agent workflows for research code. |
| 5 | Outcome: repeatable path from idea to tested proof-of-concept | `stable` | Outcome: repeatable path from idea to tested proof-of-concept. |

## Slide 3: Agenda (60 Minutes)
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | 11:00-11:10: Why agents now + key definitions | `needs-date` | As of Feb 26, 2026: 11:00-11:10: Why agents now + key definitions. Reconfirm against current official docs, release notes, and pricing pages. |
| 2 | 11:10-11:25: Tooling landscape (Codex, Copilot, Jules, Gemini, MCP) | `needs-date` | As of Feb 26, 2026: 11:10-11:25: Tooling landscape (Codex, Copilot, Jules, Gemini, MCP). Reconfirm against current official docs, release notes, and pricing pages. |
| 3 | 11:25-11:45: Live repo walkthrough with role-split agents | `needs-date` | As of Feb 26, 2026: 11:25-11:45: Live repo walkthrough with role-split agents. Reconfirm against current official docs, release notes, and pricing pages. |
| 4 | 11:45-11:55: Debug, testing, research, and writing workflows | `needs-date` | As of Feb 26, 2026: 11:45-11:55: Debug, testing, research, and writing workflows. Reconfirm against current official docs, release notes, and pricing pages. |

## Slide 4: Why 2026 Is Different
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Coding agents moved from chat help to autonomous PR-style execution | `uncertain` | Coding agents have increasingly moved from chat help to autonomous PR-style execution (validate with benchmarks, logs, or citations before stating as fact). |
| 2 | MCP-style protocols made tool integrations composable | `uncertain` | MCP-style protocols made tool integrations composable (validate with benchmarks, logs, or citations before stating as fact). |
| 3 | Larger context + stronger reasoning enable longer task chains | `uncertain` | Larger context + stronger reasoning enable longer task chains (validate with benchmarks, logs, or citations before stating as fact). |
| 4 | Teams can parallelize exploration, implementation, and review | `uncertain` | Teams can parallelize exploration, implementation, and review (validate with benchmarks, logs, or citations before stating as fact). |
| 5 | Bottleneck shifted from typing speed to orchestration quality | `uncertain` | Bottleneck is shifting from typing speed to orchestration quality (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 5: What Multi-agent Workflow Means
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Multiple specialized agents coordinate on one objective | `stable` | Multiple specialized agents coordinate on one objective. |
| 2 | Planner decomposes work into parallelizable tasks | `stable` | Planner decomposes work into parallelizable tasks. |
| 3 | Implementers execute code, tests, and integrations | `stable` | Implementers execute code, tests, and integrations. |
| 4 | Reviewer/critic validates correctness and regression risk | `stable` | Reviewer/critic validates correctness and regression risk. |
| 5 | Human sets priorities, trust boundaries, and final approvals | `stable` | Human sets priorities, trust boundaries, and final approvals. |

## Slide 6: Reference Architecture
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Inputs: issue statement, repo state, tests, constraints | `stable` | Inputs: issue statement, repo state, tests, constraints. |
| 2 | Planner agent: task graph + acceptance criteria | `stable` | Planner agent: task graph + acceptance criteria. |
| 3 | Implementer agents: code changes + local validation | `stable` | Implementer agents: code changes + local validation. |
| 4 | Reviewer agent: risk scan + quality bar checks | `stable` | Reviewer agent: risk scan + quality bar checks. |
| 5 | Operator (human): checkpoint approvals + merge decisions | `stable` | Operator (human): checkpoint approvals + merge decisions. |

## Slide 7: Tool Landscape (As of Feb 26, 2026)
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | OpenAI Codex CLI: local coding agent with multi-agent + MCP | `needs-date` | As of Feb 26, 2026: OpenAI Codex CLI: local coding agent with multi-agent + MCP. Reconfirm against current official docs, release notes, and pricing pages. |
| 2 | GitHub Copilot coding agent: issue-to-PR automation in GitHub | `needs-date` | As of Feb 26, 2026: GitHub Copilot coding agent: issue-to-PR automation in GitHub. Reconfirm against current official docs, release notes, and pricing pages. |
| 3 | Google Jules/Jules API: asynchronous coding agent + API automation | `needs-date` | As of Feb 26, 2026: Google Jules/Jules API: asynchronous coding agent + API automation. Reconfirm against current official docs, release notes, and pricing pages. |
| 4 | Gemini CLI: open-source terminal agent with MCP extensibility | `needs-date` | As of Feb 26, 2026: Gemini CLI: open-source terminal agent with MCP extensibility. Reconfirm against current official docs, release notes, and pricing pages. |
| 5 | Shared denominator: prompts + tools + policy + eval loops | `uncertain` | Shared denominator: prompts + tools + policy + eval loops (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 8: Codex CLI: High-Leverage Features
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Local repo read/edit/run with explicit approval modes | `needs-date` | As of Feb 26, 2026: Local repo read/edit/run with explicit approval modes. Reconfirm against current official docs, release notes, and pricing pages. |
| 2 | Non-interactive automation via codex exec workflows | `needs-date` | As of Feb 26, 2026: Non-interactive automation via codex exec workflows. Reconfirm against current official docs, release notes, and pricing pages. |
| 3 | Experimental multi-agent orchestration with specialized roles | `needs-date` | As of Feb 26, 2026: Experimental multi-agent orchestration with specialized roles. Reconfirm against current official docs, release notes, and pricing pages. |
| 4 | First-party web search (cached or live modes) | `needs-date` | As of Feb 26, 2026: First-party web search (cached or live modes). Reconfirm against current official docs, release notes, and pricing pages. |
| 5 | Built-in MCP support for external tools and context providers | `needs-date` | As of Feb 26, 2026: Built-in MCP support for external tools and context providers. Reconfirm against current official docs, release notes, and pricing pages. |

## Slide 9: GitHub Copilot Coding Agent
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Strong fit for issue-driven asynchronous implementation | `uncertain` | Strong fit for issue-driven asynchronous implementation (validate with benchmarks, logs, or citations before stating as fact). |
| 2 | Operates directly in GitHub pull request workflows | `needs-date` | As of Feb 26, 2026: Operates directly in GitHub pull request workflows. Reconfirm against current official docs, release notes, and pricing pages. |
| 3 | Useful for repetitive backlog and maintenance tasks | `uncertain` | Useful for repetitive backlog and maintenance tasks (validate with benchmarks, logs, or citations before stating as fact). |
| 4 | Current constraints: preview status and restricted execution model | `needs-date` | As of Feb 26, 2026 (GitHub Docs): Copilot coding agent is available on Pro/Pro+/Business/Enterprise plans; practical constraints are repo policy, plan limits, and execution in an ephemeral GitHub Actions environment, not a blanket "preview status". |
| 5 | Best used as implementer with independent reviewer checks | `uncertain` | Often effective used as implementer with independent reviewer checks (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 10: Google Jules
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Jules targets asynchronous coding tasks on codebases | `needs-date` | As of Feb 26, 2026: Jules targets asynchronous coding tasks on codebases. Reconfirm against current official docs, release notes, and pricing pages. |
| 2 | Good pattern: dispatch tasks, collect artifacts, review diffs | `stable` | Good pattern: dispatch tasks, collect artifacts, review diffs. |
| 3 | Useful for long-running background work | `uncertain` | Useful for long-running background work (validate with benchmarks, logs, or citations before stating as fact). |
| 4 | Needs strict acceptance tests before delegated execution | `stable` | Needs strict acceptance tests before delegated execution. |

## Slide 11: Gemini CLI in Multi-agent Stacks
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Open-source terminal agent for coding and scripting workflows | `needs-date` | As of Feb 26, 2026: Open-source terminal agent for coding and scripting workflows. Reconfirm against current official docs, release notes, and pricing pages. |
| 2 | Useful for rapid implementation and repository exploration | `uncertain` | Useful for rapid implementation and repository exploration (validate with benchmarks, logs, or citations before stating as fact). |
| 3 | Extensible with MCP for custom integrations | `needs-date` | As of Feb 26, 2026: Extensible with MCP for custom integrations. Reconfirm against current official docs, release notes, and pricing pages. |
| 4 | Can be paired with Gemini Code Assist for IDE workflows | `needs-date` | As of Feb 26, 2026: Can be paired with Gemini Code Assist for IDE workflows. Reconfirm against current official docs, release notes, and pricing pages. |
| 5 | Treat outputs as proposals and enforce test/eval gates | `stable` | Treat outputs as proposals and enforce test/eval gates. |

## Slide 12: Codex vs Gemini CLI vs Claude: Choice Matters
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Codex: strongest when you want strict rule-following (AGENTS.md, skills, explicit constraints). | `uncertain` | Treat this as an internal observation, not a vendor-level fact; back it with internal evals (instruction adherence, scope drift, defect rate) before stating it publicly. |
| 2 | Gemini CLI: often takes more initiative and may deviate if your guardrails are loose. | `uncertain` | Keep as anecdotal behavior unless your own benchmark data is shown; do not present as an objective product guarantee. |
| 3 | Claude: tends to over-improve and expand scope beyond the exact ask. | `uncertain` | Keep as anecdotal behavior unless your own benchmark data is shown; do not present as an objective product guarantee. |
| 4 | Operational takeaway: same prompt can produce very different behaviors across agents. | `stable` | Keep this claim and pair it with explicit evaluation criteria (scope adherence, pass rate, time-to-fix) so "different behaviors" is measured, not implied. |
| 5 | Your choice matters: pick the agent by control needs, risk tolerance, and review bandwidth. | `stable` | Your choice matters: pick the agent by control needs, risk tolerance, and review bandwidth. |

## Slide 13: Using GPT-5.2 Pro (Why It Helps)
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Best for hardest tasks: deep reasoning, multi-step code edits, and agentic tool-use chains. | `uncertain` | Often effective for hardest tasks: deep reasoning, multi-step code edits, and agentic tool-use chains (validate with benchmarks, logs, or citations before stating as fact). |
| 2 | OpenAI positions GPT-5.2 Pro as the highest-capability GPT-5.2 tier (Responses API only). | `needs-date` | As of Feb 26, 2026 (OpenAI model page): GPT-5.2 Pro is labeled "Reasoning: Highest" and "available in the Responses API only." Keep both points with the date and source URL in notes/footer. |
| 3 | High leverage in your workflow: architecture decisions, risky refactors, and root-cause analysis. | `uncertain` | High leverage in your workflow: architecture decisions, risky refactors, and root-cause analysis (validate with benchmarks, logs, or citations before stating as fact). |
| 4 | Pattern: use GPT-5.2 Pro for planning/critical reviews; use faster models for implementation loops. | `stable` | Pattern: use GPT-5.2 Pro for planning/critical reviews; use faster models for implementation loops. |
| 5 | When uncertainty and downside risk are high, paying for stronger reasoning is usually net-positive. | `uncertain` | When uncertainty and downside risk are high, paying for stronger reasoning is often cost-effective (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 14: Planning Mode: Codex and Gemini
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Codex: collaboration modes include plan mode (useful for design-first, read-before-write workflows). | `needs-date` | As of Feb 26, 2026 (public Codex CLI docs): documented approval modes are `Auto` (default), `Read-only`, and `Full Access`; no public Codex `/plan` mode is documented. |
| 2 | Gemini CLI: `/plan` switches to read-only planning mode (feature marked experimental). | `needs-date` | As of Feb 26, 2026 (gemini-cli docs): `/plan` enters Plan Mode, a read-only environment, and the feature is marked experimental/preview. |
| 3 | Gemini also supports `--approval-mode=plan` and explicit plan artifact generation before coding. | `needs-date` | As of Feb 26, 2026 (gemini-cli docs): `--approval-mode=plan` and `defaultApprovalMode: \"plan\"` are supported entry points for Plan Mode. |
| 4 | Common benefit: better approach selection, fewer blind edits, cleaner handoff to implementer agents. | `uncertain` | Common benefit: better approach selection, fewer blind edits, cleaner handoff to implementer agents (validate with benchmarks, logs, or citations before stating as fact). |
| 5 | Note: in Gemini docs, enter-plan tool is unavailable while running in YOLO mode. | `needs-date` | As of Feb 26, 2026 (gemini-cli `planning.md`): `enter_plan_mode` is not available while Gemini CLI is in YOLO mode. |

## Slide 15: Subscription Prices Snapshot (US, Feb 26, 2026)
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | OpenAI ChatGPT: Plus $20/mo, Pro $200/mo, Business $25/user/mo (annual) (Enterprise: contact sales). | `needs-date` | As of Feb 26, 2026 (OpenAI Codex pricing page): Plus $20/mo, Pro $200/mo, Business $30/user/mo; Enterprise/Edu via sales/workspace terms. Mark this as a US snapshot and note that tax/region/promo can change checkout totals. |
| 2 | Codex CLI: no separate subscription; included with ChatGPT Plus/Pro/Business/Edu/Enterprise. | `needs-date` | As of Feb 26, 2026 (OpenAI Codex docs): Codex is included with Plus/Pro/Business/Edu/Enterprise; docs also note a limited-time Free/Go trial path. |
| 3 | GitHub Copilot: Pro $10/mo, Pro+ $39/mo, Business $19/user/mo, Enterprise $39/user/mo. | `needs-date` | As of Feb 26, 2026 (GitHub Docs plans page): Pro $10/mo ($100/yr), Pro+ $39/mo ($390/yr), Business $19 per granted seat/mo, Enterprise $39 per granted seat/mo. |
| 4 | Google AI plans: AI Pro $19.99/mo; AI Ultra launched at $249.99/mo in the US (pricing/promos can change). | `needs-date` | As of Feb 26, 2026: official Google launch posts cite AI Pro at $19.99/mo and AI Ultra at $249.99/mo in the US; current Google One pages use country/promo-specific pricing displays, so verify live checkout before presenting exact numbers. |
| 5 | Jules: no separate public subscription on its own page; usage limits are tied to AI Pro/Ultra tiers. | `needs-date` | As of Feb 26, 2026 (jules.google docs): Jules has base limits plus `Jules in Pro` and `Jules in Ultra` tiers tied to Google AI plans; limits and concurrency are explicitly documented and subject to change. |

## Slide 16: Local Models: When and Why to Use Them
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Codex supports local OSS providers (`--oss`) via Ollama or LM Studio in config. | `needs-date` | As of Feb 26, 2026 (Codex advanced config docs): `--oss` is supported with local providers and `oss_provider` defaults (for example `ollama` or `lmstudio`). |
| 2 | OpenAI open-weight options: `gpt-oss-20b` (local/specialized) and `gpt-oss-120b` (single H100 class). | `needs-date` | As of Feb 26, 2026 (OpenAI cookbook docs): `openai/gpt-oss-20b` and `openai/gpt-oss-120b` are documented; "single H100" appears as hardware guidance for 120b, not a hard requirement. |
| 3 | Cost model shift: lower subscription dependence, higher compute/ops responsibility. | `uncertain` | Cost model shift: lower subscription dependence, higher compute/ops responsibility (validate with benchmarks, logs, or citations before stating as fact). |
| 4 | Best fit: privacy-sensitive data, air-gapped workflows, custom fine-tunes, deterministic local tooling. | `uncertain` | Often effective fit: privacy-sensitive data, air-gapped workflows, custom fine-tunes, deterministic local tooling (validate with benchmarks, logs, or citations before stating as fact). |
| 5 | Practical strategy: hybrid stack (local models for bulk loops, frontier models for critical reasoning). | `stable` | Practical strategy: hybrid stack (local models for bulk loops, frontier models for critical reasoning). |

## Slide 17: Role Split: Planner vs Implementer vs Reviewer
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Planner: defines task DAG, dependencies, and rollback logic | `stable` | Planner: defines task DAG, dependencies, and rollback logic. |
| 2 | Implementer: ships smallest safe patches per task node | `stable` | Implementer: ships smallest safe patches per task node. |
| 3 | Reviewer: adversarial check for bugs, security, regressions | `stable` | Reviewer: adversarial check for bugs, security, regressions. |
| 4 | Release agent (optional): changelog, versioning, deployment notes | `stable` | Release agent (optional): changelog, versioning, deployment notes. |
| 5 | Human remains accountable for risk decisions and shipping | `stable` | Human remains accountable for risk decisions and shipping. |

## Slide 18: Codex Spawn Tree: Agents, Subagents, Max Depth
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Root session starts at depth 0; parent can spawn child agents for parallel tasks. | `needs-date` | As of Feb 26, 2026 (Codex multi-agent docs): root depth is 0 and Codex can spawn child agents for parallel workflows. |
| 2 | Children can spawn subagents recursively only when depth budget allows. | `needs-date` | As of Feb 26, 2026 (Codex multi-agent docs): child agents may spawn deeper agents only within configured depth limits. |
| 3 | `agents.max_depth` limits nesting: default 1 = root -> child only (no grandchild). | `needs-date` | As of Feb 26, 2026 (Codex multi-agent docs): `agents.max_depth` defaults to `1`, allowing a direct child but preventing deeper nesting. |
| 4 | `agents.max_threads` limits concurrent open agent threads to avoid overload. | `needs-date` | As of Feb 26, 2026 (Codex multi-agent docs): `agents.max_threads` is the concurrency limit for open agent threads. |
| 5 | Parent orchestrates lifecycle with spawn/send_input/wait/resume/close and merges outputs. | `needs-date` | As of Feb 26, 2026: parent orchestration across spawn/routing/wait/close is documented; exact tool names can vary by host/runtime implementation. |

## Slide 19: Codex Agent Types and Why This Is Marvelous
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Built-in roles: `default`, `worker`, `explorer`, and `monitor` (plus custom roles). | `needs-date` | As of Feb 26, 2026 (public Codex docs): built-in roles are `default`, `worker`, `explorer`, and `monitor`; caveat: this workspace API schema uses `awaiter` for long-wait work. |
| 2 | `worker` focuses on execution/fixes; `explorer` on read-heavy code discovery; `monitor` on long waits/polling. | `needs-date` | As of Feb 26, 2026: role intent is execution (`worker`), read-heavy discovery (`explorer`), and long waits/polling (`monitor` in docs, `awaiter` in this host). |
| 3 | Each role can have its own model, reasoning effort, sandbox mode, and instructions. | `needs-date` | As of Feb 26, 2026 (Codex multi-agent docs): role-level overrides for model, reasoning effort, sandbox mode, and developer instructions are documented. |
| 4 | Marvelous effect: role specialization + parallelism reduces context rot and increases throughput. | `uncertain` | Marvelous effect: role specialization + parallelism reduces context rot and increases throughput (validate with benchmarks, logs, or citations before stating as fact). |
| 5 | You keep control with depth/thread limits and permissions while still moving much faster. | `uncertain` | You keep control with depth/thread limits and permissions while still moving much faster (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 20: Hardcore Orchestration Pattern
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | 1) Set measurable goal and explicit stop conditions | `stable` | 1) Set measurable goal and explicit stop conditions. |
| 2 | 2) Spawn parallel implementers on isolated branches | `stable` | 2) Spawn parallel implementers on isolated branches. |
| 3 | 3) Run automated checks after every patch | `stable` | 3) Run automated checks after every patch. |
| 4 | 4) Reviewer compares alternatives with evidence | `stable` | 4) Reviewer compares alternatives with evidence. |
| 5 | 5) Approve based on test artifacts, not model confidence | `stable` | 5) Approve based on test artifacts, not model confidence. |

## Slide 21: skills.md / SKILL.md Patterns
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Package repeatable workflows as skills: instructions + scripts + assets | `stable` | Package repeatable workflows as skills: instructions + scripts + assets. |
| 2 | Keep skills narrow: setup, test triage, docs, release notes | `stable` | Keep skills narrow: setup, test triage, docs, release notes. |
| 3 | Embed deterministic scripts in scripts/ for repeatability | `stable` | Embed deterministic scripts in scripts/ for repeatability. |
| 4 | Use clear descriptions for reliable triggering | `stable` | Use clear descriptions for reliable triggering. |
| 5 | Version and review skills with normal PR discipline | `stable` | Version and review skills with normal PR discipline. |

## Slide 22: How to Create a Skill (skill-creator Workflow)
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | 1) Define concrete usage examples and identify reusable resources (scripts, references, assets). | `stable` | 1) Define concrete usage examples and identify reusable resources (scripts, references, assets). |
| 2 | 2) Initialize scaffold with `scripts/init_skill.py <skill-name> --path <dir> --resources ...`. | `stable` | 2) Initialize scaffold with `scripts/init_skill.py <skill-name> --path <dir> --resources ...`. |
| 3 | 3) Write `SKILL.md`: frontmatter only `name` + `description`; keep body concise and imperative. | `stable` | 3) Write `SKILL.md`: frontmatter only `name` + `description`; keep body concise and imperative. |
| 4 | 4) Add deterministic scripts, needed references, and optional assets; generate `agents/openai.yaml` metadata. | `needs-date` | As of Feb 26, 2026: 4) Add deterministic scripts, needed references, and optional assets; generate `agents/openai.yaml` metadata. Reconfirm against current official docs, release notes, and pricing pages. |
| 5 | 5) Validate with `scripts/quick_validate.py <skill-folder>`, test scripts, then iterate from real usage feedback. | `stable` | 5) Validate with `scripts/quick_validate.py <skill-folder>`, test scripts, then iterate from real usage feedback. |

## Slide 23: Skill Spotlight: create-plan
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Purpose: generate a concise, actionable plan when planning is explicitly requested. | `stable` | Purpose: generate a concise, actionable plan when planning is explicitly requested. |
| 2 | Core behavior: fast read-only context scan + only blocking follow-up questions. | `stable` | Core behavior: fast read-only context scan + only blocking follow-up questions. |
| 3 | Output contract: #Plan with scope, ordered checklist, and open questions. | `stable` | Output contract: #Plan with scope, ordered checklist, and open questions. |
| 4 | Why it matters here: aligns planner-agent behavior before parallel execution. | `stable` | Why it matters here: aligns planner-agent behavior before parallel execution. |
| 5 | Best use: kickoff for complex coding/research tasks with clear acceptance criteria. | `uncertain` | Often effective use: kickoff for complex coding/research tasks with clear acceptance criteria (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 24: Skill Spotlight: github-agents-deploy
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Purpose: triage open GitHub issues/PRs and deploy Copilot/Jules/Codex review strategically. | `needs-date` | As of Feb 26, 2026: Purpose: triage open GitHub issues/PRs and deploy Copilot/Jules/Codex review strategically. Reconfirm against current official docs, release notes, and pricing pages. |
| 2 | Core behavior: MCP-only GitHub operations, capacity-aware assignment, no duplicate deployment. | `stable` | Core behavior: MCP-only GitHub operations, capacity-aware assignment, no duplicate deployment. |
| 3 | Safety pattern: draft per-issue/per-PR plan first, execute only after user approval. | `stable` | Safety pattern: draft per-issue/per-PR plan first, execute only after user approval. |
| 4 | Why it matters here: operationalizes your issue-to-agent dispatch workflow at scale. | `stable` | Why it matters here: operationalizes your issue-to-agent dispatch workflow at scale. |
| 5 | Best use: weekly triage to keep agent workloads balanced and visible. | `uncertain` | Often effective use: weekly triage to keep agent workloads balanced and visible (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 25: Skill Spotlight: openai-docs
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Purpose: fetch current OpenAI guidance from official docs with citations. | `needs-date` | As of Feb 26, 2026: Purpose: fetch current OpenAI guidance from official docs with citations. Reconfirm against current official docs, release notes, and pricing pages. |
| 2 | Core behavior: search + fetch via OpenAI Docs MCP before any web fallback. | `needs-date` | As of Feb 26, 2026: Core behavior: search + fetch via OpenAI Docs MCP before any web fallback. Reconfirm against current official docs, release notes, and pricing pages. |
| 3 | Output quality: source-grounded API/tooling guidance with reduced speculation risk. | `stable` | Output quality: source-grounded API/tooling guidance with reduced speculation risk. |
| 4 | Why it matters here: keeps agent architecture choices aligned with latest platform reality. | `stable` | Why it matters here: keeps agent architecture choices aligned with latest platform reality. |
| 5 | Best use: model/tool capability checks before implementing new workflow patterns. | `uncertain` | Often effective use: model/tool capability checks before implementing new workflow patterns (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 26: Skill Spotlight: suggest-improve
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Purpose: deep codebase health review with ranked, actionable improvements (no new features). | `stable` | Purpose: deep codebase health review with ranked, actionable improvements (no new features). |
| 2 | Core behavior: evidence-based analysis and up to 10 prioritized suggestions (★ to ★★★). | `stable` | Core behavior: evidence-based analysis and up to 10 prioritized suggestions (★ to ★★★). |
| 3 | Output contract: why/evidence, what to change, where to change, and how to validate. | `stable` | Output contract: why/evidence, what to change, where to change, and how to validate. |
| 4 | Why it matters here: acts as reviewer/critic mode for technical debt and reliability. | `stable` | Why it matters here: acts as reviewer/critic mode for technical debt and reliability. |
| 5 | Best use: post-sprint optimization and hardening before broad agent rollout. | `uncertain` | Often effective use: post-sprint optimization and hardening before broad agent rollout (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 27: Skill Spotlight: playwright
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Purpose: automate real browser flows from terminal for testing and debugging. | `stable` | Purpose: automate real browser flows from terminal for testing and debugging. |
| 2 | Core behavior: open -> snapshot -> interact by refs -> re-snapshot -> capture artifacts. | `stable` | Core behavior: open -> snapshot -> interact by refs -> re-snapshot -> capture artifacts. |
| 3 | Operational guardrail: CLI-first automation with reproducible interaction loops. | `stable` | Operational guardrail: CLI-first automation with reproducible interaction loops. |
| 4 | Why it matters here: closes the test loop for UI paths that coding agents modify. | `stable` | Why it matters here: closes the test loop for UI paths that coding agents modify. |
| 5 | Best use: regression checks, bug repros, and evidence capture in agent pipelines. | `uncertain` | Often effective use: regression checks, bug repros, and evidence capture in agent pipelines (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 28: Skill Spotlight: literature-review
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Purpose: systematic literature review across multiple academic databases. | `stable` | Purpose: systematic literature review across multiple academic databases. |
| 2 | Core behavior: scoped search strategy, dedup/screening, thematic synthesis, verified citations. | `stable` | Core behavior: scoped search strategy, dedup/screening, thematic synthesis, verified citations. |
| 3 | Deliverables: publication-grade markdown/PDF outputs with reproducible search traces. | `stable` | Deliverables: publication-grade markdown/PDF outputs with reproducible search traces. |
| 4 | Why it matters here: enables agent-assisted research discovery for issue ideation. | `stable` | Why it matters here: enables agent-assisted research discovery for issue ideation. |
| 5 | Best use: state-of-the-art surveys before launching new experiment or implementation tracks. | `uncertain` | Often effective use: state-of-the-art surveys before launching new experiment or implementation tracks (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 29: Skill Spotlight: scientific-report-editor
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Purpose: draft and quality-gate scientific/technical reports in publication-grade style. | `stable` | Purpose: draft and quality-gate scientific/technical reports in publication-grade style. |
| 2 | Core behavior: multi-pass workflow (draft, micro-reviews, controlled rewrite, final review). | `stable` | Core behavior: multi-pass workflow (draft, micro-reviews, controlled rewrite, final review). |
| 3 | Quality controls: math-aware formatting, evidence-linked claims, layout validation. | `stable` | Quality controls: math-aware formatting, evidence-linked claims, layout validation. |
| 4 | Why it matters here: turns agent outputs into coherent, defensible research communication. | `stable` | Why it matters here: turns agent outputs into coherent, defensible research communication. |
| 5 | Best use: transform experiment logs and notes into clean reports and summaries. | `uncertain` | Often effective use: transform experiment logs and notes into clean reports and summaries (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 30: Skill Spotlight: pr-merger
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Purpose: review, fix, validate, and merge PRs end-to-end with tight scope control. | `stable` | Purpose: review, fix, validate, and merge PRs end-to-end with tight scope control. |
| 2 | Core behavior: inspect PR signals, patch minimally, run tests, comment rationale, merge/close. | `stable` | Core behavior: inspect PR signals, patch minimally, run tests, comment rationale, merge/close. |
| 3 | Workflow discipline: keep main synced, verify fixes, and clean branch state after merge. | `stable` | Workflow discipline: keep main synced, verify fixes, and clean branch state after merge. |
| 4 | Why it matters here: final integration step for work produced by multiple agents. | `stable` | Why it matters here: final integration step for work produced by multiple agents. |
| 5 | Best use: converging parallel agent branches into safe, merge-ready outcomes. | `uncertain` | Often effective use: converging parallel agent branches into safe, merge-ready outcomes (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 31: AGENTS.md as Behavioral Control Plane
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Encodes persistent repo rules: build/test/style/review expectations | `stable` | Encodes persistent repo rules: build/test/style/review expectations. |
| 2 | Supports layered precedence: global -> repo -> subdirectory | `stable` | Supports layered precedence: global -> repo -> subdirectory. |
| 3 | Turn repeated reviewer feedback into durable instructions | `stable` | Turn repeated reviewer feedback into durable instructions. |
| 4 | Pair with linters and pre-commit hooks for enforcement | `stable` | Pair with linters and pre-commit hooks for enforcement. |
| 5 | Treat AGENTS.md as living policy, not static docs | `stable` | Treat AGENTS.md as living policy, not static docs. |

## Slide 32: MCP Basics: Why It Matters
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | MCP standardizes model access to tools and context | `stable` | MCP standardizes model access to tools and context. |
| 2 | Core primitives: tools, resources, prompts | `stable` | Core primitives: tools, resources, prompts. |
| 3 | Transports: local STDIO and remote HTTP | `stable` | Transports: local STDIO and remote HTTP. |
| 4 | Decouples orchestration logic from vendor-specific integrations | `stable` | Decouples orchestration logic from vendor-specific integrations. |
| 5 | Enables reusable agent workflows across different hosts | `stable` | Enables reusable agent workflows across different hosts. |

## Slide 33: MCP in Practice: Trust and Safety
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Connect only to trusted and verified MCP servers | `stable` | Connect only to trusted and verified MCP servers. |
| 2 | Minimize tool scopes; separate read-only and mutating actions | `stable` | Minimize tool scopes; separate read-only and mutating actions. |
| 3 | Require explicit approvals for high-impact tool calls | `stable` | Require explicit approvals for high-impact tool calls. |
| 4 | Apply OAuth/token hygiene and audience validation | `stable` | Apply OAuth/token hygiene and audience validation. |
| 5 | Log every tool call for auditability and incident response | `stable` | Log every tool call for auditability and incident response. |

## Slide 34: Live Walkthrough: Blank Repo to PoC
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Task: research pipeline from raw data to baseline model | `stable` | Task: research pipeline from raw data to baseline model. |
| 2 | Planner writes milestones and acceptance criteria | `stable` | Planner writes milestones and acceptance criteria. |
| 3 | Implementers split ingestion, modeling, evaluation, docs | `stable` | Implementers split ingestion, modeling, evaluation, docs. |
| 4 | Reviewer runs risk checklist and regression pass | `stable` | Reviewer runs risk checklist and regression pass. |
| 5 | Output: tested PoC branch with metrics and documentation | `uncertain` | Output: tested PoC branch with metrics and documentation (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 35: Cesar's Real Workflow (Control Loop)
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Codex CLI is the control plane: parent/subagent orchestration at explicit depth levels. | `needs-date` | As of Feb 26, 2026: Codex CLI is the control plane: parent/subagent orchestration at explicit depth levels. Reconfirm against current official docs, release notes, and pricing pages. |
| 2 | Default operating mode is `--yolo` to maximize autonomy, speed, and exploration breadth. | `needs-date` | As of Feb 26, 2026 (Codex CLI features docs): default approval mode is `Auto`; treat full-access/YOLO operation as an explicit escalation for sandboxed, low-consequence runs only. |
| 3 | Codex git skills convert lateral ideas and research asks directly into GitHub issues. | `needs-date` | As of Feb 26, 2026: Codex git skills convert lateral ideas and research asks directly into GitHub issues. Reconfirm against current official docs, release notes, and pricing pages. |
| 4 | Dispatch in GitHub: tag for Jules or assign to Copilot, often with parallel approaches. | `needs-date` | As of Feb 26, 2026: Dispatch in GitHub: tag for Jules or assign to Copilot, often with parallel approaches. Reconfirm against current official docs, release notes, and pricing pages. |
| 5 | Gemini CLI critiques outputs and files difficulty-tagged bugs; Codex /review is the final gate. | `uncertain` | Gemini CLI critiques outputs and files difficulty-tagged bugs; Codex /review can serve as a final gate (validate with benchmarks, logs, or citations before stating as fact). |

## Slide 36: Debug Loop with Agents
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Reproduce: isolate failing test and create minimal repro | `stable` | Reproduce: isolate failing test and create minimal repro. |
| 2 | Diagnose: trace logs, data flow, and dependency graph | `stable` | Diagnose: trace logs, data flow, and dependency graph. |
| 3 | Patch: propose fix with backward compatibility checks | `stable` | Patch: propose fix with backward compatibility checks. |
| 4 | Verify: rerun targeted and full suite tests | `stable` | Verify: rerun targeted and full suite tests. |
| 5 | Document: root cause, fix rationale, and prevention steps | `stable` | Document: root cause, fix rationale, and prevention steps. |

## Slide 37: Testing Workflows with Agents
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Generate edge-case tests and mutation-style checks | `stable` | Generate edge-case tests and mutation-style checks. |
| 2 | Triage flaky tests with repeated run variance reports | `stable` | Triage flaky tests with repeated run variance reports. |
| 3 | Use CI autofix loops for lint/build breakages | `stable` | Use CI autofix loops for lint/build breakages. |
| 4 | Run adversarial review prompts for correctness/security | `stable` | Run adversarial review prompts for correctness/security. |
| 5 | Track regression rate per agent and task class | `stable` | Track regression rate per agent and task class. |

## Slide 38: Research and Writing Workflows
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Parallel literature triage and synthesis by topic | `stable` | Parallel literature triage and synthesis by topic. |
| 2 | Experiment design support for ablations and controls | `stable` | Experiment design support for ablations and controls. |
| 3 | Auto-build reproducibility artifacts (env, seeds, scripts) | `stable` | Auto-build reproducibility artifacts (env, seeds, scripts). |
| 4 | Writing loop: draft -> critique -> revise -> citation audit | `stable` | Writing loop: draft -> critique -> revise -> citation audit. |
| 5 | Prism (OpenAI, Jan 27 2026): AI-native LaTeX scientific workspace | `needs-date` | As of Feb 26, 2026: Prism (OpenAI, Jan 27 2026): AI-native LaTeX scientific workspace. Reconfirm against current official docs, release notes, and pricing pages. |

## Slide 39: Experimental Robotics: Real World as Tools
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Any system connected to a computer can be wrapped as an agent tool interface. | `uncertain` | Any system connected to a computer can be wrapped as an agent tool interface (validate with benchmarks, logs, or citations before stating as fact). |
| 2 | With GPT-5.3-Codex orchestration, cameras/sensors can feed real-world context into workflows. | `needs-date` | As of Feb 26, 2026: `gpt-5.3-codex` is a documented Codex model; sensor/camera input claims are only accurate when those data streams are explicitly exposed via tools/MCP and guarded by safety controls. |
| 3 | Agents can run your own scripts as tools for control, logging, and data quality checks. | `stable` | Agents can run your own scripts as tools for control, logging, and data quality checks. |
| 4 | Real-world data collection can be agent-assisted with safety gates and human supervision. | `stable` | Real-world data collection can be agent-assisted with safety gates and human supervision. |
| 5 | Pattern: scriptable interface -> MCP/tool wrapper -> agent policy -> monitored execution. | `stable` | Pattern: scriptable interface -> MCP/tool wrapper -> agent policy -> monitored execution. |

## Slide 40: High Risk, High Reward in Robot Agent Systems
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Reward: faster robotics iteration, larger design search, and continuous real-world data loops. | `stable` | Reward: faster robotics iteration, larger design search, and continuous real-world data loops. |
| 2 | Operating doctrine: run in `--yolo` mode by default for maximum autonomous action space. | `needs-date` | As of Feb 26, 2026: documented default is `Auto` approval mode. Safer doctrine for robotics: start constrained, require explicit escalation gates for any full-autonomy run. |
| 3 | Risk: unsafe actuation, sensor misreads, and over-trusting autonomous decisions. | `stable` | Risk: unsafe actuation, sensor misreads, and over-trusting autonomous decisions. |
| 4 | Counterbalance controls: kill-switches, hard interrupts, telemetry, and post-run forensics. | `stable` | Counterbalance controls: kill-switches, hard interrupts, telemetry, and post-run forensics. |
| 5 | Core metrics: incident/near-miss rate, rollback frequency, and data quality drift. | `stable` | Core metrics: incident/near-miss rate, rollback frequency, and data quality drift. |

## Slide 41: Ralph Wiggum Technique (Actual Definition)
| # | Claim | Flag | Safer alternative wording |
|---|---|---|---|
| 1 | Core loop: run the same prompt repeatedly (`while :; do cat PROMPT.md \| agent; done`) until completion signal. | `uncertain` | Core loop: run the same prompt repeatedly (`while :; do cat PROMPT.md \| agent; done`) until completion signal (validate with benchmarks, logs, or citations before stating as fact). |
| 2 | State is externalized to files + git, not chat history; each iteration can start with a fresh context window. | `uncertain` | State is externalized to files + git, not chat history; each iteration can start with a fresh context window (validate with benchmarks, logs, or citations before stating as fact). |
| 3 | Operational rule: one concrete item per loop to reduce context pollution and drift. | `stable` | Operational rule: one concrete item per loop to reduce context pollution and drift. |
| 4 | Add backpressure gates (tests, type checks, linters, scanners) so bad code is automatically rejected. | `stable` | Add backpressure gates (tests, type checks, linters, scanners) so bad code is automatically rejected. |
| 5 | Tune iteratively with explicit guardrail instructions (“signs”) when failure patterns appear. | `stable` | Tune iteratively with explicit guardrail instructions (“signs”) when failure patterns appear. |
