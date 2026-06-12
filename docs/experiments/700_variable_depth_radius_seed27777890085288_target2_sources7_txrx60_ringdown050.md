# Experiment 700: Seed27777890085288 Target2 Sources=7 Tx/Rx=60 Ringdown050

## Purpose

Run the seed27777890085288 target2 7-source Tx/Rx=60 source-density bracket
after the 5-source control was an exact near miss below cutoff.

## 1163: Coordinate Optimizer Variable-Depth/Radius Seed27777890085288 Target2 Sources=7 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1163_coordinate_optimizer_variable_depth_radius_seed27777890085288_target2_sources7_txrx60_ringdown050_objectives
```

## Results

Run 1163 selected the exact geometry but remains weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 7
tx_rx_offset_mm: 60.0
absolute radius margin: 4.867230e-04
offset from cutoff: -1.327699e-05
relative margin: 3.289315e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.479709e-02
next radius misfit: 1.528381e-02
elapsed: 511.8 s
```

Diagnostic objective margins:

```text
base       4.867230e-04  below cutoff
highband   6.434465e-04  above cutoff
late       7.188731e-04  above cutoff
late_high  7.943807e-04  above cutoff
veryhigh   6.432257e-04  above cutoff
early_high 4.102825e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
base objective distinct-radius and changed-geometry competitor remains
`r=8.75 mm` at `z=121 mm`.

## Interpretation

The 7-source bracket improves the objective gap relative to the lower-margin
tail of recent target2 weak controls, but it still does not clear cutoff:

```text
5 sources, Tx/Rx=60  base margin 4.980e-04
7 sources, Tx/Rx=60  base margin 4.867e-04
```

Because the geometry is still exact and every objective variant ranks the true
target2 geometry first, continue to the standard 9-source Tx/Rx=60 target2
escalation.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3141 and sampled_unique_colors=227
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1627 and sampled_unique_colors=379
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and sampled_unique_colors=1148
figure validation: system_scene_geometry.png is 1768x1065 RGB with nonwhite_fraction=0.6338 and sampled_unique_colors=1077
figure notes: figures/FIGURE_NOTES.md present, reports one weak row and lists base and early_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=7; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 511.8 s through the candidate sweep
```

## Next Decision

Run seed27777890085288 target2 with 9 sources and Tx/Rx=60 as the standard
target2 source-density escalation.
