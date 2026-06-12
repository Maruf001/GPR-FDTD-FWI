# Experiment 535: Seed1346269 Target2 Sources=5 Tx/Rx=52.5 Ringdown050

## Purpose

Run 1001 tests whether Tx/Rx=52.5 can rescue seed1346269 target2 at the
original 5-source density after the Tx/Rx=60 5-source row was exact but weak.

## 1001: Coordinate Optimizer Variable-Depth/Radius Seed1346269 Target2 Sources=5 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1001_coordinate_optimizer_variable_depth_radius_seed1346269_target2_sources5_txrx52p5_ringdown050_objectives
```

Command parameters:

```text
backend: gpu-cpml
grid_step_mm: 1.0
sources: 5
tx_rx_offset_mm: 52.5
target_indices: [2]
truth: x=[150,250,350] mm, z=[80,100,120] mm, r=[5,6,8] mm
candidate grid: x_offset=[0], z_offset=[0,1], radius_offset=[0,0.25,0.5,0.75,1.0,1.25]
replication case: source_mismatch_ringdown050_noise10_seed1346269
source profile grid: frequency=[0.9,1.0,1.1], time_shift=[-50,0,50] ps, fitted amplitude and ringdown coefficient
diagnostics: base, highband, late, late_high, veryhigh, early_high
```

## Results

Run 1001 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 4.858530e-04
offset from cutoff: -1.414697e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 362.7 s
```

Diagnostic objective margins:

```text
base       4.858530e-04  below cutoff
highband   5.702407e-04  above cutoff
late       7.609306e-04  above cutoff
late_high  7.526105e-04  above cutoff
veryhigh   6.444679e-04  above cutoff
early_high 4.085969e-04  below cutoff
```

All six objective variants rank the true target2 geometry first.

## Interpretation

Tx/Rx=52.5 is not a 5-source remedy for seed1346269 target2. It keeps the
same truth-preserving but weak behavior, with base and early_high below cutoff.
Use source-density bracketing next: test 7 sources at the original Tx/Rx=60
before assuming the previously accepted 9-source row is the minimum.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.232903 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target2 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and identifies the weak target2 row
metadata validation: tx_rx_offset_mm is 52.5; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88%; Python process RSS stayed about 452 MB
```

## Next Decision

Run seed1346269 target2 with 7 sources at Tx/Rx=60. That intermediate
source-density bracket is underway as experiment 1002.
