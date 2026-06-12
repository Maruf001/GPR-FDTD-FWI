# Experiment 656: Seed365435296162 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

## Purpose

Run the first acquisition-offset probe for seed365435296162 target0. Run 1120
was exact but weak at the standard 8-source Tx/Rx=60 control, so this run keeps
the source count fixed and reduces Tx/Rx to 52.5 mm.

## 1121: Coordinate Optimizer Variable-Depth/Radius Seed365435296162 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1121_coordinate_optimizer_variable_depth_radius_seed365435296162_target0_sources8_txrx52p5_ringdown050_objectives
```

## Results

Run 1121 is exact but still weak, although substantially improved:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 52.5
absolute radius margin: 4.942808e-04
offset from cutoff: -5.719247e-06
relative margin: 2.699896e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.830740e-02
next radius misfit: 1.880168e-02
```

Diagnostic objective margins:

```text
base       4.942808e-04  weak, just below cutoff
highband   6.554093e-04  above cutoff
late       3.765105e-04  weak, below cutoff
late_high  4.172790e-04  weak, below cutoff
veryhigh   6.278637e-04  above cutoff
early_high 5.423760e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
distinct-radius competitor remains `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.00 mm` at `z=81 mm`.

## Interpretation

Tx/Rx=52.5 improves the base margin by about `3.18e-05` relative to the
Tx/Rx=60 control, reducing the cutoff deficit from `3.76e-05` to `5.72e-06`.
Because the acquisition probe improved the row rather than worsening it, follow
the seed5702887 acquisition-bracket precedent and test Tx/Rx=50 before changing
source density.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png unique=233 nonwhite_fraction=0.3231
figure validation: coordinate_radius_decision_panel.png unique=812 nonwhite_fraction=0.1616
figure validation: coordinate_objective_radius_candidates.png unique=3174 nonwhite_fraction=0.0679
figure validation: system_scene_geometry.png unique=2148 nonwhite_fraction=0.6336
visual inspection: decision panel shows exact selected r=5.00 mm and base just below cutoff
metadata validation: tx_rx_offset_mm is 52.5; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in about 576 s
```

## Next Decision

Run seed365435296162 target0 with 8 sources and Tx/Rx=50. If Tx/Rx=50 clears
the base cutoff with useful reserve, compare to the seed5702887 lower-edge
precedent before closing target0. If it weakens, switch mechanism rather than
sweeping offsets blindly.
