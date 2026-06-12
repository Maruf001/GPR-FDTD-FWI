# Experiment 671: Seed1548008755920 Target2 Sources=7 Tx/Rx=60 Ringdown050

## Purpose

Run the standard target2 source-density bracket after the seed1548008755920
5-source target2 control preserved the true geometry but failed the base
confidence cutoff.

## 1134: Coordinate Optimizer Variable-Depth/Radius Seed1548008755920 Target2 Sources=7 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1134_coordinate_optimizer_variable_depth_radius_seed1548008755920_target2_sources7_txrx60_ringdown050_objectives
```

## Results

Run 1134 is exact and accepted with a razor-thin base reserve and an early_high
caveat:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 7
tx_rx_offset_mm: 60.0
absolute radius margin: 5.015880e-04
offset from cutoff: +1.588007e-06
relative margin: 3.398505e-02
confidence label: moderate
fallback warning: none
best misfit: 1.475908e-02
next radius misfit: 1.526067e-02
elapsed: 520.2 s
```

Diagnostic objective margins:

```text
base       5.015880e-04  above cutoff
highband   6.099906e-04  above cutoff
late       7.277387e-04  above cutoff
late_high  7.571658e-04  above cutoff
veryhigh   6.278648e-04  above cutoff
early_high 4.024552e-04  weak, below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
distinct-radius competitor is `r=8.75 mm`; the closest changed-geometry
competitor is `r=8.75 mm` at `z=121 mm`.

## Interpretation

The 7-source bracket formally rescues the target2 base confidence row, but the
reserve above cutoff is only `1.588e-06`. This is accepted because the base
rule passes, all objective variants rank the true geometry first, and prior
target2 7-source rescue policy does not run an immediate 9-source cleanup once
the base row clears. Carry both caveats: the base reserve is razor-thin and
early_high remains weak.

Continue seed1548008755920 with target1 at the standard 5-source Tx/Rx=60
control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3243 and unique_colors=394
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1598 and unique_colors=869
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and unique_colors=2990
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6308 and unique_colors=2107
figure notes: figures/FIGURE_NOTES.md present, lists early_high below cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=7; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 89%; run completed in 520.2 s
```

## Next Decision

Continue seed1548008755920 with target1 at the standard 5-source Tx/Rx=60
control under the same ringdown050 objective suite.
