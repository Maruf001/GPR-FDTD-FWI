# Experiment 546: Seed5702887 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 1012 continues the seed5702887 branch after the target0 acquisition rescue
settled at Tx/Rx=45. It tests the standard target2 5-source Tx/Rx=60 control.

## 1012: Coordinate Optimizer Variable-Depth/Radius Seed5702887 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1012_coordinate_optimizer_variable_depth_radius_seed5702887_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1012 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 4.419153e-04
offset from cutoff: -5.580847e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 366.3 s
```

Diagnostic objective margins:

```text
base       4.419153e-04  below cutoff by 5.580847e-05
highband   5.267590e-04  above cutoff
late       7.308583e-04  above cutoff
late_high  7.228504e-04  above cutoff
veryhigh   5.707074e-04  above cutoff
early_high 4.071192e-04  below cutoff by 9.288083e-05
```

All six objective variants rank the true target2 geometry first.

## Interpretation

Seed5702887 target2 is truth-preserving at 5 sources and Tx/Rx=60, but base
confidence is too weak to accept. The late-window and high-band objectives
clear cutoff, while base and early_high are below. This matches the pattern
where target2 needs source-density support rather than an immediate acquisition
offset change.

Run a 7-source Tx/Rx=60 target2 rescue before considering 9 sources.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.214649 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target2 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88%; nvidia-smi process memory was about 252 MiB
```

## Next Decision

Run seed5702887 target2 with 7 sources and Tx/Rx=60. That rescue is underway
as experiment 1013.
