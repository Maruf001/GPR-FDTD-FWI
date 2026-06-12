# Experiment 675: Seed2504730781961 Target0 Sources=8 Tx/Rx=50 Ringdown050

## Purpose

Continue the target0 acquisition-spacing ladder for seed2504730781961. The
Tx/Rx=60 control and 52.5 mm probe both selected the exact target0 geometry but
remained below the moderate-confidence cutoff, so this run tests the same
8-source setup at Tx/Rx=50 mm.

## 1138: Coordinate Optimizer Variable-Depth/Radius Seed2504730781961 Target0 Sources=8 Tx/Rx=50 Ringdown050

Output:

```text
outputs/experiments/1138_coordinate_optimizer_variable_depth_radius_seed2504730781961_target0_sources8_txrx50_ringdown050_objectives
```

## Results

Run 1138 selected the exact geometry but remained weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 50.0
absolute radius margin: 4.477069e-04
offset from cutoff: -5.229314e-05
relative margin: 2.343632e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.910312e-02
next radius misfit: 1.955083e-02
elapsed: 562.7 s
```

Diagnostic objective margins:

```text
base       4.477069e-04  below cutoff
highband   5.897961e-04  above cutoff
late       3.280513e-04  below cutoff
late_high  3.580254e-04  below cutoff
veryhigh   5.619058e-04  above cutoff
early_high 4.760022e-04  below cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
distinct-radius competitor is `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.0 mm` at `z=81 mm`.

## Interpretation

Tx/Rx=50 continues the upward trend but does not rescue the base confidence:

```text
Tx/Rx=60.0  base margin 3.873e-04
Tx/Rx=52.5  base margin 4.324e-04
Tx/Rx=50.0  base margin 4.477e-04
```

The spacing trend is monotone but flattening. Based on the earlier
seed5702887 target0 acquisition bracket, run one lower-edge Tx/Rx=45 mm probe
before escalating source density. If Tx/Rx=45 also remains below cutoff, stop
the spacing ladder for this seed and use a source-density rescue instead of
continuing to smaller offsets without evidence.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.2936 and unique_colors=233
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1790 and unique_colors=794
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and unique_colors=3153
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6308 and unique_colors=2090
figure notes: figures/FIGURE_NOTES.md present, lists base, late, late_high, and early_high below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 50.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 562.7 s through the candidate sweep
```

## Next Decision

Run seed2504730781961 target0 with the same 8-source aperture at Tx/Rx=45 mm.
Treat this as the lower-edge spacing bracket before source-density escalation.
