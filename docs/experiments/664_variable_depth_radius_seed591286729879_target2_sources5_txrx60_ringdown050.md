# Experiment 664: Seed591286729879 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Continue seed591286729879 after target0 accepted at the 8-source Tx/Rx=60
control with the recurring late-window caveat. This run tests target2 at the
standard 5-source Tx/Rx=60 control under the ringdown050 source-mismatch/noise
condition.

## 1127: Coordinate Optimizer Variable-Depth/Radius Seed591286729879 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1127_coordinate_optimizer_variable_depth_radius_seed591286729879_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1127 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.552969e-04
offset from cutoff: +5.529693e-05
relative margin: 3.261177e-02
confidence label: moderate
fallback warning: none
best misfit: 1.702750e-02
next radius misfit: 1.758280e-02
elapsed: 392.5 s
```

Diagnostic objective margins:

```text
base       5.552969e-04  above cutoff
highband   7.039478e-04  above cutoff
late       8.725430e-04  above cutoff
late_high  9.404163e-04  above cutoff
veryhigh   7.314076e-04  above cutoff
early_high 5.038796e-04  above cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
distinct-radius competitor is `r=8.75 mm`; the closest changed-geometry
competitor is `r=8.75 mm` at `z=121 mm`.

## Interpretation

Target2 passes at the standard 5-source Tx/Rx=60 control. Even the weakest
diagnostic objective, early_high, clears the cutoff by a small positive
reserve. No target2 rescue is justified.

Continue seed591286729879 with target1 at the standard 5-source Tx/Rx=60
control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3581 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1877 and unique_colors=874
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and unique_colors=2990
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6306 and unique_colors=2081
figure notes: figures/FIGURE_NOTES.md present, lists no objective variants below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88%; run completed in 392.5 s
```

## Next Decision

Continue seed591286729879 with target1 at the standard 5-source Tx/Rx=60
control under the same ringdown050 objective suite.
