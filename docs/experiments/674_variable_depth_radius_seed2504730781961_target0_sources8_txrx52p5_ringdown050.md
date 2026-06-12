# Experiment 674: Seed2504730781961 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

## Purpose

Follow up the weak Tx/Rx=60 control for seed2504730781961 target0. This run
keeps the 8-source aperture but tightens Tx/Rx spacing to 52.5 mm to test
whether the radius margin recovers under the same ringdown050
source-mismatch/noise condition.

## 1137: Coordinate Optimizer Variable-Depth/Radius Seed2504730781961 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1137_coordinate_optimizer_variable_depth_radius_seed2504730781961_target0_sources8_txrx52p5_ringdown050_objectives
```

## Results

Run 1137 selected the exact geometry but remained weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 52.5
absolute radius margin: 4.324383e-04
offset from cutoff: -6.756166e-05
relative margin: 2.354827e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.836391e-02
next radius misfit: 1.879635e-02
elapsed: 552.9 s
```

Diagnostic objective margins:

```text
base       4.324383e-04  below cutoff
highband   5.652835e-04  above cutoff
late       3.029100e-04  below cutoff
late_high  3.374468e-04  below cutoff
veryhigh   5.335920e-04  above cutoff
early_high 4.614985e-04  below cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
distinct-radius competitor is again `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.0 mm` at `z=81 mm`.

## Interpretation

Tightening Tx/Rx from 60.0 mm to 52.5 mm improves the base margin from
3.873e-04 to 4.324e-04 and restores highband/veryhigh above cutoff, but it
does not clear the base rule. Continue the target0 spacing ladder with Tx/Rx=50
mm before considering a stronger source-density rescue.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.2847 and unique_colors=236
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1830 and unique_colors=794
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and unique_colors=3174
figure validation: system_scene_geometry.png is 1770x1065 RGB with nonwhite_fraction=0.6331 and unique_colors=2118
figure notes: figures/FIGURE_NOTES.md present, lists base, late, late_high, and early_high below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 52.5; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 552.9 s through the candidate sweep
```

## Next Decision

Run seed2504730781961 target0 with the same 8-source aperture at Tx/Rx=50 mm.
If that also remains weak, compare the spacing trend before choosing between a
tighter spacing probe and a source-density rescue.
