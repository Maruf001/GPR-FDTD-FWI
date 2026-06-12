# Experiment 537: Seed1346269 Target1 Sources=5 Tx/Rx=52.5 Ringdown050

## Purpose

Run 1003 checks whether the Tx/Rx=52.5 acquisition offset harms seed1346269
target1 after target0 improved at Tx/Rx=52.5 and target2 preferred a
7-source Tx/Rx=60 rescue.

## 1003: Coordinate Optimizer Variable-Depth/Radius Seed1346269 Target1 Sources=5 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1003_coordinate_optimizer_variable_depth_radius_seed1346269_target1_sources5_txrx52p5_ringdown050_objectives
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
replication case: source_mismatch_ringdown050_noise10_seed1346269
source profile grid: frequency=[0.9,1.0,1.1], time_shift=[-50,0,50] ps, fitted amplitude and ringdown coefficient
diagnostics: base, highband, late, late_high, veryhigh, early_high
```

## Results

Run 1003 is exact and cleanly accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.426894e-04
offset from cutoff: +4.268941e-05
confidence label: moderate
fallback warning: none
elapsed: 364.9 s
```

Diagnostic objective margins:

```text
base       5.426894e-04  above cutoff
highband   7.298336e-04  above cutoff
late       8.781591e-04  above cutoff
late_high  9.868196e-04  above cutoff
veryhigh   6.755558e-04  above cutoff
early_high 5.066088e-04  above cutoff
```

All six objective variants rank the true target1 geometry first.

## Interpretation

Tx/Rx=52.5 is safe for seed1346269 target1. This gives a clean target1 row
for the revised seed1346269 policy summary, while target0 remains
base-accepted with late-window caveats and target2 is better handled by
7-source Tx/Rx=60.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.258135 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target1 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88%; Python process RSS stayed about 452 MB
```

## Next Decision

Build the revised seed1346269 policy summary while experiment 1004 starts the
next Fibonacci seed branch.
