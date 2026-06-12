# Experiment 686: Seed10610209877723 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Start the seed10610209877723 Fibonacci branch after seed6557470329842 closed.
This run tests target0 at the standard 8-source Tx/Rx=60 control under the
ringdown050 source-mismatch/noise condition.

## 1149: Coordinate Optimizer Variable-Depth/Radius Seed10610209877723 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1149_coordinate_optimizer_variable_depth_radius_seed10610209877723_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1149 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.294598e-04
offset from cutoff: +2.945980e-05
relative margin: 3.326349e-02
confidence label: moderate
fallback warning: none
best misfit: 1.591714e-02
next radius misfit: 1.644660e-02
elapsed: 609.2 s
```

Diagnostic objective margins:

```text
base       5.294598e-04  above cutoff
highband   6.974767e-04  above cutoff
late       3.830555e-04  below cutoff
late_high  4.490728e-04  below cutoff
veryhigh   6.424100e-04  above cutoff
early_high 5.751065e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
distinct-radius competitor is `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.0 mm` at `z=81 mm`.

## Interpretation

Target0 passes the standard 8-source Tx/Rx=60 control. Late and late_high
remain weak, so carry the recurring target0 late-window caveat. No rescue
branch is justified because the base row passes and all objective variants
preserve the true geometry. Continue seed10610209877723 with target2 at the
standard 5-source Tx/Rx=60 control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3379 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1710 and unique_colors=822
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and unique_colors=3167
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6336 and unique_colors=2141
figure notes: figures/FIGURE_NOTES.md present, lists late and late_high below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 609.2 s through the candidate sweep
```

## Next Decision

Run seed10610209877723 target2 with 5 sources and Tx/Rx=60.
