# Experiment 697: Seed17167680207565 Target1 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Run the seed17167680207565 target1 9-source Tx/Rx=60 rescue after the standard
5-source control selected the exact geometry but remained weak.

## 1160: Coordinate Optimizer Variable-Depth/Radius Seed17167680207565 Target1 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1160_coordinate_optimizer_variable_depth_radius_seed17167680207565_target1_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1160 selected the exact geometry and clears the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 5.549433e-04
offset from cutoff: +5.494335e-05
relative margin: 3.472372e-02
confidence label: moderate
fallback warning: none
best misfit: 1.598168e-02
next radius misfit: 1.653662e-02
elapsed: 670.1 s
```

Diagnostic objective margins:

```text
base       5.549433e-04  above cutoff
highband   7.747011e-04  above cutoff
late       8.074528e-04  above cutoff
late_high  1.033725e-03  above cutoff
veryhigh   7.055423e-04  above cutoff
early_high 5.894972e-04  above cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
base objective distinct-radius competitor is `r=6.25 mm` at the same depth,
and the closest changed-geometry competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

The 9-source rescue resolves the weak target1 control:

```text
5 sources, Tx/Rx=60  base margin 4.758e-04
9 sources, Tx/Rx=60  base margin 5.549e-04
```

This closes seed17167680207565 without a separate numbered summary output
folder:

```text
target0: exact, accepted at 8-source Tx/Rx=60 with recurring late-window caveat
target2: exact, rescued cleanly by 9-source Tx/Rx=60 after weak 5/7 controls
target1: exact, rescued cleanly by 9-source Tx/Rx=60 after weak 5-source control
```

The next seed in the Fibonacci replication chain is `27777890085288`; NumPy
validated `np.random.default_rng(27777890085288)` in the active FNO
environment.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3524 and sampled_unique_colors=289
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1785 and sampled_unique_colors=371
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and sampled_unique_colors=1144
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6335 and sampled_unique_colors=1075
figure notes: figures/FIGURE_NOTES.md present, reports one moderate row and no objective variants below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 670.1 s through the candidate sweep
next seed validation: np.random.default_rng(27777890085288) succeeds
```

## Next Decision

Continue the Fibonacci replication chain with seed27777890085288 target0 using
the standard 8-source Tx/Rx=60 control.
