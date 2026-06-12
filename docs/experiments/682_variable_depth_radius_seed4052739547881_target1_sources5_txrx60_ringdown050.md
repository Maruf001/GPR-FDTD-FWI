# Experiment 682: Seed4052739547881 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Complete seed4052739547881 after target0 passed the standard 8-source Tx/Rx=60
control with a late-window caveat and target2 passed cleanly at the standard
5-source Tx/Rx=60 control. This run tests target1 at the standard 5-source
Tx/Rx=60 control under the ringdown050 source-mismatch/noise condition.

## 1145: Coordinate Optimizer Variable-Depth/Radius Seed4052739547881 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1145_coordinate_optimizer_variable_depth_radius_seed4052739547881_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1145 is exact and accepted cleanly:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.236399e-04
offset from cutoff: +2.363986e-05
relative margin: 3.067307e-02
confidence label: moderate
fallback warning: none
best misfit: 1.707165e-02
next radius misfit: 1.759529e-02
elapsed: 366.7 s
```

Diagnostic objective margins:

```text
base       5.236399e-04  above cutoff
highband   6.937423e-04  above cutoff
late       7.929946e-04  above cutoff
late_high  9.312597e-04  above cutoff
veryhigh   6.021862e-04  above cutoff
early_high 5.075134e-04  above cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
distinct-radius competitor is `r=6.25 mm`; the closest changed-geometry
competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

Target1 passes cleanly at the standard 5-source Tx/Rx=60 control. This closes
seed4052739547881:

```text
target0: accepted at 8-source Tx/Rx=60, with recurring late-window caveat
target2: accepted cleanly at 5-source Tx/Rx=60
target1: accepted cleanly at 5-source Tx/Rx=60
```

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3371 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1621 and unique_colors=869
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and unique_colors=3016
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6308 and unique_colors=2063
figure notes: figures/FIGURE_NOTES.md present, lists no objective variants below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 366.7 s through the candidate sweep
```

## Next Decision

Continue the Fibonacci replication chain with seed6557470329842 target0. Seed
validation succeeded in the active FNO environment:

```text
np.random.default_rng(6557470329842) succeeded
```
