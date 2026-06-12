# Experiment 703: Seed44945570292853 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Start the seed44945570292853 Fibonacci replication branch with the standard
target0 8-source Tx/Rx=60 control.

## 1166: Coordinate Optimizer Variable-Depth/Radius Seed44945570292853 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1166_coordinate_optimizer_variable_depth_radius_seed44945570292853_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1166 selected the exact geometry but remains below the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 4.945706e-04
offset from cutoff: -5.429425e-06
relative margin: 3.146040e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.572042e-02
next radius misfit: 1.621499e-02
elapsed: 578.0 s
```

Diagnostic objective margins:

```text
base       4.945706e-04  below cutoff
highband   6.207747e-04  above cutoff
late       4.169343e-04  below cutoff
late_high  4.703645e-04  below cutoff
veryhigh   5.734923e-04  above cutoff
early_high 5.147492e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
base objective distinct-radius competitor is `r=5.25 mm` at the same depth,
and the closest changed-geometry competitor is `r=6.0 mm` at `z=81 mm`.

## Interpretation

This is a near-miss target0 weak control: the base margin is only
`5.429e-06` below cutoff, but late and late_high are also weak. The geometry is
truth-preserving across all objective variants. Follow the target0 weak-control
policy with an 8-source Tx/Rx=52.5 mm acquisition probe before deciding whether
tighter spacing or a 9-source Tx/Rx=60 source-density bracket is the better
rescue.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3186 and sampled_unique_colors=227
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1632 and sampled_unique_colors=382
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and sampled_unique_colors=1164
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6337 and sampled_unique_colors=1092
figure notes: figures/FIGURE_NOTES.md present, reports one weak row and lists base, late, and late_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 578.0 s through the candidate sweep
```

## Next Decision

Run seed44945570292853 target0 with the same 8-source aperture at Tx/Rx=52.5 mm.
