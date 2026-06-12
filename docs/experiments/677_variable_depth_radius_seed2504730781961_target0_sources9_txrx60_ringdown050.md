# Experiment 677: Seed2504730781961 Target0 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Run the source-density rescue for seed2504730781961 target0 after the 8-source
spacing ladder preserved the exact geometry but stayed below the
moderate-confidence cutoff. This run returns to canonical Tx/Rx=60 and
increases the aperture to 9 sources.

## 1140: Coordinate Optimizer Variable-Depth/Radius Seed2504730781961 Target0 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1140_coordinate_optimizer_variable_depth_radius_seed2504730781961_target0_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1140 is exact and accepted by the 9-source source-density rescue:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 5.296469e-04
offset from cutoff: +2.964689e-05
relative margin: 3.368699e-02
confidence label: moderate
fallback warning: none
best misfit: 1.572260e-02
next radius misfit: 1.625224e-02
elapsed: 652.6 s
```

Diagnostic objective margins:

```text
base       5.296469e-04  above cutoff
highband   7.350984e-04  above cutoff
late       3.821278e-04  below cutoff
late_high  4.641037e-04  below cutoff
veryhigh   7.979799e-04  above cutoff
early_high 6.388480e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
distinct-radius competitor is `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.0 mm` at `z=81 mm`.

## Interpretation

The standard 9-source Tx/Rx=60 source-density bracket rescues this target0 row.
It improves the base margin over both comparison points:

```text
8 sources, Tx/Rx=60  base margin 3.873e-04
8 sources, Tx/Rx=45  base margin 4.843e-04
9 sources, Tx/Rx=60  base margin 5.296e-04
```

Late and late_high remain below cutoff, so carry the recurring target0
late-window caveat. No 11-source cleanup is justified because the base rule
passes, highband/veryhigh/early_high pass, and all objective variants preserve
the true geometry. Continue seed2504730781961 with target2 at the standard
5-source Tx/Rx=60 control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3404 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1666 and unique_colors=822
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and unique_colors=3167
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6308 and unique_colors=2136
figure notes: figures/FIGURE_NOTES.md present, lists late and late_high below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 652.6 s through the candidate sweep
```

## Next Decision

Run seed2504730781961 target2 with 5 sources and Tx/Rx=60. If target2 is weak,
use the recent target2 source-density bracket policy rather than revisiting the
target0 spacing ladder.
