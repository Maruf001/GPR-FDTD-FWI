# Experiment 540: Seed3524578 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 1006 continues the seed3524578 Fibonacci branch after the clean target0
control. It tests whether the original 5-source Tx/Rx=60 acquisition is enough
for the deep, large-radius target2 under the full ringdown050 source-mismatch
case.

## 1006: Coordinate Optimizer Variable-Depth/Radius Seed3524578 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1006_coordinate_optimizer_variable_depth_radius_seed3524578_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1006 is exact and base-accepted, with a narrow early_high diagnostic
caveat:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.691824e-04
offset from cutoff: +6.918241e-05
confidence label: moderate
fallback warning: none
elapsed: 367.1 s
```

Diagnostic objective margins:

```text
base       5.691824e-04  above cutoff
highband   6.895847e-04  above cutoff
late       8.693891e-04  above cutoff
late_high  8.982087e-04  above cutoff
veryhigh   6.876029e-04  above cutoff
early_high 4.897265e-04  below cutoff by 1.027346e-05
```

All six objective variants rank the true target2 geometry first.

## Interpretation

Seed3524578 target2 does not need an immediate source-density rescue for base
confidence. The base margin clears the working 5.0e-4 cutoff by 6.92e-05, and
the late and high-band diagnostics are stronger than base. The only deficit is
the early_high diagnostic, which is just below cutoff while still selecting the
true radius first. Carry this as an early-window robustness caveat and continue
the branch with the standard target1 5-source Tx/Rx=60 control.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.269636 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target2 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88-89%; nvidia-smi process memory was about 252 MiB
```

## Next Decision

Run seed3524578 target1 at 5 sources and Tx/Rx=60. That run is underway as
experiment 1007.
