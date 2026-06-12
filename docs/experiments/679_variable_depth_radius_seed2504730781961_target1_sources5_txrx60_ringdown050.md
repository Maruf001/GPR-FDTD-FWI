# Experiment 679: Seed2504730781961 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Complete seed2504730781961 after target0 was accepted by the 9-source Tx/Rx=60
source-density rescue and target2 passed the standard 5-source Tx/Rx=60
control with an early_high caveat. This run tests target1 at the standard
5-source Tx/Rx=60 control under the same ringdown050 source-mismatch/noise
condition.

## 1142: Coordinate Optimizer Variable-Depth/Radius Seed2504730781961 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1142_coordinate_optimizer_variable_depth_radius_seed2504730781961_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1142 is exact and accepted, with an early_high diagnostic caveat:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.173551e-04
offset from cutoff: +1.735512e-05
relative margin: 3.094207e-02
confidence label: moderate
fallback warning: none
best misfit: 1.672012e-02
next radius misfit: 1.723747e-02
elapsed: 367.9 s
```

Diagnostic objective margins:

```text
base       5.173551e-04  above cutoff
highband   6.409903e-04  above cutoff
late       7.858969e-04  above cutoff
late_high  8.564727e-04  above cutoff
veryhigh   6.180360e-04  above cutoff
early_high 4.710454e-04  below cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
distinct-radius competitor is `r=6.25 mm`; the closest changed-geometry
competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

Target1 passes the standard 5-source Tx/Rx=60 control. The base reserve is
small but positive, and all diagnostic objectives preserve the true geometry.
Early_high remains weak, so carry an early_high caveat.

This closes seed2504730781961:

```text
target0: accepted by 9-source Tx/Rx=60 source-density rescue, with late-window caveat
target2: accepted at 5-source Tx/Rx=60, with early_high caveat
target1: accepted at 5-source Tx/Rx=60, with early_high caveat
```

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3335 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1626 and unique_colors=859
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and unique_colors=3006
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6307 and unique_colors=2063
figure notes: figures/FIGURE_NOTES.md present, lists early_high below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 367.9 s through the candidate sweep
```

## Next Decision

Continue the Fibonacci replication chain with seed4052739547881 target0. Seed
validation succeeded in the active FNO environment:

```text
np.random.default_rng(4052739547881) succeeded
```
