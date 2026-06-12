# Experiment 657: Seed365435296162 Target0 Sources=8 Tx/Rx=50 Ringdown050

## Purpose

Bracket the seed365435296162 target0 acquisition rescue at Tx/Rx=50. Run 1121
improved the weak Tx/Rx=60 row but remained just below cutoff at Tx/Rx=52.5, so
this run tests whether a 50 mm offset gives useful base-margin reserve.

## 1122: Coordinate Optimizer Variable-Depth/Radius Seed365435296162 Target0 Sources=8 Tx/Rx=50 Ringdown050

Output:

```text
outputs/experiments/1122_coordinate_optimizer_variable_depth_radius_seed365435296162_target0_sources8_txrx50_ringdown050_objectives
```

## Results

Run 1122 is exact and base-accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 50.0
absolute radius margin: 5.049557e-04
offset from cutoff: +4.955676e-06
relative margin: 2.651008e-02
confidence label: moderate
fallback warning: none
best misfit: 1.904769e-02
next radius misfit: 1.955264e-02
```

Diagnostic objective margins:

```text
base       5.049557e-04  above cutoff
highband   6.780759e-04  above cutoff
late       3.956564e-04  weak, below cutoff
late_high  4.396859e-04  weak, below cutoff
veryhigh   6.520031e-04  above cutoff
early_high 5.567277e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
distinct-radius competitor remains `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.00 mm` at `z=81 mm`.

## Interpretation

Tx/Rx=50 clears the base cutoff and improves the base margin by about
`1.07e-05` over Tx/Rx=52.5 and `4.25e-05` over Tx/Rx=60. The accepted reserve
is still small, and late/late_high remain weak. Follow the seed5702887
lower-edge bracket precedent by running one Tx/Rx=45 check before closing
target0.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png unique=338 nonwhite_fraction=0.3287
figure validation: coordinate_radius_decision_panel.png unique=822 nonwhite_fraction=0.1601
figure validation: coordinate_objective_radius_candidates.png unique=3133 nonwhite_fraction=0.0679
figure validation: system_scene_geometry.png unique=2108 nonwhite_fraction=0.6307
visual inspection: decision panel shows exact selected r=5.00 mm and base just above cutoff
metadata validation: tx_rx_offset_mm is 50.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in about 570 s
```

## Next Decision

Run seed365435296162 target0 with 8 sources and Tx/Rx=45. If it strengthens
the base margin, close target0 with the lower-offset caveat and continue to
target2. If it weakens, keep Tx/Rx=50 as the best tested accepted point.
