# Experiment 527: Seed2178309 Target2 Sources=5 Tx/Rx=52.5 Ringdown050

## Purpose

Run 993 completes the seed2178309 all-target Tx/Rx=52.5 validation by testing
target2 after target1 accepted at Tx/Rx=52.5 in run 991 and target0 accepted
with late-window caveats in run 992.

## 993: Coordinate Optimizer Variable-Depth/Radius Seed2178309 Target2 Sources=5 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/993_coordinate_optimizer_variable_depth_radius_seed2178309_target2_sources5_txrx52p5_ringdown050_objectives
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
replication case: source_mismatch_ringdown050_noise10_seed2178309
source profile grid: frequency=[0.9,1.0,1.1], time_shift=[-50,0,50] ps, fitted amplitude and ringdown coefficient
diagnostics: base, highband, late, late_high, veryhigh, early_high
```

## Results

Run 993 is exact and cleanly accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.993183e-04
offset from cutoff: +9.931829e-05
confidence label: moderate
fallback warning: none
elapsed: 364.7 s
```

Diagnostic objective margins all remain above cutoff:

```text
base       5.993183e-04
highband   7.526021e-04
late       9.518032e-04
late_high  1.012567e-03
veryhigh   8.530113e-04
early_high 5.426424e-04
```

## Interpretation

Target2 is not the limiting seed2178309 case at Tx/Rx=52.5. Unlike target0
and target1, it has no below-cutoff diagnostic caveat. This makes Tx/Rx=52.5
all-target base-accepted for seed2178309: target0 is accepted with late-window
caveats, target1 is accepted with an early_high caveat, and target2 is clean.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.280651 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target2 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization remained about 88-90% during the sweep; Python process RSS stayed about 450 MB
```

## Next Decision

Build the seed2178309 Tx/Rx=52.5 acquisition-policy summary and then test
whether the same offset transfers to seed832040 target1.
