# Experiment 672: Seed1548008755920 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Complete seed1548008755920 after target0 accepted at the standard 8-source
control and target2 was accepted by a 7-source source-density bracket with a
razor-thin base reserve. This run tests target1 at the standard 5-source
Tx/Rx=60 control under the ringdown050 source-mismatch/noise condition.

## 1135: Coordinate Optimizer Variable-Depth/Radius Seed1548008755920 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1135_coordinate_optimizer_variable_depth_radius_seed1548008755920_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1135 is exact and accepted cleanly:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 6.622968e-04
offset from cutoff: +1.622968e-04
relative margin: 3.865070e-02
confidence label: moderate
fallback warning: none
best misfit: 1.713544e-02
next radius misfit: 1.779774e-02
elapsed: 395.2 s
```

Diagnostic objective margins:

```text
base       6.622968e-04  above cutoff
highband   8.373698e-04  above cutoff
late       9.910309e-04  above cutoff
late_high  1.102002e-03  above cutoff
veryhigh   7.797914e-04  above cutoff
early_high 6.256990e-04  above cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
distinct-radius competitor is `r=6.25 mm`; the closest changed-geometry
competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

Target1 passes cleanly at the standard 5-source Tx/Rx=60 control. This closes
seed1548008755920:

```text
target0: accepted at 8 sources, Tx/Rx=60, with recurring late-window caveat
target2: accepted at 7 sources, Tx/Rx=60, with razor-thin base reserve and early_high caveat
target1: accepted cleanly at 5 sources, Tx/Rx=60
```

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.4165 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2128x1583 RGB with nonwhite_fraction=0.1794 and unique_colors=863
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and unique_colors=3003
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6308 and unique_colors=2048
figure notes: figures/FIGURE_NOTES.md present, lists no objective variants below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 87%; run completed in 395.2 s
```

## Next Decision

Continue the Fibonacci replication chain with seed2504730781961 target0. Seed
validation succeeded in the active FNO environment:

```text
np.random.default_rng(2504730781961) succeeded
```
