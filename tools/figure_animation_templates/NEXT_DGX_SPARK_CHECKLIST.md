# Next DGX Spark Figure Checklist

Use this checklist after the project folder and local output archive are
migrated to the next NVIDIA DGX Spark machine.

## 1. Confirm Migration State

- Check that the source repository is present.
- Check that `outputs/experiments/` is present; it is local artifact data and
  is not a normal Git-tracked clone artifact.
- Check that `outputs/visualization_audits/` is present.
- Check that the reference runs exist:
  - `outputs/experiments/1160_coordinate_optimizer_variable_depth_radius_seed17167680207565_target1_sources9_txrx60_ringdown050_objectives`
  - `outputs/experiments/1218_coordinate_optimizer_variable_depth_radius_seed5527939710754757_target1_sources11_txrx60_ringdown050_objectives`

## 2. Inspect The Target Experiment Folder

- Locate the run folder under `outputs/experiments/<RUN>_...`.
- Confirm `data/multi_rebar_coordinate_optimizer_summary.json` exists.
- Confirm `figures/` and `data/` exist or let the generator create them.
- Read existing `figures/FIGURE_NOTES.md` before changing anything.

## 3. Verify Required Core Figures

For each future coordinate experiment, verify:

- `figures/system_scene_geometry.png`
- `figures/source_pulse_noise_context.png`
- `figures/coordinate_confidence_margins.png`
- `figures/coordinate_radius_decision_panel.png`
- `figures/coordinate_objective_radius_candidates.png` when top-candidate rows exist
- `figures/FIGURE_NOTES.md`

Do not delete or replace `coordinate_confidence_margins.png`; it is the legacy
compact summary and should be preserved.

## 4. Generate Missing Core Context Safely

Generate scene geometry from real summary metadata:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_scene_visualization.py \
  --summary outputs/experiments/<RUN>/data/multi_rebar_coordinate_optimizer_summary.json
```

Generate source pulse/noise context from real summary metadata:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_pulse_noise_visualization.py \
  --summary outputs/experiments/<RUN>/data/multi_rebar_coordinate_optimizer_summary.json
```

For batch work, use backfill commands without `--refresh-existing` first and
write audit JSON/CSV under `outputs/visualization_audits/YYYYMMDD/`.

## 5. Optional GIF Backfill

Generate schematic travel-time GIFs only for selected runs:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_wave_propagation_animation.py \
  --summary outputs/experiments/<RUN>/data/multi_rebar_coordinate_optimizer_summary.json \
  --frames 36 \
  --fps 8
```

Generate true FDTD wavefield GIFs only for selected runs:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_fdtd_wavefield_animation.py \
  --summary outputs/experiments/<RUN>/data/multi_rebar_coordinate_optimizer_summary.json \
  --backend cpu
```

Use `--backend gpu-cpml` only after confirming the GPU environment. Do not
broad-generate true FDTD GIFs automatically.

## 6. Preserve And Document

- Preserve older figures and notes.
- Do not overwrite existing artifacts unless the user explicitly approves a
  refresh.
- Update `figures/FIGURE_NOTES.md` through the scripts where possible.
- Record commands, output paths, validation, and interpretation in a tracker
  under `docs/experiments/`.

## 7. Verify

Run focused tests:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_experiment_scene_visualization.py \
  tests/test_experiment_context_visualizations.py \
  tests/test_experiment_fdtd_wavefield_animation.py \
  tests/test_wavefield_animation.py \
  tests/test_multi_rebar_coordinate_optimizer.py
```

Check generated outputs:

```bash
find outputs/experiments/<RUN>/figures -maxdepth 1 -type f | sort
find outputs/experiments/<RUN>/data -maxdepth 1 -type f | sort
```

Remember: the current true FDTD artifact is lowercase
`fdtd_wavefield_amplitude.gif`.
