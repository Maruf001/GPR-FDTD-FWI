# Experiment 702: Seed27777890085288 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run the standard target1 5-source Tx/Rx=60 control for seed27777890085288 after
target0 was accepted and target2 was rescued by a 9-source escalation.

## 1165: Coordinate Optimizer Variable-Depth/Radius Seed27777890085288 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1165_coordinate_optimizer_variable_depth_radius_seed27777890085288_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1165 selected the exact geometry and clears the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 6.079749e-04
offset from cutoff: +1.079749e-04
relative margin: 3.594375e-02
confidence label: moderate
fallback warning: none
best misfit: 1.691462e-02
next radius misfit: 1.752259e-02
elapsed: 378.2 s
```

Diagnostic objective margins:

```text
base       6.079749e-04  above cutoff
highband   8.032063e-04  above cutoff
late       9.735952e-04  above cutoff
late_high  1.099637e-03  above cutoff
veryhigh   7.853863e-04  above cutoff
early_high 5.852483e-04  above cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
base objective distinct-radius competitor is `r=6.25 mm` at the same depth,
and the closest changed-geometry competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

This is a clean target1 acceptance. It closes seed27777890085288 without a
separate numbered summary output folder:

```text
target0: exact, accepted at 8-source Tx/Rx=60 with recurring late-window caveat
target2: exact, accepted by 9-source Tx/Rx=60 after near-miss 5-source and weak 7-source controls
target1: exact, accepted cleanly at 5-source Tx/Rx=60
```

The next seed in the Fibonacci replication chain is `44945570292853`; NumPy
validated `np.random.default_rng(44945570292853)` in the active FNO
environment.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3822 and sampled_unique_colors=289
figure validation: coordinate_radius_decision_panel.png is 2128x1583 RGB with nonwhite_fraction=0.1766 and sampled_unique_colors=384
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and sampled_unique_colors=1144
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6339 and sampled_unique_colors=1045
figure notes: figures/FIGURE_NOTES.md present, reports one moderate row and no objective variants below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 378.2 s through the candidate sweep
next seed validation: np.random.default_rng(44945570292853) succeeds
```

## Next Decision

Continue the Fibonacci replication chain with seed44945570292853 target0 using
the standard 8-source Tx/Rx=60 control.
