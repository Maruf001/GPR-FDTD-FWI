# Experiment 685: Seed6557470329842 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Complete seed6557470329842 after target0 passed cleanly at the standard
8-source Tx/Rx=60 control and target2 passed the standard 5-source Tx/Rx=60
control with a razor-thin base reserve and early_high caveat. This run tests
target1 at the standard 5-source Tx/Rx=60 control under the same ringdown050
source-mismatch/noise condition.

## 1148: Coordinate Optimizer Variable-Depth/Radius Seed6557470329842 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1148_coordinate_optimizer_variable_depth_radius_seed6557470329842_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1148 is exact and accepted, with an early_high diagnostic caveat:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.202871e-04
offset from cutoff: +2.028710e-05
relative margin: 3.072429e-02
confidence label: moderate
fallback warning: none
best misfit: 1.693406e-02
next radius misfit: 1.745435e-02
elapsed: 366.5 s
```

Diagnostic objective margins:

```text
base       5.202871e-04  above cutoff
highband   6.570116e-04  above cutoff
late       8.328828e-04  above cutoff
late_high  9.124961e-04  above cutoff
veryhigh   6.352853e-04  above cutoff
early_high 4.784448e-04  below cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
distinct-radius competitor is `r=6.25 mm`; the closest changed-geometry
competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

Target1 passes the standard 5-source Tx/Rx=60 control. Early_high is weak, so
carry that caveat. This closes seed6557470329842:

```text
target0: accepted cleanly at 8-source Tx/Rx=60
target2: accepted at 5-source Tx/Rx=60, with razor-thin base reserve and early_high caveat
target1: accepted at 5-source Tx/Rx=60, with early_high caveat
```

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3351 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1619 and unique_colors=859
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and unique_colors=3016
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6308 and unique_colors=2050
figure notes: figures/FIGURE_NOTES.md present, lists early_high below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 366.5 s through the candidate sweep
```

## Next Decision

Continue the Fibonacci replication chain with seed10610209877723 target0. Seed
validation succeeded in the active FNO environment:

```text
np.random.default_rng(10610209877723) succeeded
```
