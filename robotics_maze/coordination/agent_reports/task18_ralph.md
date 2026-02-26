# Task 18/36 - Ralph Wiggum Technique Research

- Date (UTC): 2026-02-26
- Ownership: `presentation_assets/references_notes.md`, `robotics_maze/coordination/agent_reports/task18_ralph.md`
- Goal: Validate terminology and provide accurate replacement phrasing + references for slide narrative.

## Verdict

- The phrase "Ralph Wiggum technique" is not fabricated: it appears in current community tooling/docs.
- It is an informal/community label, not a standardized software engineering term.
- For a presentation claiming "actual definition," neutral terminology is more accurate.

## Recommended Slide Language

- Recommended title: `Fresh-Context Agent Loop (Externalized State)`
- Optional alias line: `Community alias: "Ralph Wiggum loop"`

Suggested narrative bullets:

1. Run a bounded loop: execute agent -> check completion signal -> repeat.
2. Persist durable state in repository artifacts (files/tests/commits), not chat memory.
3. Enforce backpressure gates (tests, lint, type checks, required status checks) before accepting progress.

## Reference Recommendations

Primary technical anchors for slide narrative:

1. GNU Bash manual, looping constructs:
   `https://www.gnu.org/software/bash/manual/html_node/Looping-Constructs`
2. Git docs (working tree/index/object database model):
   `https://git-scm.com/docs/git`
3. GitHub rulesets (required status checks):
   `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets`
4. 12-Factor app, stateless processes:
   `https://www.12factor.net/processes`

Community-term provenance (for alias context only):

1. Vercel Labs `ralph-loop-agent`:
   `https://github.com/vercel-labs/ralph-loop-agent`
2. Wiggum docs, loop concept:
   `https://wiggum.dev/concepts/the-loop/`

## Research Notes

- As of 2026-02-26, web checks show usage in OSS/community docs.
- As of 2026-02-26, no clear evidence this phrase is a formal term in peer-reviewed software engineering literature.
- Therefore: keep the concept, replace the headline terminology for factual precision.
