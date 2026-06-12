# Experiment 547: Seed5702887 Target2 Sources=7 Tx/Rx=60 Ringdown050

## Purpose

Run 1013 tests whether a 7-source Tx/Rx=60 source-density rescue fixes the
weak seed5702887 target2 5-source control from run 1012.

## 1013: Coordinate Optimizer Variable-Depth/Radius Seed5702887 Target2 Sources=7 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1013_coordinate_optimizer_variable_depth_radius_seed5702887_target2_sources7_txrx60_ringdown050_objectives
```

## Results

Run 1013 is exact but still weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 7
tx_rx_offset_mm: 60.0
absolute radius margin: 4.329420e-04
offset from cutoff: -6.705798e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 508.4 s
```

Diagnostic objective margins:

```text
base       4.329420e-04  below cutoff by 6.705798e-05
highband   5.771532e-04  above cutoff
late       6.137107e-04  above cutoff
late_high  7.049134e-04  above cutoff
veryhigh   5.882859e-04  above cutoff
early_high 4.008295e-04  below cutoff by 9.917048e-05
```

All six objective variants rank the true target2 geometry first.

## Interpretation

The 7-source rescue does not help seed5702887 target2. It remains
truth-preserving, but the base margin is lower than the 5-source control
(`4.329e-04` versus `4.419e-04`) and early_high is still weak. This makes the
source-density response nonmonotone at 7 sources.

Run a 9-source escalation as the next source-density check. If 9 sources also
fails, stop blind source-density escalation and switch mechanism.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.211043 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target2 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=7; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90%; nvidia-smi process memory was about 280 MiB
```

## Next Decision

Run seed5702887 target2 with 9 sources and Tx/Rx=60. That escalation is
underway as experiment 1014.
