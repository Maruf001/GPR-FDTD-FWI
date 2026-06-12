# Experiment 692: Seed17167680207565 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Start the seed17167680207565 Fibonacci replication branch with the standard
target0 8-source Tx/Rx=60 control.

## 1155: Coordinate Optimizer Variable-Depth/Radius Seed17167680207565 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1155_coordinate_optimizer_variable_depth_radius_seed17167680207565_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1155 selected the exact geometry and clears the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.455539e-04
offset from cutoff: +4.555391e-05
relative margin: 3.392439e-02
confidence label: moderate
fallback warning: none
best misfit: 1.608147e-02
next radius misfit: 1.662702e-02
elapsed: 572.4 s
```

Diagnostic objective margins:

```text
base       5.455539e-04  above cutoff
highband   6.911404e-04  above cutoff
late       4.563285e-04  below cutoff
late_high  4.782245e-04  below cutoff
veryhigh   6.333735e-04  above cutoff
early_high 5.793051e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
base objective distinct-radius competitor is `r=5.25 mm` at the same depth,
and the closest changed-geometry competitor is `r=6.0 mm` at `z=81 mm`.

## Interpretation

This is an accepted target0 result with the recurring late-window caveat. The
base, highband, veryhigh, and early_high objectives clear cutoff and all
objectives agree on the true radius/depth, so no rescue branch is justified.
Carry the weak late and late_high diagnostics as a robustness caveat for this
seed, then continue to target2.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3472 and sampled_unique_colors=289
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1848 and sampled_unique_colors=380
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and sampled_unique_colors=1165
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6336 and sampled_unique_colors=1109
figure notes: figures/FIGURE_NOTES.md present, reports one moderate row and lists late and late_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 572.4 s through the candidate sweep
```

## Next Decision

Continue seed17167680207565 with target2 at the standard 5-source Tx/Rx=60
control.
