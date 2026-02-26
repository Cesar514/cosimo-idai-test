# Subscription and Local-Model Cost Notes (Slides 15-16)

Date stamp: 2026-02-26  
Scope: `Subscription Prices Snapshot (US, Feb 26, 2026)` and `Local Models: When and Why to Use Them`

## Required Caveat Before Presenting
- This note is a point-in-time planning artifact dated `2026-02-26`.
- Vendor pricing, plan names, and included quotas can change without notice.
- Re-verify all live prices on presentation day before showing any numeric claim.
- If a value differs from these notes, use the vendor page value and update slide copy.

## Primary Sources to Re-Check on Presentation Day
- OpenAI pricing docs: `https://developers.openai.com/docs/pricing`
- GitHub Copilot subscription plans: `https://docs.github.com/en/copilot/about-github-copilot/subscription-plans-for-github-copilot`
- Google developer plans/pricing: `https://developers.google.com/program/plans-and-pricing`
- Local tooling references (capability context, not vendor-price authority):
  - `https://github.com/ollama/ollama`
  - `https://lmstudio.ai/docs`

## Comparison Frame
| Dimension | Hosted Subscriptions / APIs | Local Model Stack |
| --- | --- | --- |
| Cost shape | Mostly recurring (`$ / seat / month` plus usage) | Upfront hardware + recurring power/ops |
| Startup effort | Low | Medium to high |
| Marginal cost at higher usage | Can rise quickly with token/tool usage | Usually flatter until hardware saturates |
| Privacy/data residency | Depends on vendor controls | Stronger local control by default |
| Performance ceiling | Vendor-managed | Bounded by local hardware |
| Operations burden | Lower | Higher (drivers, model hosting, updates) |

## Assumption-Based Cost Model (for Talking Points)
Use this model if live vendor pricing cannot be pasted into the deck in time.  
These are modeling assumptions, not authoritative public price quotes.

Assumptions:
- Blended hosted spend per active engineer per month: `H = $40` (`seat + light API usage`)
- Local workstation CapEx: `C = $4,800`
- Amortization: `24` months
- Local recurring OpEx: `P + O = $160 / month` (`power/cooling + maintenance time`)

Derived monthly totals:
- Hosted team monthly cost: `Hosted(N) = 40 * N`
- Local monthly baseline: `Local = (4800 / 24) + 160 = 360`

Break-even headcount (assumption case):
- `Hosted(N) = Local` -> `40N = 360` -> `N = 9`
- Interpretation: around `9` consistently active users, local cost can begin to look favorable under these assumptions.

Example monthly comparison (assumption case):
| Active engineers (`N`) | Hosted (`40 * N`) | Local baseline (`360`) |
| ---: | ---: | ---: |
| 3 | $120 | $360 |
| 6 | $240 | $360 |
| 9 | $360 | $360 |
| 12 | $480 | $360 |

## Slide 15 Talking Notes (Subscription Snapshot)
- Emphasize that subscription/API spend is an operating-policy decision, not just a vendor decision.
- Keep one sentence: "As of `2026-02-26`, this is a snapshot and must be rechecked before every live talk."
- Explain spend levers:
  - who gets premium tiers
  - which tasks route to high-cost models
  - how often autonomous runs are allowed

## Slide 16 Talking Notes (Local Models)
- Position local models as cost-stability + privacy + lower-latency for routine workloads.
- Call out local hidden costs explicitly:
  - hardware refresh cadence
  - engineering time for operations
  - throughput limits under parallel load
- Recommend hybrid routing policy:
  - local default for routine tasks
  - hosted premium models for hard reasoning and high-stakes reviews

## Presenter Checklist (T-24h and T-1h)
- Re-open all three pricing pages above and capture current values.
- Validate plan names and included quotas match slide text.
- Recompute any shown totals if prices changed.
- Update the slide subtitle or speaker note date if presented after `2026-02-26`.
