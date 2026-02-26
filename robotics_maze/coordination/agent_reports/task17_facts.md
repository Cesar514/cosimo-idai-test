# Task 17/36 - Factual Correctness Reviewer

Date: 2026-02-26
Owner file: `robotics_maze/coordination/agent_reports/task17_facts.md`
Related audit: `agents_factual_risk_audit.md`

## Scope
Focused factual-risk review for deck claims in three volatile areas:
- model naming/availability
- pricing and plan entitlements
- agent behavior/mode claims

## Summary outcome
- Updated `agents_factual_risk_audit.md` with concrete corrections for slides `9`, `12`, `13`, `14`, `15`, `16`, `18`, `19`, `35`, `39`, and `40`.
- Replaced stale or speculative wording (for example, "preview status" and "YOLO by default") with source-backed statements.
- Added date-scoped caveats wherever vendor docs are likely to drift.

## High-risk findings and corrections
| Area | Risk found | Correction applied (as of 2026-02-26) | Caveat |
|---|---|---|---|
| Codex default behavior | Deck implied `--yolo`/full-autonomy default. | Updated to documented default approval mode `Auto`; full-access mode treated as explicit escalation. | Defaults can change by release/profile. |
| Codex vs Gemini planning parity | Deck implied both tools expose comparable plan mode primitives. | Split claims: Gemini has explicit experimental Plan Mode (`/plan`, `--approval-mode=plan`), while public Codex docs describe approval modes (`Auto`, `Read-only`, `Full Access`). | Vendor UX may converge/diverge over time. |
| Copilot agent status | Deck used stale "preview status" wording. | Reframed as availability and execution constraints: plan eligibility + ephemeral GitHub Actions runtime + repo policy gates. | Plan entitlements/features can change by plan and org policy. |
| OpenAI pricing | Business price in deck was stale (`$25`). | Updated to Codex pricing page snapshot (`Plus $20`, `Pro $200`, `Business $30/user/mo`) with US snapshot caveat. | Taxes, region, currency, and promos vary. |
| GitHub Copilot pricing | Needed precise values and billing units. | Updated to docs values (`Pro $10/mo or $100/yr`, `Pro+ $39/mo or $390/yr`, `Business $19/seat/mo`, `Enterprise $39/seat/mo`). | Regional taxes/contract terms may alter invoice totals. |
| Google AI + Jules pricing/limits | Exact prices and Jules limits are dynamic. | Kept launch-price references (`Pro $19.99`, `Ultra $249.99` US) and tied Jules to documented tiered limits (`Jules in Pro`, `Jules in Ultra`). | Region/promo-dependent checkout and evolving usage limits. |
| Codex roles | Role naming can drift by host implementation. | Public docs retained (`default`, `worker`, `explorer`, `monitor`) with explicit caveat that this workspace schema exposes `awaiter` for long waits. | Host/runtime-specific schemas can differ from public docs. |
| GPT-5.2 Pro claim | Needed direct evidence, not assertion. | Retained claim with source-backed phrasing: GPT-5.2 Pro marked "Reasoning: Highest" and "Responses API only". | Model catalog and positioning can change quickly. |
| GPT-oss hardware phrasing | "single H100" read as hard requirement. | Reworded as cookbook guidance for 120b, not a mandatory requirement. | Hardware guidance is workload/config dependent. |
| GPT-5.3-Codex + sensors claim | Coupled model validity with deployment-specific sensor wiring. | Kept model name and separated sensor statement into conditional tool/MCP integration with safety controls. | Real-world sensor integration is architecture- and safety-policy-specific. |

## Claim class guidance used in edits
- `needs-date`: versioned models, plan prices, feature availability, defaults, and limits.
- `uncertain`: cross-agent behavior comparisons without benchmark data.
- `stable`: process guidance that does not depend on vendor release cadence.

## Primary sources used
- OpenAI Codex docs:  
  `https://developers.openai.com/codex/cli/`  
  `https://developers.openai.com/codex/cli/features/`  
  `https://developers.openai.com/codex/multi-agent/`  
  `https://developers.openai.com/codex/models/`  
  `https://developers.openai.com/codex/pricing/`  
  `https://developers.openai.com/codex/config-advanced/#oss-mode-local-providers`
- OpenAI model page:  
  `https://developers.openai.com/api/docs/models/gpt-5.2-pro`
- GitHub Copilot docs:  
  `https://docs.github.com/en/copilot/get-started/plans-for-github-copilot`  
  `https://docs.github.com/en/copilot/how-tos/agents/copilot-coding-agent/delegate-tasks/delegate-tasks-to-copilot`
- Gemini CLI upstream docs (Google):  
  `https://github.com/google-gemini/gemini-cli/blob/main/README.md`  
  `https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/plan-mode.md`  
  `https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/planning.md`
- Google AI/Jules pricing and limits context:  
  `https://blog.google/products/google-one/google-ai-ultra/`  
  `https://one.google.com/about/ai-premium/`  
  `https://jules.google/docs/usage-limits`

## Residual risks
- Live pricing pages can render region/promo-dependent values that differ from static doc captures.
- Cross-agent behavior claims remain non-portable unless backed by internal benchmark traces.
- Some product pages change faster than release-note cadence; date-stamping remains mandatory for slide publication.
