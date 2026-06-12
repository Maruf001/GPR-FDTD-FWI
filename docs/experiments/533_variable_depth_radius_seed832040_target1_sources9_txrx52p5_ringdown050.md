# Experiment 533: Seed832040 Target1 Sources=9 Tx/Rx=52.5 Ringdown050

## Purpose

Run 999 tests the accepted combined-policy endpoint for seed832040 target1:
9 sources at the best acquisition offset, Tx/Rx=52.5. The comparison row is
the earlier accepted 9-source Tx/Rx=60 rescue from run 971.

## 999: Coordinate Optimizer Variable-Depth/Radius Seed832040 Target1 Sources=9 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/999_coordinate_optimizer_variable_depth_radius_seed832040_target1_sources9_txrx52p5_ringdown050_objectives
```

Command parameters:

```text
backend: gpu-cpml
grid_step_mm: 1.0
sources: 9
tx_rx_offset_mm: 52.5
target_indices: [1]
truth: x=[150,250,350] mm, z=[80,100,120] mm, r=[5,6,8] mm
candidate grid: x_offset=[0], z_offset=[0,1], radius_offset=[0,0.25,0.5,0.75,1.0,1.25]
replication case: source_mismatch_ringdown050_noise10_seed832040
source profile grid: frequency=[0.9,1.0,1.1], time_shift=[-50,0,50] ps, fitted amplitude and ringdown coefficient
diagnostics: base, highband, late, late_high, veryhigh, early_high
```

## Results

Run 999 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.297020e-04
offset from cutoff: +2.970198e-05
confidence label: moderate
fallback warning: none
elapsed: 659.2 s
```

Diagnostic objective margins:

```text
base       5.297020e-04  above cutoff
highband   7.444354e-04  above cutoff
late       7.673499e-04  above cutoff
late_high  9.440353e-04  above cutoff
veryhigh   6.066043e-04  above cutoff
early_high 5.358135e-04  above cutoff
```

All six objective variants rank the true target1 geometry first.

## Interpretation

Tx/Rx=52.5 improves the accepted 9-source seed832040 target1 rescue. The
5-source acquisition-only bracket was insufficient, and 7 sources were a
partial rescue, but 9 sources at Tx/Rx=52.5 cleanly clears all diagnostic
objectives and improves the base reserve over the older 9-source Tx/Rx=60 row.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.255384 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target1 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91-92%; Python process RSS stayed about 462 MB
```

## Next Decision

Move the Tx/Rx=52.5 policy to seed1346269 target0, where the Tx/Rx=60 branch
needed escalation from 8 to 11 sources. That run is underway as experiment
1000.
