# Experiment 684: Seed6557470329842 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Continue seed6557470329842 after target0 passed cleanly at the standard
8-source Tx/Rx=60 control. This run tests target2 at the standard 5-source
Tx/Rx=60 control under the ringdown050 source-mismatch/noise condition.

## 1147: Coordinate Optimizer Variable-Depth/Radius Seed6557470329842 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1147_coordinate_optimizer_variable_depth_radius_seed6557470329842_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1147 is exact and accepted, but with a razor-thin base reserve and an
early_high diagnostic caveat:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.065078e-04
offset from cutoff: +6.507808e-06
relative margin: 2.991059e-02
confidence label: moderate
fallback warning: none
best misfit: 1.693406e-02
next radius misfit: 1.744057e-02
elapsed: 368.0 s
```

Diagnostic objective margins:

```text
base       5.065078e-04  above cutoff
highband   6.193885e-04  above cutoff
late       7.576086e-04  above cutoff
late_high  7.609849e-04  above cutoff
veryhigh   6.502960e-04  above cutoff
early_high 4.471996e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
distinct-radius and changed-geometry competitor is `r=8.75 mm` at `z=121 mm`.

## Interpretation

Target2 passes the base rule, but the reserve is only 6.51e-06 above cutoff.
Because highband, late, late_high, and veryhigh clear cutoff and all objective
variants preserve the true geometry, no source-density rescue is justified.
Carry both caveats: razor-thin base reserve and weak early_high. Continue
seed6557470329842 with target1 at the standard 5-source Tx/Rx=60 control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3271 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1658 and unique_colors=867
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and unique_colors=2990
figure validation: system_scene_geometry.png is 1775x1065 RGB with nonwhite_fraction=0.6311 and unique_colors=2042
figure notes: figures/FIGURE_NOTES.md present, lists early_high below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 368.0 s through the candidate sweep
```

## Next Decision

Run seed6557470329842 target1 with 5 sources and Tx/Rx=60.
