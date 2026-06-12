# Experiment 673: Seed2504730781961 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Continue the Fibonacci replication chain after seed1548008755920 closed.
This run tests seed2504730781961 target0 at the standard 8-source Tx/Rx=60
control under the ringdown050 source-mismatch/noise condition.

## 1136: Coordinate Optimizer Variable-Depth/Radius Seed2504730781961 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1136_coordinate_optimizer_variable_depth_radius_seed2504730781961_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1136 selected the exact geometry, but the decision is weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 3.872998e-04
offset from cutoff: -1.127002e-04
relative margin: 2.460596e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.574008e-02
next radius misfit: 1.612738e-02
elapsed: 567.5 s
```

Diagnostic objective margins:

```text
base       3.872998e-04  below cutoff
highband   4.953100e-04  below cutoff
late       2.735985e-04  below cutoff
late_high  3.255405e-04  below cutoff
veryhigh   4.694052e-04  below cutoff
early_high 4.134309e-04  below cutoff
```

All six objective variants still rank the exact target0 geometry first. The
closest distinct-radius competitor is `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.0 mm` at `z=81 mm`.

## Interpretation

The geometry is exact, but the control does not pass the moderate-confidence
radius-margin rule. Unlike the accepted target0 controls with only late-window
weakness, this run is weak across all six objective variants. Follow the
target0 weak-control policy with a Tx/Rx=52.5 mm acquisition probe before
deciding whether tighter spacing or additional sources are justified.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.2594 and unique_colors=234
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1803 and unique_colors=974
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and unique_colors=3169
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6309 and unique_colors=2103
figure notes: figures/FIGURE_NOTES.md present, lists all six objective variants below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 567.5 s through the candidate sweep
```

## Next Decision

Run seed2504730781961 target0 with the same 8-source aperture at Tx/Rx=52.5 mm.
If the margin remains below cutoff, continue the target0 spacing probe ladder
rather than accepting the weak Tx/Rx=60 control.
