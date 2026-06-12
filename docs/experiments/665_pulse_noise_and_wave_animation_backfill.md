# Experiment 665: Pulse/Noise And Wave Animation Backfill

## Purpose

Backfill the newly approved pulse/noise context figures and geometric wave
propagation GIFs, and add a separate true-FDTD wavefield inventory path for
runs that already contain saved FDTD wavefield animations.

No FDTD, FWI, or optimizer simulation was launched for this backfill.

## Scripts

Updated reusable pulse/noise context script:

```text
run_experiment_pulse_noise_visualization.py
```

It now supports newest-first batch backfill with JSON/CSV audits and existing
valid artifact skips.

Updated reusable geometric wave propagation script:

```text
run_experiment_wave_propagation_animation.py
```

It now supports newest-first batch backfill with JSON/CSV audits and existing
valid artifact skips. This remains a geometry/travel-time schematic based on
true run geometry and acquisition metadata, not an FDTD field snapshot.

Added true-wavefield inventory script:

```text
run_existing_wavefield_animation_backfill.py
```

It validates already-saved FDTD wavefield GIFs, writes per-run inventories, and
updates figure notes. It deliberately skips runs without saved wavefield GIFs;
it does not regenerate field snapshots because that would require rerunning
FDTD.

## Commands

Archive pulse/noise pass:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_pulse_noise_visualization.py \
  --backfill-root outputs/experiments \
  --audit-json outputs/visualization_audits/20260610/pulse_noise_backfill_audit_20260610.json \
  --audit-csv outputs/visualization_audits/20260610/pulse_noise_backfill_audit_20260610.csv
```

Archive geometric GIF pass:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_wave_propagation_animation.py \
  --backfill-root outputs/experiments \
  --audit-json outputs/visualization_audits/20260610/geometric_wave_backfill_audit_20260610.json \
  --audit-csv outputs/visualization_audits/20260610/geometric_wave_backfill_audit_20260610.csv
```

Existing true-FDTD wavefield inventory pass:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_existing_wavefield_animation_backfill.py \
  --backfill-root outputs/experiments \
  --audit-json outputs/visualization_audits/20260610/existing_true_wavefield_backfill_audit_20260610.json \
  --audit-csv outputs/visualization_audits/20260610/existing_true_wavefield_backfill_audit_20260610.csv
```

Supplemental pass for completed concurrent runs 1126-1127:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_pulse_noise_visualization.py \
  --backfill-root outputs/experiments \
  --min-run-number 1126 \
  --max-run-number 1127 \
  --audit-json outputs/visualization_audits/20260610/pulse_noise_backfill_audit_20260610_latest.json \
  --audit-csv outputs/visualization_audits/20260610/pulse_noise_backfill_audit_20260610_latest.csv

/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_wave_propagation_animation.py \
  --backfill-root outputs/experiments \
  --min-run-number 1126 \
  --max-run-number 1127 \
  --audit-json outputs/visualization_audits/20260610/geometric_wave_backfill_audit_20260610_latest.json \
  --audit-csv outputs/visualization_audits/20260610/geometric_wave_backfill_audit_20260610_latest.csv

/home/lam001/miniforge3/envs/FNO/bin/python run_existing_wavefield_animation_backfill.py \
  --backfill-root outputs/experiments \
  --min-run-number 1126 \
  --max-run-number 1127 \
  --audit-json outputs/visualization_audits/20260610/existing_true_wavefield_backfill_audit_20260610_latest.json \
  --audit-csv outputs/visualization_audits/20260610/existing_true_wavefield_backfill_audit_20260610_latest.csv
```

## Counts

Pulse/noise context:

```text
archive pass: generated=529, skipped=596
latest 1126-1127 pass: generated=2
current source_pulse_noise_context.png files: 532
```

Geometric wave propagation GIFs:

```text
archive pass: generated=493, skipped=632
latest 1126-1127 pass: generated=2
current geometric_wave_propagation.gif files: 496
```

Existing true FDTD wavefield inventories:

```text
archive pass: generated=18, skipped=1109
latest 1126-1127 pass: skipped=2
current existing_true_wavefield_animations_summary.json files: 18
```

The 36-run gap between pulse/noise and geometric GIF coverage is expected:
those older coordinate summaries have enough source/noise metadata for pulse
figures but lack compatible geometry/acquisition metadata for travel-time
schematics.

Run 1128 was active during handoff and was not touched.

## True Wavefield Scope

The true-FDTD wavefield path found existing saved wavefield GIFs in these older
runs:

```text
052-062, 100-104, 194-195
```

These were validated and inventoried. Recent coordinate-optimizer runs do not
retain raw Ez snapshot arrays or true wavefield GIFs, so they were skipped by
the true-wavefield script rather than approximated. Their geometric schematic
GIFs provide the broad propagation-path context.

## Validation

Focused tests:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_experiment_context_visualizations.py \
  tests/test_existing_wavefield_animation_backfill.py
9 passed
```

Byte compilation:

```text
py_compile passed for:
run_experiment_pulse_noise_visualization.py
run_experiment_wave_propagation_animation.py
run_existing_wavefield_animation_backfill.py
```

Spot checks:

```text
1127 source_pulse_noise_context.png: 2314x1379 px, unique_colors=6539, nonwhite_fraction=0.1183
1127 geometric_wave_propagation.gif: 977x621 px, 36 frames, midframe unique_colors=256, nonwhite_fraction=0.6831
```

Visual inspection:

```text
1127 pulse/noise figure shows seed591286729879, noise RMS fraction 0.1, Ricker source, ringdown, and noise proxy.
1127 geometric GIF frame shows Tx/Rx path, true rebars, target2 highlight, and forward-wavefront legend.
```

## Next Decision

When active run 1128 completes, run the same supplemental pulse/noise and
geometric GIF commands for that run range. Do not create true FDTD wavefield
animations for recent coordinate runs unless the forward run is deliberately
configured to save Ez snapshots or a future experiment stores snapshot arrays.
