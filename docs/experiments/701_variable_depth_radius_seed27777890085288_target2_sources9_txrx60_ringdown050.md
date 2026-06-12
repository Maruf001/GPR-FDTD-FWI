# Experiment 701: Seed27777890085288 Target2 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Escalate seed27777890085288 target2 to the standard 9-source Tx/Rx=60
source-density level after 5- and 7-source runs selected the exact geometry
but remained weak.

## 1164: Coordinate Optimizer Variable-Depth/Radius Seed27777890085288 Target2 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1164_coordinate_optimizer_variable_depth_radius_seed27777890085288_target2_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1164 selected the exact geometry and clears the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 5.354413e-04
offset from cutoff: +3.544133e-05
relative margin: 3.390504e-02
confidence label: moderate
fallback warning: none
best misfit: 1.579238e-02
next radius misfit: 1.632782e-02
elapsed: 672.5 s
```

Diagnostic objective margins:

```text
base       5.354413e-04  above cutoff
highband   6.720074e-04  above cutoff
late       7.590895e-04  above cutoff
late_high  8.314008e-04  above cutoff
veryhigh   7.045823e-04  above cutoff
early_high 4.946160e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
base objective distinct-radius and changed-geometry competitor is `r=8.75 mm`
at `z=121 mm`.

## Interpretation

The 9-source escalation rescues target2:

```text
5 sources, Tx/Rx=60  base margin 4.980e-04
7 sources, Tx/Rx=60  base margin 4.867e-04
9 sources, Tx/Rx=60  base margin 5.354e-04
```

Carry the early_high caveat, but the base objective clears cutoff and all
diagnostic variants rank the true radius/depth first. No 11-source closeout is
justified. Continue to target1 at the standard 5-source Tx/Rx=60 control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3412 and sampled_unique_colors=289
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1791 and sampled_unique_colors=381
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and sampled_unique_colors=1148
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6339 and sampled_unique_colors=1088
figure notes: figures/FIGURE_NOTES.md present, reports one moderate row and lists early_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 672.5 s through the candidate sweep
```

## Next Decision

Continue seed27777890085288 with target1 at the standard 5-source Tx/Rx=60
control.
