# Experiment 669: Seed1548008755920 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Continue the Fibonacci replication chain after closing seed956722026041. This
run tests seed1548008755920 target0 at the standard 8-source Tx/Rx=60 control
under the ringdown050 source-mismatch/noise condition.

Seed validation:

```text
np.random.default_rng(1548008755920) succeeded in the active FNO environment.
```

## 1132: Coordinate Optimizer Variable-Depth/Radius Seed1548008755920 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1132_coordinate_optimizer_variable_depth_radius_seed1548008755920_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1132 is exact and accepted with the recurring target0 late-window caveat:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.514880e-04
offset from cutoff: +5.148799e-05
relative margin: 3.486597e-02
confidence label: moderate
fallback warning: none
best misfit: 1.581737e-02
next radius misfit: 1.636886e-02
elapsed: 573.0 s
```

Diagnostic objective margins:

```text
base       5.514880e-04  above cutoff
highband   7.346796e-04  above cutoff
late       4.451094e-04  weak, below cutoff
late_high  5.365616e-04  above cutoff
veryhigh   6.810479e-04  above cutoff
early_high 6.062755e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
distinct-radius competitor is `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.00 mm` at `z=81 mm`.

## Interpretation

The base confidence rule accepts target0, and the only weak diagnostic is the
recurring late objective. Late_high and the other diagnostic variants clear
cutoff while preserving the exact true geometry. No Tx/Rx acquisition probe is
justified.

Continue seed1548008755920 with target2 at the standard 5-source Tx/Rx=60
control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3533 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1878 and unique_colors=835
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and unique_colors=3171
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6310 and unique_colors=2120
figure notes: figures/FIGURE_NOTES.md present, lists late below cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90%; run completed in 573.0 s
```

## Next Decision

Continue seed1548008755920 with target2 at the standard 5-source Tx/Rx=60
control under the same ringdown050 objective suite.
