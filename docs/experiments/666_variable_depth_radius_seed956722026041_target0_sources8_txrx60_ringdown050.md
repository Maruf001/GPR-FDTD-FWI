# Experiment 666: Seed956722026041 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Continue the Fibonacci replication chain after closing seed591286729879. This
run tests seed956722026041 target0 at the standard 8-source Tx/Rx=60 control
under the ringdown050 source-mismatch/noise condition.

Seed validation:

```text
np.random.default_rng(956722026041) succeeded in the active FNO environment.
```

## 1129: Coordinate Optimizer Variable-Depth/Radius Seed956722026041 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1129_coordinate_optimizer_variable_depth_radius_seed956722026041_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1129 is exact and accepted with the recurring target0 late-window caveat:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.821233e-04
offset from cutoff: +8.212335e-05
relative margin: 3.738462e-02
confidence label: moderate
fallback warning: none
best misfit: 1.557120e-02
next radius misfit: 1.615332e-02
elapsed: 580.7 s
```

Diagnostic objective margins:

```text
base       5.821233e-04  above cutoff
highband   7.489600e-04  above cutoff
late       4.546483e-04  weak, below cutoff
late_high  5.454778e-04  above cutoff
veryhigh   6.961195e-04  above cutoff
early_high 6.304126e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
distinct-radius competitor is `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.00 mm` at `z=81 mm`.

## Interpretation

The base confidence rule accepts target0, and only the late objective is below
cutoff. This matches the recurring accepted target0 pattern: base clears,
late_high clears, all high-frequency variants clear, and all objective
variants preserve the exact true geometry. No Tx/Rx acquisition probe is
justified.

Continue seed956722026041 with target2 at the standard 5-source Tx/Rx=60
control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3738 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2128x1583 RGB with nonwhite_fraction=0.1880 and unique_colors=840
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and unique_colors=3167
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6308 and unique_colors=2102
figure notes: figures/FIGURE_NOTES.md present, lists late below cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90%; run completed in 580.7 s
```

## Next Decision

Continue seed956722026041 with target2 at the standard 5-source Tx/Rx=60
control under the same ringdown050 objective suite.
