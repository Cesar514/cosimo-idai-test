# Privacy Audit Report (Agent 03 - Presentation Assets)

Date: 2026-02-27

## Scope
- `presentation_assets/` (text assets only)
- `agents.pptx` (slide text extracted from PPTX XML)
- `agents_factual_risk_audit.md`
- `agents_factual_risk_audit_draft.md`

## What Was Checked
- Private data indicators: names, location/time details, emails, credentials/tokens, key material.
- Host-specific path indicators: absolute local paths (`/Users/...`, `/home/...`, `C:\\...`), `localhost`, loopback/file URLs.

## Findings

| Severity | Type | Evidence | Notes |
|---|---|---|---|
| Medium | Personal/event-identifying data | `agents_factual_risk_audit.md:41`, `agents_factual_risk_audit.md:48`, `agents_factual_risk_audit.md:49` | Contains full name (`Cesar Contreras`) plus location (`Elm House 214 + Teams`) and event date/time. |
| Medium | Personal/event-identifying data | `agents_factual_risk_audit_draft.md:9`, `agents_factual_risk_audit_draft.md:16`, `agents_factual_risk_audit_draft.md:17` | Same name + location/date/time tuple repeated in draft audit text. |
| Medium | Personal/event-identifying data in deck | `agents.pptx` slide text: `slide1.xml` (`Cesar Contreras | Friday 27 February 2026`), `slide2.xml` (`Location: Elm House 214 + Teams`, `Date: Friday 27 February 2026 | Time: 11:00`) | Present in rendered slide content; not a host path leak, but sensitive meeting/person metadata. |

## No Findings (Explicitly Checked)
- No host-specific absolute paths found in scoped text assets or extracted PPTX XML.
- No secret/token/key patterns found (AWS keys, GitHub/OpenAI/Slack tokens, private key blocks).
- No email addresses found in scoped assets.

## Recommended Remediation
1. Replace person-identifying + meeting-location details with role-level placeholders for shareable artifacts (e.g., `Presenter`, `Room TBD / Remote`).
2. Keep exact schedule/location only in a private distribution copy if required operationally.
3. Add a pre-publish scrub checklist item for `name + date/time + location` combinations in deck and audit files.

