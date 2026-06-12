# Experiment 688: Seed10610209877723 Target2 Sources=7 Tx/Rx=60 Ringdown050

## Purpose

Run the first target2 source-density bracket for seed10610209877723 after the
5-source Tx/Rx=60 control selected the exact geometry but remained weak. This
run increases source count to 7 while keeping Tx/Rx=60.

## 1151: Coordinate Optimizer Variable-Depth/Radius Seed10610209877723 Target2 Sources=7 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1151_coordinate_optimizer_variable_depth_radius_seed10610209877723_target2_sources7_txrx60_ringdown050_objectives
```

## Results

Run 1151 selected the exact geometry but did not rescue target2:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 7
tx_rx_offset_mm: 60.0
absolute radius margin: 4.449196e-04
offset from cutoff: -5.508040e-05
relative margin: 2.985661e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.490188e-02
next radius misfit: 1.534680e-02
elapsed: 517.9 s
```

Diagnostic objective margins:

```text
base       4.449196e-04  below cutoff
highband   5.706443e-04  above cutoff
late       6.563621e-04  above cutoff
late_high  7.332194e-04  above cutoff
veryhigh   5.608779e-04  above cutoff
early_high 3.655641e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
distinct-radius and changed-geometry competitor is `r=8.75 mm` at `z=121 mm`.

## Interpretation

The 7-source bracket preserves the true geometry but weakens the base margin
relative to the 5-source control:

```text
5 sources, Tx/Rx=60  base margin 4.719e-04
7 sources, Tx/Rx=60  base margin 4.449e-04
```

Since source density has not yet been tested at the accepted 9-source level
for target2, continue to the standard 9-source Tx/Rx=60 escalation before
deciding whether this target is unresolved or needs a different mechanism.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.2899 and unique_colors=233
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1839 and unique_colors=857
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and unique_colors=2990
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6338 and unique_colors=2065
figure notes: figures/FIGURE_NOTES.md present, lists base and early_high below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=7; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 517.9 s through the candidate sweep
```

## Next Decision

Run seed10610209877723 target2 with 9 sources and Tx/Rx=60. If that row also
remains weak, compare it against the 5- and 7-source rows before deciding
whether an 11-source closeout or a different acquisition mechanism is justified.
