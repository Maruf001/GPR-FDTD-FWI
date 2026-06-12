# Experiment 699: Seed27777890085288 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run the standard target2 5-source Tx/Rx=60 control for seed27777890085288 after
target0 was accepted with the recurring late-window caveat.

## 1162: Coordinate Optimizer Variable-Depth/Radius Seed27777890085288 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1162_coordinate_optimizer_variable_depth_radius_seed27777890085288_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1162 selected the exact geometry but remains just below the moderate
cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 4.980430e-04
offset from cutoff: -1.956958e-06
relative margin: 2.944453e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.691462e-02
next radius misfit: 1.741266e-02
elapsed: 378.6 s
```

Diagnostic objective margins:

```text
base       4.980430e-04  below cutoff
highband   6.079216e-04  above cutoff
late       7.438839e-04  above cutoff
late_high  7.606177e-04  above cutoff
veryhigh   6.465337e-04  above cutoff
early_high 4.721510e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
base objective distinct-radius and changed-geometry competitor is `r=8.75 mm`
at `z=121 mm`.

## Interpretation

This is a near-miss weak target2 control: the base margin is only
`1.957e-06` below cutoff, but the row is still formally weak and early_high is
also below cutoff. Follow the standard target2 policy with a 7-source Tx/Rx=60
source-density bracket before accepting or escalating further.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3206 and sampled_unique_colors=227
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1620 and sampled_unique_colors=379
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and sampled_unique_colors=1148
figure validation: system_scene_geometry.png is 1768x1065 RGB with nonwhite_fraction=0.6338 and sampled_unique_colors=1067
figure notes: figures/FIGURE_NOTES.md present, reports one weak row and lists base and early_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 378.6 s through the candidate sweep
```

## Next Decision

Run seed27777890085288 target2 with 7 sources and Tx/Rx=60 as the
source-density bracket.
