# Experiment 678: Seed2504730781961 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Continue seed2504730781961 after target0 was accepted by the 9-source Tx/Rx=60
source-density rescue. This run tests target2 at the standard 5-source Tx/Rx=60
control under the ringdown050 source-mismatch/noise condition.

## 1141: Coordinate Optimizer Variable-Depth/Radius Seed2504730781961 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1141_coordinate_optimizer_variable_depth_radius_seed2504730781961_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1141 is exact and accepted, with an early_high diagnostic caveat:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.506970e-04
offset from cutoff: +5.069697e-05
relative margin: 3.293619e-02
confidence label: moderate
fallback warning: none
best misfit: 1.672012e-02
next radius misfit: 1.727082e-02
elapsed: 365.9 s
```

Diagnostic objective margins:

```text
base       5.506970e-04  above cutoff
highband   6.583843e-04  above cutoff
late       8.112186e-04  above cutoff
late_high  8.206967e-04  above cutoff
veryhigh   7.216689e-04  above cutoff
early_high 4.800605e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
distinct-radius and changed-geometry competitor is `r=8.75 mm` at `z=121 mm`.

## Interpretation

Target2 passes the standard 5-source Tx/Rx=60 control. Early_high is weak, but
the base row clears with useful reserve and all diagnostic objectives preserve
the true geometry. No target2 source-density rescue is justified. Continue
seed2504730781961 with target1 at the standard 5-source Tx/Rx=60 control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3528 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1916 and unique_colors=867
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and unique_colors=2990
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6308 and unique_colors=2080
figure notes: figures/FIGURE_NOTES.md present, lists early_high below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 365.9 s through the candidate sweep
```

## Next Decision

Run seed2504730781961 target1 with 5 sources and Tx/Rx=60. If target1 clears,
the seed closes with target0 rescued by 9-source Tx/Rx=60, target2 accepted at
the standard control with an early_high caveat, and target1 decided by its
control row.
