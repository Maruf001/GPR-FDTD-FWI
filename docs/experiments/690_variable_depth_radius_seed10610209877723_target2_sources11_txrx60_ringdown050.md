# Experiment 690: Seed10610209877723 Target2 Sources=11 Tx/Rx=60 Ringdown050

## Purpose

Close the seed10610209877723 target2 source-density ladder with an 11-source
Tx/Rx=60 test after 5-, 7-, and 9-source runs all selected the exact geometry
but stayed below the moderate radius-margin cutoff.

## 1153: Coordinate Optimizer Variable-Depth/Radius Seed10610209877723 Target2 Sources=11 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1153_coordinate_optimizer_variable_depth_radius_seed10610209877723_target2_sources11_txrx60_ringdown050_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml --grid-step-mm 1.0 --sources 11 --tx-rx-offset-mm 60 --frequency-ghz 1.5 --true-x-values-mm 150,250,350 --true-z-values-mm 80,100,120 --truth-radius-values-mm 5,6,8 --initial-x-values-mm 150,250,350 --initial-z-values-mm 80,100,120 --initial-radius-values-mm 5,6,8 --target-indices 2 --passes 1 --x-offsets-mm=0 --z-offsets-mm=0:1:1 --radius-offsets-mm=0:1.25:0.25 --replication-cases source_mismatch_ringdown050_noise10_seed10610209877723:1.1,-50.0,1.1,0.10,10610209877723,0.5,180.0,0.8 --update-case-label source_mismatch_ringdown050_noise10_seed10610209877723 --source-frequency-scales 0.9,1.0,1.1 --fit-ringdown-coefficient --source-ringdown-delay-ps 180.0 --source-ringdown-frequency-scale 0.8 --source-time-shift-ps-values=-50,0,50 --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' --top-k 12 --progress-every 2 --run-name coordinate_optimizer_variable_depth_radius_seed10610209877723_target2_sources11_txrx60_ringdown050_objectives
```

## Results

Run 1153 selected the exact geometry, but the base margin remains weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 11
tx_rx_offset_mm: 60.0
absolute radius margin: 4.076261e-04
offset from cutoff: -9.237387e-05
relative margin: 2.779939e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.466313e-02
next radius misfit: 1.507076e-02
elapsed: 883.5 s
```

Diagnostic objective margins:

```text
base       4.076261e-04  below cutoff
highband   5.210651e-04  above cutoff
late       5.469874e-04  above cutoff
late_high  5.996396e-04  above cutoff
veryhigh   5.132683e-04  above cutoff
early_high 3.830658e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
base objective distinct-radius and changed-geometry competitor is `r=8.75 mm`
at `z=121 mm`.

## Interpretation

The simple source-density ladder preserves the truth but does not monotonically
increase the base margin:

```text
5 sources, Tx/Rx=60   base margin 4.719e-04
7 sources, Tx/Rx=60   base margin 4.449e-04
9 sources, Tx/Rx=60   base margin 4.831e-04
11 sources, Tx/Rx=60  base margin 4.076e-04
```

This closes target2 as a truth-preserving but weak-base result rather than a
clean accepted result. The evidence is still useful: the exact radius/depth is
ranked first by every objective variant after four source-density levels, and
the highband, late, late_high, and veryhigh diagnostics clear the cutoff. The
remaining caveat is that the base and early_high windows do not separate
`r=8.0 mm` from the nearby `r=8.75 mm, z=121 mm` competitor strongly enough to
claim moderate point-radius confidence.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.2686 and sampled_unique_colors=227
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.2029 and sampled_unique_colors=464
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and sampled_unique_colors=1148
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6336 and sampled_unique_colors=1095
figure notes: figures/FIGURE_NOTES.md present, lists base and early_high below moderate cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=11; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 883.5 s through the candidate sweep
```

## Next Decision

Continue seed10610209877723 with target1 at the standard 5-source Tx/Rx=60
control. Do not extend target2 further until a later targeted study adds a new
dimension beyond simple source density, such as aperture geometry, objective
weighting, or interval reporting.
