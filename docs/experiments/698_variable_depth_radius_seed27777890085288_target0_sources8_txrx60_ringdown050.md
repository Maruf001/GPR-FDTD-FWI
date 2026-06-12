# Experiment 698: Seed27777890085288 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Start the seed27777890085288 Fibonacci replication branch with the standard
target0 8-source Tx/Rx=60 control.

## 1161: Coordinate Optimizer Variable-Depth/Radius Seed27777890085288 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1161_coordinate_optimizer_variable_depth_radius_seed27777890085288_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1161 selected the exact geometry and clears the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.578823e-04
offset from cutoff: +5.788231e-05
relative margin: 3.511539e-02
confidence label: moderate
fallback warning: none
best misfit: 1.588712e-02
next radius misfit: 1.644500e-02
elapsed: 585.7 s
```

Diagnostic objective margins:

```text
base       5.578823e-04  above cutoff
highband   7.151789e-04  above cutoff
late       3.694475e-04  below cutoff
late_high  4.322151e-04  below cutoff
veryhigh   6.580522e-04  above cutoff
early_high 5.987721e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
base objective distinct-radius competitor is `r=5.25 mm` at the same depth,
and the closest changed-geometry competitor is `r=6.0 mm` at `z=81 mm`.

## Interpretation

This is an accepted target0 result with the recurring late-window caveat. The
base, highband, veryhigh, and early_high objectives clear cutoff and all
objectives rank the true radius/depth first, so no target0 rescue branch is
justified. Continue to target2 at the standard 5-source control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3541 and sampled_unique_colors=289
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1862 and sampled_unique_colors=384
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and sampled_unique_colors=1164
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6337 and sampled_unique_colors=1109
figure notes: figures/FIGURE_NOTES.md present, reports one moderate row and lists late and late_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 585.7 s through the candidate sweep
```

## Next Decision

Continue seed27777890085288 with target2 at the standard 5-source Tx/Rx=60
control.
