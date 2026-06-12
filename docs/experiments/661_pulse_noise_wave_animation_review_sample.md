# Experiment 661: Pulse/Noise And Wave Animation Review Sample

## Purpose

Prototype two reusable, CPU-only visualization scripts and apply them to one
recent completed coordinate-optimizer run for review before any archive-wide
backfill.

No FDTD, FWI, or optimizer simulation was launched for this work.

## Scripts

Added source/noise context visualization:

```text
run_experiment_pulse_noise_visualization.py
```

It reconstructs the configured Ricker source pulse, source frequency/time/
amplitude mismatch, delayed ringdown, and additive Gaussian observed-data noise
metadata from a coordinate-optimizer summary. It writes:

```text
figures/source_pulse_noise_context.png
data/source_pulse_noise_context_summary.json
```

Added geometric wave-propagation animation:

```text
run_experiment_wave_propagation_animation.py
```

It builds a travel-time schematic GIF from summary geometry: representative
Tx/Rx pair, outgoing wavefront, rebar reflection fronts, target highlight, and
approximate echo arrival timing. This is not an FDTD amplitude animation. It
writes:

```text
figures/geometric_wave_propagation.gif
data/geometric_wave_propagation_summary.json
```

Both scripts update `figures/FIGURE_NOTES.md` idempotently.

## Review Sample

Applied both scripts to:

```text
outputs/experiments/1124_coordinate_optimizer_variable_depth_radius_seed365435296162_target2_sources5_txrx60_ringdown050_objectives
```

Commands:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_pulse_noise_visualization.py \
  --summary outputs/experiments/1124_coordinate_optimizer_variable_depth_radius_seed365435296162_target2_sources5_txrx60_ringdown050_objectives/data/multi_rebar_coordinate_optimizer_summary.json

/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_wave_propagation_animation.py \
  --summary outputs/experiments/1124_coordinate_optimizer_variable_depth_radius_seed365435296162_target2_sources5_txrx60_ringdown050_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --frames 36 \
  --fps 8
```

## Sample Metadata

Pulse/noise condition:

```text
case: source_mismatch_ringdown050_noise10_seed365435296162
pulse type: Ricker / Mexican hat
base frequency: 1.5 GHz
frequency scale: 1.1
time shift: -50 ps
amplitude scale: 1.1
ringdown scale: 0.5
ringdown delay: 180 ps
ringdown frequency scale: 0.8
noise type: zero-mean Gaussian additive observed-data noise
noise RMS fraction: 0.1
noise seed: 365435296162
```

Geometric animation selected the Tx/Rx pair nearest the target2 rebar:

```text
Tx x: 346 mm
Rx x: 406 mm
target rebar index: 2
target two-way schematic time: 1.482 ns
concrete velocity model: c0 / sqrt(eps_r=6)
```

## Validation

Focused tests:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q tests/test_experiment_context_visualizations.py
4 passed
```

Generated sample validation:

```text
source_pulse_noise_context.png: 2314x1379 px, unique_colors=6412, nonwhite_fraction=0.1202
geometric_wave_propagation.gif: 977x621 px, 36 frames, midframe unique_colors=256, nonwhite_fraction=0.6831
```

Visual spot check:

```text
source/noise PNG: readable pulse, spectrum, noise proxy, and metadata panels
wave GIF: first frame readable; GIF validation confirms 36 nonblank frames
```

## Next Decision

Pause here for review. After feedback, refine the visual design if needed and
then backfill selectively: pulse/noise figures can be broadly backfilled for
compatible coordinate summaries, while wave-propagation GIFs should be reserved
for representative or decision-critical runs rather than forced onto every run.
