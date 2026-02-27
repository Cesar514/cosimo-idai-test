# IEEE T-RO Robotics Maze Paper

This directory contains the IEEEtran manuscript sources, build entrypoints, and submission artifacts.

## Build commands

Run from `paper/ieee_tro_robotics_maze`:

```bash
make pdf
```

- Source: `Makefile` target `pdf`
- Effective compiler invocation:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Clean LaTeX build outputs:

```bash
make clean
```

Build output:

- `main.pdf`

## Key inputs

Primary manuscript inputs:

- `main.tex`
- `sections/02_introduction.tex`
- `sections/03_related_work.tex`
- `sections/04_method.tex`
- `sections/05_experiments.tex`
- `sections/06_results.tex`
- `sections/07_discussion.tex`
- `sections/08_conclusion.tex`
- `sections/A_appendix.tex`
- `appendix/mathematical_formulation.tex`
- `appendix/reproducibility_checklist.tex`
- `tables/closest_work_delta_table.tex`
- `tables/experiment_protocol_table.tex`
- `tables/main_results_table.tex`
- `tables/statistical_comparison_table.tex`
- `figures/system_pipeline.png`
- `figures/benchmark_runtime_ms.png`
- `figures/runtime_uncertainty.png`
- `figures/benchmark_expansions.png`
- `figures/benchmark_success_rate.png`
- `references.bib`

Evidence/provenance inputs referenced by manuscript + coordination files:

- `../../robotics_maze/results/benchmark_results.csv`
- `../../robotics_maze/results/benchmark_summary.md`
- `coordination/inferential_runtime_comparison.csv`
- `coordination/figure_manifest.csv`

Benchmark regeneration command documented in `robotics_maze/results/README.md` (run from repository root):

```bash
python3 robotics_maze/src/benchmark.py --mazes 50 --width 15 --height 15 --algorithm backtracker --seed 7
```

Equivalent command from `paper/ieee_tro_robotics_maze`:

```bash
python3 ../../robotics_maze/src/benchmark.py --mazes 50 --width 15 --height 15 --algorithm backtracker --seed 7
```

## Artifact paths

- Local build artifact: `main.pdf`
- Submission PDF: `submission/ieee_tro_robotics_maze_main.pdf`
- Submission source package: `submission/ieee_tro_robotics_maze_source.zip`
- Build + quality status ledger: `coordination/paper_status.md`

## Latest submission artifact hashes

Current files in `submission/`:

| Artifact | Size (bytes) | Modified (UTC) | SHA-256 |
| --- | ---: | --- | --- |
| `submission/ieee_tro_robotics_maze_main.pdf` | 1026654 | 2026-02-26 23:52:59 +0000 | `8a2caef1edd77ee1f328661a628cbb2a5c5f2f0c94953ca42afa5115e5182f24` |
| `submission/ieee_tro_robotics_maze_source.zip` | 990176 | 2026-02-27 00:20:17 +0000 | `0456079f8f62ae63e527dd0a8294cb1e7f0678fef7085348b1e32feae61e7c8b` |

Recompute:

```bash
shasum -a 256 submission/ieee_tro_robotics_maze_main.pdf submission/ieee_tro_robotics_maze_source.zip
```
