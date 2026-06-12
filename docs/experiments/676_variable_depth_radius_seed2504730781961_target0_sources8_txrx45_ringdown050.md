# Experiment 676: Seed2504730781961 Target0 Sources=8 Tx/Rx=45 Ringdown050

## Purpose

Run the lower-edge target0 spacing bracket for seed2504730781961. The 8-source
Tx/Rx=60, 52.5, and 50 mm rows all selected the exact geometry but remained
below the moderate-confidence cutoff, so this run tests the final planned
spacing point before source-density escalation.

## 1139: Coordinate Optimizer Variable-Depth/Radius Seed2504730781961 Target0 Sources=8 Tx/Rx=45 Ringdown050

Output:

```text
outputs/experiments/1139_coordinate_optimizer_variable_depth_radius_seed2504730781961_target0_sources8_txrx45_ringdown050_objectives
```

## Results

Run 1139 selected the exact geometry but still remained just below cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 45.0
absolute radius margin: 4.842585e-04
offset from cutoff: -1.574153e-05
relative margin: 2.276416e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 2.127284e-02
next radius misfit: 2.175710e-02
elapsed: 567.1 s
```

Diagnostic objective margins:

```text
base       4.842585e-04  below cutoff
highband   6.520764e-04  above cutoff
late       4.169480e-04  below cutoff
late_high  4.392972e-04  below cutoff
veryhigh   6.495970e-04  above cutoff
early_high 5.081162e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
distinct-radius competitor is `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.0 mm` at `z=81 mm`.

## Interpretation

The target0 spacing ladder was monotone and truth-preserving but did not pass
the base rule:

```text
Tx/Rx=60.0  base margin 3.873e-04
Tx/Rx=52.5  base margin 4.324e-04
Tx/Rx=50.0  base margin 4.477e-04
Tx/Rx=45.0  base margin 4.843e-04
```

Because the predeclared lower-edge spacing bracket still misses cutoff by
1.57e-05, stop the simple spacing ladder for this seed. Switch mechanism to a
standard target0 9-source Tx/Rx=60 source-density bracket so the source-count
effect is measured against the canonical acquisition spacing before any
combined spacing/source-density rescue is considered.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3149 and unique_colors=233
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1683 and unique_colors=812
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and unique_colors=3078
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6308 and unique_colors=2089
figure notes: figures/FIGURE_NOTES.md present, lists base, late, and late_high below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 45.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 567.1 s through the candidate sweep
```

## Next Decision

Run seed2504730781961 target0 with 9 sources at Tx/Rx=60 mm. Compare that
source-density bracket against both the original 8-source Tx/Rx=60 control and
the best 8-source spacing row at Tx/Rx=45 mm before choosing any further
escalation.
