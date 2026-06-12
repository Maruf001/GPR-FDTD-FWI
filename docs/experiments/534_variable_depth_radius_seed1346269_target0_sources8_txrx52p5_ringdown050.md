# Experiment 534: Seed1346269 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

## Purpose

Run 1000 tests whether Tx/Rx=52.5 can reduce the seed1346269 target0
source-density burden. The older Tx/Rx=60 branch was exact but weak at
8 sources, worsened at 9 sources, and accepted only at 11 sources.

## 1000: Coordinate Optimizer Variable-Depth/Radius Seed1346269 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1000_coordinate_optimizer_variable_depth_radius_seed1346269_target0_sources8_txrx52p5_ringdown050_objectives
```

Command parameters:

```text
backend: gpu-cpml
grid_step_mm: 1.0
sources: 8
tx_rx_offset_mm: 52.5
target_indices: [0]
truth: x=[150,250,350] mm, z=[80,100,120] mm, r=[5,6,8] mm
candidate grid: x_offset=[0], z_offset=[0,1], radius_offset=[0,0.25,0.5,0.75,1.0,1.25]
replication case: source_mismatch_ringdown050_noise10_seed1346269
source profile grid: frequency=[0.9,1.0,1.1], time_shift=[-50,0,50] ps, fitted amplitude and ringdown coefficient
diagnostics: base, highband, late, late_high, veryhigh, early_high
```

## Results

Run 1000 is exact and base-accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.368229e-04
offset from cutoff: +3.682286e-05
confidence label: moderate
fallback warning: none
elapsed: 566.8 s
```

Diagnostic objective margins:

```text
base       5.368229e-04  above cutoff
highband   6.859603e-04  above cutoff
late       3.544509e-04  below cutoff
late_high  3.704226e-04  below cutoff
veryhigh   6.505499e-04  above cutoff
early_high 5.606218e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

Tx/Rx=52.5 rescues seed1346269 target0 at the original 8-source density,
which is a useful reduction from the previous 11-source Tx/Rx=60 accepted
rescue. The late and late_high caveats remain, so this is not a clean
all-objective result; it is a base-confidence rescue with target0 late-window
limitations.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.255449 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target0 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91%; Python process RSS stayed about 459 MB
```

## Next Decision

Run seed1346269 target2 at 5 sources and Tx/Rx=52.5. That run is underway as
experiment 1001.
