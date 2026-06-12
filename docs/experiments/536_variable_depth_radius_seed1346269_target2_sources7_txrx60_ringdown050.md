# Experiment 536: Seed1346269 Target2 Sources=7 Tx/Rx=60 Ringdown050

## Purpose

Run 1002 brackets the seed1346269 target2 source-density rescue at the original
Tx/Rx=60 setting. The previous branch used 5 sources as a weak control and
9 sources as an accepted rescue; this run tests whether 7 sources are enough.

## 1002: Coordinate Optimizer Variable-Depth/Radius Seed1346269 Target2 Sources=7 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1002_coordinate_optimizer_variable_depth_radius_seed1346269_target2_sources7_txrx60_ringdown050_objectives
```

Command parameters:

```text
backend: gpu-cpml
grid_step_mm: 1.0
sources: 7
tx_rx_offset_mm: 60.0
target_indices: [2]
truth: x=[150,250,350] mm, z=[80,100,120] mm, r=[5,6,8] mm
candidate grid: x_offset=[0], z_offset=[0,1], radius_offset=[0,0.25,0.5,0.75,1.0,1.25]
replication case: source_mismatch_ringdown050_noise10_seed1346269
source profile grid: frequency=[0.9,1.0,1.1], time_shift=[-50,0,50] ps, fitted amplitude and ringdown coefficient
diagnostics: base, highband, late, late_high, veryhigh, early_high
```

## Results

Run 1002 is exact and base-accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.181048e-04
offset from cutoff: +1.810477e-05
confidence label: moderate
fallback warning: none
elapsed: 493.3 s
```

Diagnostic objective margins:

```text
base       5.181048e-04  above cutoff
highband   6.591267e-04  above cutoff
late       7.125618e-04  above cutoff
late_high  7.823203e-04  above cutoff
veryhigh   6.532334e-04  above cutoff
early_high 4.408620e-04  below cutoff
```

All six objective variants rank the true target2 geometry first.

## Interpretation

Seed1346269 target2 does not need the full 9-source rescue for base
acceptance: 7 sources at Tx/Rx=60 are enough. The early_high diagnostic still
fails, so this should be reported as a base-confidence rescue with an
early_high caveat rather than a clean all-objective replacement.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.247327 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target2 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=7; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90%; Python process RSS stayed about 455 MB
```

## Next Decision

Run seed1346269 target1 at 5 sources and Tx/Rx=52.5 as an offset safety check.
That run is underway as experiment 1003.
