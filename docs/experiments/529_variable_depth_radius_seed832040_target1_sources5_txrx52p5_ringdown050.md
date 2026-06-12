# Experiment 529: Seed832040 Target1 Sources=5 Tx/Rx=52.5 Ringdown050

## Purpose

Run 995 tests cross-seed transfer of the seed2178309 Tx/Rx=52.5 acquisition
remedy. The reference rows are seed832040 target1 run 970, which was exact but
weak at Tx/Rx=60 with 5 sources, and run 971, which accepted after a 9-source
Tx/Rx=60 rescue.

## 995: Coordinate Optimizer Variable-Depth/Radius Seed832040 Target1 Sources=5 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/995_coordinate_optimizer_variable_depth_radius_seed832040_target1_sources5_txrx52p5_ringdown050_objectives
```

Command parameters:

```text
backend: gpu-cpml
grid_step_mm: 1.0
sources: 5
tx_rx_offset_mm: 52.5
target_indices: [1]
truth: x=[150,250,350] mm, z=[80,100,120] mm, r=[5,6,8] mm
candidate grid: x_offset=[0], z_offset=[0,1], radius_offset=[0,0.25,0.5,0.75,1.0,1.25]
replication case: source_mismatch_ringdown050_noise10_seed832040
source profile grid: frequency=[0.9,1.0,1.1], time_shift=[-50,0,50] ps, fitted amplitude and ringdown coefficient
diagnostics: base, highband, late, late_high, veryhigh, early_high
```

## Results

Run 995 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 4.179126e-04
offset from cutoff: -8.208735e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 360.4 s
```

Diagnostic objective margins:

```text
base       4.179126e-04  below cutoff
highband   5.988723e-04  above cutoff
late       6.464372e-04  above cutoff
late_high  7.650855e-04  above cutoff
veryhigh   4.625860e-04  below cutoff
early_high 4.271741e-04  below cutoff
```

All six objective variants rank the true target1 geometry first.

## Interpretation

Tx/Rx=52.5 improves on the old Tx/Rx=60 5-source control, but seed832040
target1 remains below cutoff. This means the seed2178309 52.5 mm remedy is
not directly transferable as a full replacement for seed832040's 9-source
rescue. Because the margin moved in the right direction when offset was
reduced, continue the bracket with Tx/Rx=50 rather than returning immediately
to source-density escalation.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.205801 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target1 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and identifies the weak target1 row
metadata validation: tx_rx_offset_mm is 52.5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88%; Python process RSS stayed about 455 MB
```

## Next Decision

Run seed832040 target1 at Tx/Rx=50 with 5 sources. That run is underway as
experiment 996.
