# Experiment 660: Seed365435296162 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Complete seed365435296162 after target0 was accepted through the Tx/Rx=45
acquisition bracket and target2 passed cleanly at the standard 5-source
control. This run tests target1 at the standard 5-source Tx/Rx=60 control under
the ringdown050 source-mismatch/noise condition.

## 1125: Coordinate Optimizer Variable-Depth/Radius Seed365435296162 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1125_coordinate_optimizer_variable_depth_radius_seed365435296162_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1125 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 6.082031e-04
offset from cutoff: +1.082031e-04
relative margin: 3.655031e-02
confidence label: moderate
fallback warning: none
best misfit: 1.664016e-02
next radius misfit: 1.724836e-02
```

Diagnostic objective margins:

```text
base       6.082031e-04  above cutoff
highband   7.777807e-04  above cutoff
late       8.886857e-04  above cutoff
late_high  1.031138e-03  above cutoff
veryhigh   7.057789e-04  above cutoff
early_high 5.883280e-04  above cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
distinct-radius competitor is `r=6.25 mm`; the closest changed-geometry
competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

Target1 passes cleanly at the standard 5-source Tx/Rx=60 control. This closes
seed365435296162:

```text
target0: accepted at 8 sources, Tx/Rx=45, with residual late-window caveat
target2: accepted at 5 sources, Tx/Rx=60, clean across all objective variants
target1: accepted at 5 sources, Tx/Rx=60, clean across all objective variants
```

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png unique=338 nonwhite_fraction=0.3884
figure validation: coordinate_radius_decision_panel.png unique=860 nonwhite_fraction=0.1797
figure validation: coordinate_objective_radius_candidates.png unique=3016 nonwhite_fraction=0.0680
figure validation: system_scene_geometry.png unique=2048 nonwhite_fraction=0.6306
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in about 378 s
```

## Next Decision

Continue the Fibonacci replication chain with seed591286729879 target0. Seed
validation succeeded in the active FNO environment:

```text
np.random.default_rng(591286729879) succeeded
```
