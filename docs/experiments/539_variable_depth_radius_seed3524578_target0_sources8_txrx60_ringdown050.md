# Experiment 539: Seed3524578 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Run 1004 starts the seed3524578 branch with the standard target0 8-source
Tx/Rx=60 control.

## 1004: Coordinate Optimizer Variable-Depth/Radius Seed3524578 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1004_coordinate_optimizer_variable_depth_radius_seed3524578_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1004 is exact and cleanly accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.715416e-04
offset from cutoff: +7.154162e-05
confidence label: moderate
fallback warning: none
elapsed: 564.3 s
```

Diagnostic objective margins:

```text
base       5.715416e-04  above cutoff
highband   7.365595e-04  above cutoff
late       5.389051e-04  above cutoff
late_high  5.847707e-04  above cutoff
veryhigh   7.241039e-04  above cutoff
early_high 6.250021e-04  above cutoff
```

## Interpretation

Seed3524578 target0 is clean at the standard control. Continue with target2 at
5 sources and Tx/Rx=60.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.269846 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target0 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91%; Python process RSS stayed about 458 MB
```

## Next Decision

Run seed3524578 target2 at 5 sources and Tx/Rx=60. That run is underway as
experiment 1006.
