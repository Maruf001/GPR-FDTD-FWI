# Experiment 693: Seed17167680207565 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run the standard target2 5-source Tx/Rx=60 control for seed17167680207565 after
target0 was accepted with the recurring late-window caveat.

## 1156: Coordinate Optimizer Variable-Depth/Radius Seed17167680207565 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1156_coordinate_optimizer_variable_depth_radius_seed17167680207565_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1156 selected the exact geometry but remains below the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 4.571020e-04
offset from cutoff: -4.289797e-05
relative margin: 2.623308e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.742464e-02
next radius misfit: 1.788174e-02
elapsed: 382.8 s
```

Diagnostic objective margins:

```text
base       4.571020e-04  below cutoff
highband   5.690417e-04  above cutoff
late       6.846390e-04  above cutoff
late_high  7.196203e-04  above cutoff
veryhigh   6.031128e-04  above cutoff
early_high 4.573551e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
base objective distinct-radius and changed-geometry competitor is `r=8.75 mm`
at `z=121 mm`.

## Interpretation

This is not a geometry failure: every diagnostic objective selects the true
target2 radius/depth. It is a radius-confidence failure in the base and
early_high windows. Follow the current target2 weak-control policy by adding a
7-source Tx/Rx=60 source-density bracket before deciding whether a 9-source
escalation is needed.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.2972 and sampled_unique_colors=228
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1841 and sampled_unique_colors=376
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and sampled_unique_colors=1148
figure validation: system_scene_geometry.png is 1768x1065 RGB with nonwhite_fraction=0.6338 and sampled_unique_colors=1068
figure notes: figures/FIGURE_NOTES.md present, reports one weak row and lists base and early_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 382.8 s through the candidate sweep
```

## Next Decision

Run seed17167680207565 target2 with 7 sources and Tx/Rx=60 as the
source-density bracket.
