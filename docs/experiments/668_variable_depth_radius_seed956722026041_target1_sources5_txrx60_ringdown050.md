# Experiment 668: Seed956722026041 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Complete seed956722026041 after target0 accepted at the standard 8-source
control and target2 accepted at the standard 5-source control with an
early_high caveat. This run tests target1 at the standard 5-source Tx/Rx=60
control under the ringdown050 source-mismatch/noise condition.

## 1131: Coordinate Optimizer Variable-Depth/Radius Seed956722026041 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1131_coordinate_optimizer_variable_depth_radius_seed956722026041_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1131 is exact and accepted with an early_high caveat:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.173580e-04
offset from cutoff: +1.735799e-05
relative margin: 3.077036e-02
confidence label: moderate
fallback warning: none
best misfit: 1.681352e-02
next radius misfit: 1.733088e-02
elapsed: 391.7 s
```

Diagnostic objective margins:

```text
base       5.173580e-04  above cutoff
highband   6.595719e-04  above cutoff
late       7.895782e-04  above cutoff
late_high  8.611893e-04  above cutoff
veryhigh   6.115457e-04  above cutoff
early_high 4.788651e-04  weak, below cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
distinct-radius competitor is `r=6.25 mm`; the closest changed-geometry
competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

Target1 passes the base confidence rule at the standard 5-source Tx/Rx=60
control. Early_high is weak, but the exact geometry is preserved across all
diagnostic objectives and prior target1 precedent accepts this pattern when
the base row clears. No target1 rescue is justified.

This closes seed956722026041:

```text
target0: accepted at 8 sources, Tx/Rx=60, with recurring late-window caveat
target2: accepted at 5 sources, Tx/Rx=60, with early_high caveat
target1: accepted at 5 sources, Tx/Rx=60, with early_high caveat
```

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3360 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1637 and unique_colors=856
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and unique_colors=3016
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6306 and unique_colors=2046
figure notes: figures/FIGURE_NOTES.md present, lists early_high below cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 86%; run completed in 391.7 s
```

## Next Decision

Continue the Fibonacci replication chain with seed1548008755920 target0. Seed
validation succeeded in the active FNO environment:

```text
np.random.default_rng(1548008755920) succeeded
```
