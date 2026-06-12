# Experiment 696: Seed17167680207565 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run the standard target1 5-source Tx/Rx=60 control for seed17167680207565 after
target0 was accepted and target2 was rescued by a 9-source escalation.

## 1159: Coordinate Optimizer Variable-Depth/Radius Seed17167680207565 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1159_coordinate_optimizer_variable_depth_radius_seed17167680207565_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1159 selected the exact geometry but remains below the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 4.758491e-04
offset from cutoff: -2.415094e-05
relative margin: 2.730898e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.742464e-02
next radius misfit: 1.790049e-02
elapsed: 380.6 s
```

Diagnostic objective margins:

```text
base       4.758491e-04  below cutoff
highband   5.987892e-04  above cutoff
late       7.513600e-04  above cutoff
late_high  8.035913e-04  above cutoff
veryhigh   6.136803e-04  above cutoff
early_high 4.440855e-04  below cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
base objective distinct-radius competitor is `r=6.25 mm` at the same depth,
and the closest changed-geometry competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

This is the recurring target1 weak-control pattern: exact geometry and
truth-ranked diagnostics, but base and early_high remain below cutoff. The
latest comparable branch, seed139583862445, used a 9-source Tx/Rx=60 target1
rescue rather than the older Tx/Rx=52.5 acquisition rescue. Follow that
current policy before closing the seed.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3076 and sampled_unique_colors=227
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1668 and sampled_unique_colors=370
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and sampled_unique_colors=1148
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6338 and sampled_unique_colors=1044
figure notes: figures/FIGURE_NOTES.md present, reports one weak row and lists base and early_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 380.6 s through the candidate sweep
```

## Next Decision

Run seed17167680207565 target1 with 9 sources and Tx/Rx=60 as the established
target1 rescue.
