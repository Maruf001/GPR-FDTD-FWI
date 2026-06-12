# Experiment 681: Seed4052739547881 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Continue seed4052739547881 after target0 passed the standard 8-source Tx/Rx=60
control with the recurring late-window caveat. This run tests target2 at the
standard 5-source Tx/Rx=60 control under the ringdown050 source-mismatch/noise
condition.

## 1144: Coordinate Optimizer Variable-Depth/Radius Seed4052739547881 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1144_coordinate_optimizer_variable_depth_radius_seed4052739547881_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1144 is exact and accepted cleanly:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 6.342653e-04
offset from cutoff: +1.342653e-04
relative margin: 3.715314e-02
confidence label: moderate
fallback warning: none
best misfit: 1.707165e-02
next radius misfit: 1.770591e-02
elapsed: 365.5 s
```

Diagnostic objective margins:

```text
base       6.342653e-04  above cutoff
highband   7.923548e-04  above cutoff
late       9.536977e-04  above cutoff
late_high  1.012281e-03  above cutoff
veryhigh   7.761873e-04  above cutoff
early_high 5.511862e-04  above cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
distinct-radius and changed-geometry competitor is `r=8.75 mm` at `z=121 mm`.

## Interpretation

Target2 passes cleanly at the standard 5-source Tx/Rx=60 control. No
source-density or acquisition rescue is justified. Continue seed4052739547881
with target1 at the standard 5-source Tx/Rx=60 control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.4004 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2128x1583 RGB with nonwhite_fraction=0.1833 and unique_colors=871
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and unique_colors=2990
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6308 and unique_colors=2080
figure notes: figures/FIGURE_NOTES.md present, lists no objective variants below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 365.5 s through the candidate sweep
```

## Next Decision

Run seed4052739547881 target1 with 5 sources and Tx/Rx=60.
