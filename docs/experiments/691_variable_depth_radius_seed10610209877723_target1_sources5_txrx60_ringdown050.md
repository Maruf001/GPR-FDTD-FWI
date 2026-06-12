# Experiment 691: Seed10610209877723 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run the standard target1 5-source Tx/Rx=60 control for seed10610209877723 after
target0 was accepted and target2 was closed as a truth-preserving weak-margin
source-density ladder.

## 1154: Coordinate Optimizer Variable-Depth/Radius Seed10610209877723 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1154_coordinate_optimizer_variable_depth_radius_seed10610209877723_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1154 selected the exact geometry and clears the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.238657e-04
offset from cutoff: +2.386570e-05
relative margin: 3.040746e-02
confidence label: moderate
fallback warning: none
best misfit: 1.722819e-02
next radius misfit: 1.775206e-02
elapsed: 379.9 s
```

Diagnostic objective margins:

```text
base       5.238657e-04  above cutoff
highband   6.966284e-04  above cutoff
late       7.701255e-04  above cutoff
late_high  8.706999e-04  above cutoff
veryhigh   6.471972e-04  above cutoff
early_high 5.054210e-04  above cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
base objective distinct-radius competitor is `r=6.25 mm` at the same depth,
and the closest changed-geometry competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

This is a clean target1 acceptance. It closes seed10610209877723 as:

```text
target0: exact, accepted at 8-source Tx/Rx=60 with recurring late-window caveat
target2: exact across 5/7/9/11 sources but weak-base; truth-preserving weak-margin closeout
target1: exact, accepted at 5-source Tx/Rx=60 with all diagnostics above cutoff
```

The next seed in the Fibonacci replication chain is `17167680207565`; NumPy
validated `np.random.default_rng(17167680207565)` in the active FNO
environment.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3347 and sampled_unique_colors=290
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1670 and sampled_unique_colors=371
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and sampled_unique_colors=1146
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6335 and sampled_unique_colors=1039
figure notes: figures/FIGURE_NOTES.md present, reports one moderate row and no objective variants below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 379.9 s through the candidate sweep
next seed validation: np.random.default_rng(17167680207565) succeeds
```

## Next Decision

Continue the Fibonacci replication chain with seed17167680207565 target0 using
the standard 8-source Tx/Rx=60 control.
