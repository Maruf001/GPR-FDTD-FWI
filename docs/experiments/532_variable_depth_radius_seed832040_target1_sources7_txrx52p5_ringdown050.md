# Experiment 532: Seed832040 Target1 Sources=7 Tx/Rx=52.5 Ringdown050

## Purpose

Run 998 tests whether combining the best 5-source acquisition offset
(Tx/Rx=52.5) with intermediate source density can rescue seed832040 target1
without returning all the way to the known 9-source Tx/Rx=60 rescue.

## 998: Coordinate Optimizer Variable-Depth/Radius Seed832040 Target1 Sources=7 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/998_coordinate_optimizer_variable_depth_radius_seed832040_target1_sources7_txrx52p5_ringdown050_objectives
```

Command parameters:

```text
backend: gpu-cpml
grid_step_mm: 1.0
sources: 7
tx_rx_offset_mm: 52.5
target_indices: [1]
truth: x=[150,250,350] mm, z=[80,100,120] mm, r=[5,6,8] mm
candidate grid: x_offset=[0], z_offset=[0,1], radius_offset=[0,0.25,0.5,0.75,1.0,1.25]
replication case: source_mismatch_ringdown050_noise10_seed832040
source profile grid: frequency=[0.9,1.0,1.1], time_shift=[-50,0,50] ps, fitted amplitude and ringdown coefficient
diagnostics: base, highband, late, late_high, veryhigh, early_high
```

## Results

Run 998 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 4.382708e-04
offset from cutoff: -6.172919e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 483.7 s
```

Diagnostic objective margins:

```text
base       4.382708e-04  below cutoff
highband   6.076125e-04  above cutoff
late       6.895040e-04  above cutoff
late_high  6.760421e-04  above cutoff
veryhigh   6.307246e-04  above cutoff
early_high 4.175502e-04  below cutoff
```

All six objective variants rank the true target1 geometry first.

## Interpretation

The 7-source combined policy is a partial improvement: it lifts veryhigh above
cutoff and improves the base margin over the 5-source rows, but base and
early_high remain below cutoff. This is not enough to replace the old
9-source rescue. Run 9 sources at Tx/Rx=52.5 to compare the best offset
against the known 9-source Tx/Rx=60 accepted row.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.214816 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target1 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and identifies the weak target1 row
metadata validation: tx_rx_offset_mm is 52.5; sources=7; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90%; Python process RSS stayed about 457 MB
```

## Next Decision

Run seed832040 target1 with 9 sources at Tx/Rx=52.5. That run is underway as
experiment 999.
