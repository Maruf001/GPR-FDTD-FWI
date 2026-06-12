# Experiment 542: Seed5702887 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Run 1008 starts the seed5702887 Fibonacci branch with the original target0
control: 8 sources and Tx/Rx=60 under the full ringdown050 source-mismatch
case.

## 1008: Coordinate Optimizer Variable-Depth/Radius Seed5702887 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1008_coordinate_optimizer_variable_depth_radius_seed5702887_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1008 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 4.694809e-04
offset from cutoff: -3.051911e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 578.2 s
```

Diagnostic objective margins:

```text
base       4.694809e-04  below cutoff by 3.051911e-05
highband   6.002317e-04  above cutoff
late       3.740456e-04  below cutoff by 1.259544e-04
late_high  3.925767e-04  below cutoff by 1.074233e-04
veryhigh   5.450284e-04  above cutoff
early_high 4.982299e-04  below cutoff by 1.770123e-06
```

All six objective variants rank the true target0 geometry first.

## Interpretation

Seed5702887 target0 is truth-preserving at the original 8-source Tx/Rx=60
control, but it is not accepted by the working confidence rule. The weak rows
are concentrated in base and late-window objectives; highband and veryhigh
remain above cutoff. This resembles the target0 acquisition sensitivity seen
in seed1346269 more than a geometry-localization failure.

The next test should therefore use the recently validated target0 acquisition
remedy first: keep 8 sources and reduce Tx/Rx to 52.5 mm. If that fails, then
escalate source density.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.226380 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target0 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91-92%; nvidia-smi process memory was about 294 MiB
```

## Next Decision

Run seed5702887 target0 with 8 sources and Tx/Rx=52.5. That rescue is underway
as experiment 1009.
