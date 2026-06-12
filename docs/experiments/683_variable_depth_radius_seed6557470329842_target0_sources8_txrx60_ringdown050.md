# Experiment 683: Seed6557470329842 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Start the seed6557470329842 Fibonacci branch after seed4052739547881 closed.
This run tests target0 at the standard 8-source Tx/Rx=60 control under the
ringdown050 source-mismatch/noise condition.

## 1146: Coordinate Optimizer Variable-Depth/Radius Seed6557470329842 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1146_coordinate_optimizer_variable_depth_radius_seed6557470329842_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1146 is exact and accepted cleanly:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.920872e-04
offset from cutoff: +9.208721e-05
relative margin: 3.704609e-02
confidence label: moderate
fallback warning: none
best misfit: 1.598245e-02
next radius misfit: 1.657454e-02
elapsed: 569.0 s
```

Diagnostic objective margins:

```text
base       5.920872e-04  above cutoff
highband   7.587717e-04  above cutoff
late       5.076346e-04  above cutoff
late_high  5.891226e-04  above cutoff
veryhigh   7.230104e-04  above cutoff
early_high 6.350128e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
distinct-radius competitor is `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.0 mm` at `z=81 mm`.

## Interpretation

Target0 passes cleanly at the standard 8-source Tx/Rx=60 control. Unlike many
target0 rows, late and late_high also clear cutoff, so no late-window caveat is
needed for this target. Continue seed6557470329842 with target2 at the
standard 5-source Tx/Rx=60 control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3766 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2128x1583 RGB with nonwhite_fraction=0.1893 and unique_colors=846
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and unique_colors=3167
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6309 and unique_colors=2129
figure notes: figures/FIGURE_NOTES.md present, lists no objective variants below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 569.0 s through the candidate sweep
```

## Next Decision

Run seed6557470329842 target2 with 5 sources and Tx/Rx=60.
