# Experiment 541: Seed3524578 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 1007 completes the seed3524578 target-specific branch by testing the
center target under the original 5-source Tx/Rx=60 acquisition. Runs 1004 and
1006 already established target0 and target2 for this seed.

## 1007: Coordinate Optimizer Variable-Depth/Radius Seed3524578 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1007_coordinate_optimizer_variable_depth_radius_seed3524578_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1007 is exact and cleanly accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.523984e-04
offset from cutoff: +5.239845e-05
confidence label: moderate
fallback warning: none
elapsed: 364.4 s
```

Diagnostic objective margins:

```text
base       5.523984e-04  above cutoff
highband   7.098408e-04  above cutoff
late       8.427641e-04  above cutoff
late_high  9.006698e-04  above cutoff
veryhigh   6.802116e-04  above cutoff
early_high 5.254032e-04  above cutoff
```

All six objective variants rank the true target1 geometry first.

## Interpretation

Seed3524578 target1 is clean at the original 5-source Tx/Rx=60 control. With
target0 also clean in run 1004 and target2 base-accepted in run 1006, the
seed3524578 branch does not need a source-density or acquisition-offset rescue.
The only branch caveat is target2 early_high, which was just below cutoff while
still truth-preserving.

Continue the Fibonacci replication chain with seed5702887 target0 at the
standard 8-source Tx/Rx=60 control. Do not create a separate summary output
folder for seed3524578 unless later cross-seed aggregation needs one.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.262412 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target1 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 89%; nvidia-smi process memory was about 252 MiB
```

## Next Decision

Run seed5702887 target0 at 8 sources and Tx/Rx=60. That run is underway as
experiment 1008.
