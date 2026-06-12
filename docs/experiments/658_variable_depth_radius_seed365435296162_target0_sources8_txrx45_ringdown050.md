# Experiment 658: Seed365435296162 Target0 Sources=8 Tx/Rx=45 Ringdown050

## Purpose

Check the lower edge of the seed365435296162 target0 acquisition bracket. The
target0 sequence was weak at Tx/Rx=60, nearly accepted at 52.5, and accepted
with small reserve at 50, so this run tests whether 45 mm gives enough reserve
to close target0 and continue to target2.

## 1123: Coordinate Optimizer Variable-Depth/Radius Seed365435296162 Target0 Sources=8 Tx/Rx=45 Ringdown050

Output:

```text
outputs/experiments/1123_coordinate_optimizer_variable_depth_radius_seed365435296162_target0_sources8_txrx45_ringdown050_objectives
```

## Results

Run 1123 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 45.0
absolute radius margin: 5.281512e-04
offset from cutoff: +2.815119e-05
relative margin: 2.487968e-02
confidence label: moderate
fallback warning: none
best misfit: 2.122821e-02
next radius misfit: 2.175636e-02
```

Diagnostic objective margins:

```text
base       5.281512e-04  above cutoff
highband   7.298394e-04  above cutoff
late       4.579559e-04  weak, below cutoff
late_high  5.121683e-04  above cutoff
veryhigh   7.277239e-04  above cutoff
early_high 5.886654e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
distinct-radius competitor remains `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.00 mm` at `z=81 mm`.

## Interpretation

Tx/Rx=45 is the strongest tested seed365435296162 target0 acquisition point.
It improves the base margin by about `2.32e-05` over Tx/Rx=50, `3.39e-05` over
Tx/Rx=52.5, and `6.57e-05` over Tx/Rx=60. Late remains below cutoff, but
late_high now clears, and every diagnostic objective preserves the true
geometry.

Stop the target0 acquisition sweep here. Close target0 as exact and accepted
with a residual late-window caveat, then continue seed365435296162 with target2
at the standard 5-source Tx/Rx=60 control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png unique=338 nonwhite_fraction=0.3425
figure validation: coordinate_radius_decision_panel.png unique=835 nonwhite_fraction=0.1758
figure validation: coordinate_objective_radius_candidates.png unique=3019 nonwhite_fraction=0.0679
figure validation: system_scene_geometry.png unique=2100 nonwhite_fraction=0.6307
visual inspection: decision panel shows exact selected r=5.00 mm, base above cutoff, late_high above cutoff, and only late below cutoff
metadata validation: tx_rx_offset_mm is 45.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in about 532 s
```

## Next Decision

Continue seed365435296162 with target2 at the standard 5-source Tx/Rx=60
control under the same ringdown050 objective suite.
