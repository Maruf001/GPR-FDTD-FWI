# Experiment 665: Seed591286729879 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Complete seed591286729879 after target0 accepted at the 8-source Tx/Rx=60
control with the recurring late-window caveat and target2 passed cleanly at
the standard 5-source control. This run tests target1 at the standard 5-source
Tx/Rx=60 control under the ringdown050 source-mismatch/noise condition.

## 1128: Coordinate Optimizer Variable-Depth/Radius Seed591286729879 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1128_coordinate_optimizer_variable_depth_radius_seed591286729879_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1128 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.931042e-04
offset from cutoff: +9.310421e-05
relative margin: 3.483213e-02
confidence label: moderate
fallback warning: none
best misfit: 1.702750e-02
next radius misfit: 1.762061e-02
elapsed: 392.9 s
```

Diagnostic objective margins:

```text
base       5.931042e-04  above cutoff
highband   7.400148e-04  above cutoff
late       8.875903e-04  above cutoff
late_high  9.627977e-04  above cutoff
veryhigh   7.269060e-04  above cutoff
early_high 5.424691e-04  above cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
distinct-radius competitor is `r=6.25 mm`; the closest changed-geometry
competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

Target1 passes cleanly at the standard 5-source Tx/Rx=60 control. This closes
seed591286729879:

```text
target0: accepted at 8 sources, Tx/Rx=60, with recurring late-window caveat
target2: accepted cleanly at 5 sources, Tx/Rx=60
target1: accepted cleanly at 5 sources, Tx/Rx=60
```

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3803 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2128x1583 RGB with nonwhite_fraction=0.1825 and unique_colors=860
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and unique_colors=3016
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6307 and unique_colors=2046
figure notes: figures/FIGURE_NOTES.md present, lists no objective variants below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 87%; run completed in 392.9 s
```

## Next Decision

Continue the Fibonacci replication chain with seed956722026041 target0. Seed
validation succeeded in the active FNO environment:

```text
np.random.default_rng(956722026041) succeeded
```
