# Experiment 670: Seed1548008755920 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Continue seed1548008755920 after target0 accepted at the standard 8-source
control with the recurring late-window caveat. This run tests target2 at the
standard 5-source Tx/Rx=60 control under the ringdown050 source-mismatch/noise
condition.

## 1133: Coordinate Optimizer Variable-Depth/Radius Seed1548008755920 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1133_coordinate_optimizer_variable_depth_radius_seed1548008755920_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1133 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 4.738266e-04
offset from cutoff: -2.617345e-05
relative margin: 2.765184e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.713544e-02
next radius misfit: 1.760927e-02
elapsed: 379.3 s
```

Diagnostic objective margins:

```text
base       4.738266e-04  weak, below cutoff
highband   5.639381e-04  above cutoff
late       6.964037e-04  above cutoff
late_high  6.744557e-04  above cutoff
veryhigh   5.896009e-04  above cutoff
early_high 4.222120e-04  weak, below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
distinct-radius competitor is `r=8.75 mm`; the closest changed-geometry
competitor is `r=8.75 mm` at `z=121 mm`.

## Interpretation

The control preserves the true geometry, but the base row is below the
`5.0e-4` cutoff and early_high is also weak. Because highband, late,
late_high, and veryhigh already clear cutoff while base and early_high do not,
follow the established target2 weak-control policy with a 7-source Tx/Rx=60
source-density bracket before considering 9 sources.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3089 and unique_colors=236
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1769 and unique_colors=857
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and unique_colors=2990
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6308 and unique_colors=2092
figure notes: figures/FIGURE_NOTES.md present, lists base and early_high below cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 87%; run completed in 379.3 s
```

## Next Decision

Run seed1548008755920 target2 at 7 sources and Tx/Rx=60 before considering a
9-source escalation.
