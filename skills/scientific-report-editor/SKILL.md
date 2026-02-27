---
name: "scientific-report-editor"
description: "Draft, improve, and quality-gate technical or scientific reports in publication-grade prose; run multi-pass review, math-aware formatting, and visual validation by coordinating doc, pdf, and screenshot workflows."
---

# Scientific Report Editor

Use this skill when a task asks to write a report from source notes, improve an existing report, enforce technical-scientific style, or polish `.docx/.pdf` report outputs.

## Core workflow

1. Define the target artifact and constraints
   - Capture audience, venue, maximum length, citation style, and language level.
   - Confirm source material, key claims, datasets, assumptions, and required sections.
   - Decide output format priority (`.docx`, `.pdf`, or both).

2. Build version 0 from source and requirements
   - Produce complete structure before wording optimization.
   - Use a standard scientific report spine: Abstract, Introduction, Methodology, Results, Discussion, Limitations, Conclusion, References.
   - Keep claims evidence-linked; avoid adding unsupported factual statements.

3. Apply mandatory math formatting rules on first pass
   - Use inline math only when the symbol density is low and expression is short.
   - Use display math for key definitions, derivations, optimization problems, and long expressions.
   - Prefer the native equation editor for DOCX and native LaTeX/renderer flow for PDF generation.
   - Do not leave raw placeholders for unresolved formulas.

4. Launch parallel micro-reviews (Pass 2)
   - Spawn 2-4 mini agents with different focuses (science logic, clarity, methods, style).
   - Treat their output as advisory only.
   - Send each mini agent a minimal rubric and ask for prioritized change proposals only.

5. Perform controlled rewrite pass (Pass 3)
   - Integrate high-confidence suggestions first.
   - Resolve conflicts by favoring evidence accuracy and reproducibility over rhetorical polish.
   - Update section transitions and terminology to remove ambiguity.

6. Run technical + layout critic pass (Pass 4)
   - Re-check claims against provided evidence and data.
   - Tighten causal wording, remove overclaims, and fill missing caveats.
   - Validate visuals and math density for readability.

7. Run final agent review (Pass 5)
   - Independently review the complete report from the perspective of a domain expert and journal editor.
   - Keep only blocking issues for another revision; defer low-value style nits.

8. Deliver.
   - Return a final artifact with a short pass log: major issues found, edits made, unresolved risks.

## Multi-pass quality gates

- Minimum: 4 passes (Draft + 2 + 3 + 5).
- Preferred: 5 passes including Pass 4 and Pass 5.
- Default behavior: run all 5 passes unless user explicitly requests fast mode.
- Hard rule: the "big agent" (main run) applies every improvement; mini agents do not edit directly.

## Integration with document workflows

- For `.docx` drafting/editing, use the `doc` skill for structure checks, typography, and layout fixes.
- For `.pdf`, use the `pdf` skill for render checks and page-level validation.
- For visual plausibility in desktop clients and desktop editors, capture screenshots and inspect rendering before finalizing.
- Save screenshots to temporary locations for internal checks unless user requests persistent output.

## Math equation policy

- Keep equations readable for experts and non-experts.
- Use consistent variable naming and define each symbol at first appearance.
- Prefer native equation objects over plain text approximations.
- Ensure punctuation and spacing around equations remain grammatically correct.

## Review rubric used by mini agents

- `scientific-report-editor/references/review-rubric.md`: claim validity, logic flow, methods coherence, and interpretation risks.
- `scientific-report-editor/references/math-and-notation.md`: equation placement, symbol clarity, notation consistency, and accessibility.

## Fallbacks

- If a requested formatting path is blocked (missing dependency, editor limitation, unsupported symbol), produce a clean-text backup in this format:
  - Keep math in LaTeX-safe notation.
  - Call out each limitation and a remediation option.
- Never invent references, measurements, or datasets.

## Delivery standards

- Keep prose specific, technical, and human-like; avoid generic filler.
- Preserve nuance, causal limits, and uncertainty language.
- Prefer exact language over simplification when technical precision is required.
- Deliver in a single coherent style; avoid section-by-section tone shifts.
