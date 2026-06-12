# Experiment 667: Seed956722026041 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Continue seed956722026041 after target0 accepted at the standard 8-source
Tx/Rx=60 control with the recurring late-window caveat. This run tests target2
at the standard 5-source Tx/Rx=60 control under the ringdown050
source-mismatch/noise condition.

## 1130: Coordinate Optimizer Variable-Depth/Radius Seed956722026041 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1130_coordinate_optimizer_variable_depth_radius_seed956722026041_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1130 is exact and accepted with an early_high caveat:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.321765e-04
offset from cutoff: +3.217649e-05
relative margin: 3.165170e-02
confidence label: moderate
fallback warning: none
best misfit: 1.681352e-02
next radius misfit: 1.734570e-02
elapsed: 392.1 s
```

Diagnostic objective margins:

```text
base       5.321765e-04  above cutoff
highband   6.446044e-04  above cutoff
late       7.840712e-04  above cutoff
late_high  8.096353e-04  above cutoff
veryhigh   7.055425e-04  above cutoff
early_high 4.798945e-04  weak, below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
distinct-radius competitor is `r=8.75 mm`; the closest changed-geometry
competitor is `r=8.75 mm` at `z=121 mm`.

## Interpretation

Target2 passes the base confidence rule at the standard 5-source Tx/Rx=60
control. Early_high is weak, but this is a recurring target2 caveat and does
not justify rescue when the base row clears and every objective variant ranks
the true geometry first.

Continue seed956722026041 with target1 at the standard 5-source Tx/Rx=60
control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3448 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1811 and unique_colors=864
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and unique_colors=2990
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6306 and unique_colors=2081
figure notes: figures/FIGURE_NOTES.md present, lists early_high below cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 87%; run completed in 392.1 s
```

## Next Decision

Continue seed956722026041 with target1 at the standard 5-source Tx/Rx=60
control under the same ringdown050 objective suite.
