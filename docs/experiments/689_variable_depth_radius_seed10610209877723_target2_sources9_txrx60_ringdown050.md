# Experiment 689: Seed10610209877723 Target2 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Escalate seed10610209877723 target2 to the standard 9-source Tx/Rx=60
source-density test after both the 5-source control and 7-source bracket
selected the exact geometry but remained weak.

## 1152: Coordinate Optimizer Variable-Depth/Radius Seed10610209877723 Target2 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1152_coordinate_optimizer_variable_depth_radius_seed10610209877723_target2_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1152 selected the exact geometry but remains a near miss:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 4.831448e-04
offset from cutoff: -1.685516e-05
relative margin: 3.069518e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.574009e-02
next radius misfit: 1.622323e-02
elapsed: 697.8 s
```

Diagnostic objective margins:

```text
base       4.831448e-04  below cutoff
highband   6.246251e-04  above cutoff
late       7.201825e-04  above cutoff
late_high  7.736749e-04  above cutoff
veryhigh   6.457343e-04  above cutoff
early_high 4.468847e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
distinct-radius and changed-geometry competitor is `r=8.75 mm` at `z=121 mm`.

## Interpretation

The 9-source escalation improves over both lower source-count rows but still
misses cutoff:

```text
5 sources, Tx/Rx=60  base margin 4.719e-04
7 sources, Tx/Rx=60  base margin 4.449e-04
9 sources, Tx/Rx=60  base margin 4.831e-04
```

Because this is a target2 near miss at the standard 9-source level, follow the
seed610/20365011074/53316291173/86267571272 precedent with one 11-source
Tx/Rx=60 closeout test before declaring the simple source-density ladder
unresolved.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3121 and unique_colors=233
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1676 and unique_colors=857
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and unique_colors=2990
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6336 and unique_colors=2135
figure notes: figures/FIGURE_NOTES.md present, lists base and early_high below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 697.8 s through the candidate sweep
```

## Next Decision

Run seed10610209877723 target2 with 11 sources and Tx/Rx=60 as a closeout of
the simple source-density ladder.
