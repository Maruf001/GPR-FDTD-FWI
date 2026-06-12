# Experiment 530: Seed832040 Target1 Sources=5 Tx/Rx=50 Ringdown050

## Purpose

Run 996 checks the lower side of the seed832040 target1 acquisition-offset
bracket after run 995 showed Tx/Rx=52.5 was exact but still weak.

## 996: Coordinate Optimizer Variable-Depth/Radius Seed832040 Target1 Sources=5 Tx/Rx=50 Ringdown050

Output:

```text
outputs/experiments/996_coordinate_optimizer_variable_depth_radius_seed832040_target1_sources5_txrx50_ringdown050_objectives
```

Command parameters:

```text
backend: gpu-cpml
grid_step_mm: 1.0
sources: 5
tx_rx_offset_mm: 50.0
target_indices: [1]
truth: x=[150,250,350] mm, z=[80,100,120] mm, r=[5,6,8] mm
candidate grid: x_offset=[0], z_offset=[0,1], radius_offset=[0,0.25,0.5,0.75,1.0,1.25]
replication case: source_mismatch_ringdown050_noise10_seed832040
source profile grid: frequency=[0.9,1.0,1.1], time_shift=[-50,0,50] ps, fitted amplitude and ringdown coefficient
diagnostics: base, highband, late, late_high, veryhigh, early_high
```

## Results

Run 996 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 4.148734e-04
offset from cutoff: -8.512663e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 363.1 s
```

Diagnostic objective margins:

```text
base       4.148734e-04  below cutoff
highband   5.952892e-04  above cutoff
late       6.316186e-04  above cutoff
late_high  7.459229e-04  above cutoff
veryhigh   4.590186e-04  below cutoff
early_high 4.216078e-04  below cutoff
```

All six objective variants rank the true target1 geometry first.

## Interpretation

Tx/Rx=50 is not the seed832040 acquisition remedy. It is slightly worse than
Tx/Rx=52.5, which suggests the seed832040 target1 5-source offset response is
not simply shifted lower. Continue with Tx/Rx=55 to complete the 50-55 mm
bracket before summarizing the acquisition-only result.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.204899 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target1 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and identifies the weak target1 row
metadata validation: tx_rx_offset_mm is 50.0; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88%; Python process RSS stayed about 451 MB
```

## Next Decision

Run seed832040 target1 at Tx/Rx=55 with 5 sources. That run is underway as
experiment 997.
