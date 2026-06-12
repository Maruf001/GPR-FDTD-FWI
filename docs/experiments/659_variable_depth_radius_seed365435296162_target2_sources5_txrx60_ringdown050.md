# Experiment 659: Seed365435296162 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Continue seed365435296162 after closing target0 through the Tx/Rx=45
acquisition bracket. This run tests target2 at the standard 5-source Tx/Rx=60
control under the ringdown050 source-mismatch/noise condition.

## 1124: Coordinate Optimizer Variable-Depth/Radius Seed365435296162 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1124_coordinate_optimizer_variable_depth_radius_seed365435296162_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1124 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 6.158368e-04
offset from cutoff: +1.158368e-04
relative margin: 3.700907e-02
confidence label: moderate
fallback warning: none
best misfit: 1.664016e-02
next radius misfit: 1.725600e-02
```

Diagnostic objective margins:

```text
base       6.158368e-04  above cutoff
highband   7.610905e-04  above cutoff
late       8.940290e-04  above cutoff
late_high  9.272592e-04  above cutoff
veryhigh   7.768839e-04  above cutoff
early_high 5.477279e-04  above cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
distinct-radius and closest changed-geometry competitor is `r=8.75 mm` at
`z=121 mm`.

## Interpretation

Target2 passes cleanly at the standard 5-source Tx/Rx=60 control. There is no
need for a target2 source-density rescue on this seed. Continue with target1 at
the standard 5-source Tx/Rx=60 control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png unique=338 nonwhite_fraction=0.3928
figure validation: coordinate_radius_decision_panel.png unique=869 nonwhite_fraction=0.1892
figure validation: coordinate_objective_radius_candidates.png unique=2990 nonwhite_fraction=0.0681
figure validation: system_scene_geometry.png unique=2092 nonwhite_fraction=0.6307
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in about 360 s
```

## Next Decision

Run seed365435296162 target1 with 5 sources and Tx/Rx=60 under the same
ringdown050 objective suite.
