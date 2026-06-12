# Experiment 694: Seed17167680207565 Target2 Sources=7 Tx/Rx=60 Ringdown050

## Purpose

Run the seed17167680207565 target2 7-source Tx/Rx=60 source-density bracket
after the 5-source control selected the exact geometry but remained weak.

## 1157: Coordinate Optimizer Variable-Depth/Radius Seed17167680207565 Target2 Sources=7 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1157_coordinate_optimizer_variable_depth_radius_seed17167680207565_target2_sources7_txrx60_ringdown050_objectives
```

## Results

Run 1157 selected the exact geometry but remains weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 7
tx_rx_offset_mm: 60.0
absolute radius margin: 4.380199e-04
offset from cutoff: -6.198013e-05
relative margin: 2.907613e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.506459e-02
next radius misfit: 1.550261e-02
elapsed: 505.0 s
```

Diagnostic objective margins:

```text
base       4.380199e-04  below cutoff
highband   5.705941e-04  above cutoff
late       6.128536e-04  above cutoff
late_high  7.306987e-04  above cutoff
veryhigh   5.898627e-04  above cutoff
early_high 3.865781e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
base objective distinct-radius and changed-geometry competitor remains
`r=8.75 mm` at `z=121 mm`.

## Interpretation

The 7-source bracket did not improve the base margin:

```text
5 sources, Tx/Rx=60  base margin 4.571e-04
7 sources, Tx/Rx=60  base margin 4.380e-04
```

Because this is still exact geometry and all objective variants agree on the
true target2 radius/depth, proceed to the established 9-source Tx/Rx=60
target2 escalation before deciding whether this seed needs an 11-source
closeout or can be accepted.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.2859 and sampled_unique_colors=228
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1881 and sampled_unique_colors=377
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and sampled_unique_colors=1148
figure validation: system_scene_geometry.png is 1768x1065 RGB with nonwhite_fraction=0.6337 and sampled_unique_colors=1078
figure notes: figures/FIGURE_NOTES.md present, reports one weak row and lists base and early_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=7; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 505.0 s through the candidate sweep
```

## Next Decision

Run seed17167680207565 target2 with 9 sources and Tx/Rx=60 as the standard
target2 source-density escalation.
