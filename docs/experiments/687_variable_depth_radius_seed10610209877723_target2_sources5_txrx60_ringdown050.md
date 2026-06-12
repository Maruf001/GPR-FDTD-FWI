# Experiment 687: Seed10610209877723 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Continue seed10610209877723 after target0 passed the standard 8-source Tx/Rx=60
control with a late-window caveat. This run tests target2 at the standard
5-source Tx/Rx=60 control under the ringdown050 source-mismatch/noise
condition.

## 1150: Coordinate Optimizer Variable-Depth/Radius Seed10610209877723 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1150_coordinate_optimizer_variable_depth_radius_seed10610209877723_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1150 selected the exact geometry but is weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 4.718645e-04
offset from cutoff: -2.813550e-05
relative margin: 2.738909e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.722819e-02
next radius misfit: 1.770006e-02
elapsed: 389.3 s
```

Diagnostic objective margins:

```text
base       4.718645e-04  below cutoff
highband   5.159554e-04  above cutoff
late       7.802744e-04  above cutoff
late_high  7.142558e-04  above cutoff
veryhigh   6.027835e-04  above cutoff
early_high 3.987411e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
distinct-radius and changed-geometry competitor is `r=8.75 mm` at `z=121 mm`.

## Interpretation

Target2 preserves the true geometry, but the base row misses cutoff and
early_high is also weak. Follow the recent target2 weak-control policy with a
7-source Tx/Rx=60 source-density bracket before considering 9 sources. No
separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3056 and unique_colors=233
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1670 and unique_colors=857
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and unique_colors=2990
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6339 and unique_colors=2047
figure notes: figures/FIGURE_NOTES.md present, lists base and early_high below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 389.3 s through the candidate sweep
```

## Next Decision

Run seed10610209877723 target2 with 7 sources and Tx/Rx=60. If that bracket
does not rescue the base row, continue to the standard 9-source Tx/Rx=60
target2 escalation.
