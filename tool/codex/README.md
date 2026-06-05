# Codex Visualization Tools

This folder contains lightweight reporting and visualization utilities for the
GPR-FDTD-FWI experiment archive.

## Presentation Context Figures

Generate the selected presentation/context figure set with:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python tool/codex/presentation_visuals.py --all
```

Default output folder:

```text
outputs/presentation_figures/2026_06_05_context_figures
```

The script reads archived experiment JSON/CSV files and does not run FDTD
simulations. See `001_2026-06-05_presentation_visualization_plan.md` for the
figure index, source grounding, and campaign rationale.
