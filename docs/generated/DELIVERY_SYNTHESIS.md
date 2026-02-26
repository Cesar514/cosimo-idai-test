# Delivery Synthesis: Smart Docs + Frontend Design

Date: 2026-02-26  
Status: presentation-ready

## Integrated Message

The smart-docs package defines the technical truth (architecture, workflow, and artifact pipeline).  
The frontend-design package defines the visual language (layout templates, imagery system, and readability guardrails).  
Together, they produce a single delivery path: evidence-backed technical narrative that is visually consistent, high-clarity, and ready for a live deck walkthrough.

## Smart-Docs to Deck Crosswalk

| Smart-doc anchor | Narrative payload | Deck zone | Frontend-design binding |
|---|---|---|---|
| `1. Project Overview` | Scope, stack, key capabilities, project map | 1-6 | `T1`, `T2`, `T4`; concepts `C01`, `C02`; keep opening visual hook with text-safe left region |
| `2. Architecture Overview` (C4 L1-L3) | System context, containers, component run loop, design decisions | 6, 16-20, 31-33 | `T4` for architecture maps; `T2` for trust/control slides; concepts `C02`, `C04` |
| `3. Workflow Overview` (Run, Benchmark, Screenshot/Deck) | End-to-end operational sequence from command to artifact | 13, 18-20, 34-38 | `T3` for process bands, `T4` for loops, `T2` for action panels; concepts `C05`, `C06`, `C07`, `C11` |
| `Deep Dive: Execution Orchestration` | Config parsing, loaders, deterministic episode loop, fallback behavior | 17-20, 34-35 | Diagram-first slides with one dominant visual; preserve >=58% text area on dense slides |
| `Deep Dive: Planning and Maze Domain` | Deterministic maze generation, planner registry, alt-planner surface | 21-30, 36-37 | Repeated `T2` right-panel geometry for rhythm; card/flow visuals via `C03`, `C06` |
| `Deep Dive: Simulation + Benchmark/Artifacts` | Backend selection, path normalization, ranking policy, output contracts | 35-42 | `T4` for debug/deploy loops, `T7` for risk/reward contrast, `T8` for close; concepts `C05`, `C07`, `C08`, `C09` |

## Presentation Integration Rules

1. Keep technical claims sourced from smart-docs sections; visuals must explain, not replace, those claims.
2. For dense technical slides, use `T2`/`T4` and keep minimum `58%` text footprint.
3. Enforce one dominant visual per slide and accent discipline (`#0B5FFF` primary, one secondary accent).
4. Preserve sequence rhythm from `image_layout_plan.md`: heavy visual slides are separated by lighter recovery slides.
5. Maintain attribution footer lane for third-party or curated imagery (`R*`, `W*` assets).

## Delivery-Ready Checklist

- Smart-doc anchors are mapped to slide clusters with no orphan technical section.
- Visual templates and concept IDs are assigned to each mapped cluster.
- Readability constraints and overlay rules are defined for projector-safe viewing.
- Robotics ending (39-42) has a clear escalation from system proof to risk/reward to call-to-action.

## Source Inputs

- `docs/generated/INDEX.md` and linked generated architecture/workflow/deep-dive docs
- `presentation_assets/image_layout_plan.md`
- `presentation_assets/custom/frontend_imagery_curation.md`
