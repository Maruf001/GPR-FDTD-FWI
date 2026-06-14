# Figure Animation Template Index

This folder is a migration-safe index for the figure and animation templates.
The canonical scripts were not moved or copied; they remain at the repository
root where tests and existing imports already expect them.

Use the root inventory for the full audit:

```text
FIGURE_ANIMATION_TEMPLATE_INVENTORY.md
```

## Canonical Generators

| Artifact | Script |
| --- | --- |
| `system_scene_geometry.png` | `run_experiment_scene_visualization.py` |
| `source_pulse_noise_context.png` | `run_experiment_pulse_noise_visualization.py` |
| `geometric_wave_propagation.gif` | `run_experiment_wave_propagation_animation.py` |
| `fdtd_wavefield_amplitude.gif` | `run_experiment_fdtd_wavefield_animation.py` |
| coordinate/report figures | `run_multi_rebar_coordinate_optimizer.py` |
| existing wavefield GIF inventory | `run_existing_wavefield_animation_backfill.py` |

## Policy

- Core future outputs: scene geometry, source/noise context, coordinate
  confidence margins, radius decision panel, objective radius candidates, and
  figure notes.
- Optional/selective outputs: `geometric_wave_propagation.gif` and
  `fdtd_wavefield_amplitude.gif`.
- Do not delete or overwrite old figures during migration.
- Use skip-existing backfill commands first.
- Treat uppercase `FDTD_wavefield_amplitude.gif` as a requested/display name;
  the current real artifact is lowercase `fdtd_wavefield_amplitude.gif`.

## Quick Commands

Scene geometry:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_scene_visualization.py \
  --summary outputs/experiments/<RUN>/data/multi_rebar_coordinate_optimizer_summary.json
```

Source pulse/noise:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_pulse_noise_visualization.py \
  --summary outputs/experiments/<RUN>/data/multi_rebar_coordinate_optimizer_summary.json
```

Geometric schematic GIF:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_wave_propagation_animation.py \
  --summary outputs/experiments/<RUN>/data/multi_rebar_coordinate_optimizer_summary.json \
  --frames 36 \
  --fps 8
```

True FDTD wavefield GIF:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_fdtd_wavefield_animation.py \
  --summary outputs/experiments/<RUN>/data/multi_rebar_coordinate_optimizer_summary.json \
  --backend cpu
```

Focused tests:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_experiment_scene_visualization.py \
  tests/test_experiment_context_visualizations.py \
  tests/test_experiment_fdtd_wavefield_animation.py \
  tests/test_wavefield_animation.py \
  tests/test_multi_rebar_coordinate_optimizer.py
```
