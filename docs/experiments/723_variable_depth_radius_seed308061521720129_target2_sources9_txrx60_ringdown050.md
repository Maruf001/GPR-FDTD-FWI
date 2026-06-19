# Experiment 723: Seed308061521720129 Target2 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Escalate the unresolved seed308061521720129 target2 source-density bracket to
9 sources after the 5-source and 7-source controls both selected the exact
geometry but remained below the moderate confidence cutoff.

## 1186: Coordinate Optimizer Variable-Depth/Radius Seed308061521720129 Target2 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1186_coordinate_optimizer_variable_depth_radius_seed308061521720129_target2_sources9_txrx60_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 9 \
  --tx-rx-offset-mm 60 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 150,250,350 \
  --initial-z-values-mm 80,100,120 \
  --initial-radius-values-mm 5,6,8 \
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown050_noise10_seed308061521720129:1.1,-50.0,1.1,0.10,308061521720129,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed308061521720129 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed308061521720129_target2_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1186 selected the exact geometry but remained weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 4.443570e-04
offset from cutoff: -5.564299e-05
relative margin: 2.836706e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.566454e-02
next radius misfit: 1.610890e-02
elapsed: 673.4 s
```

Diagnostic objective margins:

```text
base       4.443570e-04  below cutoff
highband   6.014535e-04  above cutoff
late       6.530188e-04  above cutoff
late_high  7.827925e-04  above cutoff
veryhigh   6.076647e-04  above cutoff
early_high 4.160940e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
base objective distinct-radius competitor is `r=8.75 mm` at `z=121 mm`, which
is also the closest changed-geometry competitor.

## Interpretation

The 9-source escalation does not rescue target2 point-radius confidence. Across
the 5-, 7-, and 9-source target2 probes for this seed, the exact geometry is
stable and rank 1 for every diagnostic objective, but the base margins stay
below cutoff (`4.91e-04`, `4.51e-04`, `4.44e-04`) and early_high remains weak.
Carry target2 as an exact geometry with weak point-radius confidence and use
the observed nearest competitor (`r=8.75 mm`, `z=121 mm`) as the practical
upper-side ambiguity reference. Do not spend another source-density run on
target2 before testing target1.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.2801 and sampled_unique_colors=78
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1733 and sampled_unique_colors=84
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0618 and sampled_unique_colors=157
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6260 and sampled_unique_colors=107
figure notes: figures/FIGURE_NOTES.md present, reports one weak row and lists base and early_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 673.4 s through the candidate sweep
```

## Next Decision

Continue seed308061521720129 with target1 at the standard 5-source Tx/Rx=60
control.

## 2026-06-17 Addendum

A target2 Tx/Rx=50 acquisition-offset replication probe has now been run:

```text
run:      1226_coordinate_optimizer_variable_depth_radius_seed308061521720129_target2_sources5_txrx50_ringdown050_objectives
target:   target2
sources:  5
Tx/Rx:    50.0 mm
```

Run 1226 preserved exact x/z/r geometry, but it did not rescue the strict base
margin:

| Run | Sources | Tx/Rx mm | Base margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1184 | 5 | 60.0 | 4.908834e-4 | -9.117e-6 | weak near-miss |
| 1185 | 7 | 60.0 | 4.508691e-4 | -4.913e-5 | weak |
| 1186 | 9 | 60.0 | 4.443570e-4 | -5.564e-5 | weak |
| 1226 | 5 | 50.0 | 4.707138e-4 | -2.929e-5 | weak |

This failed replication is useful: Tx/Rx=50 rescued seed20365011074 target2,
but it is not a universal target2 weak-branch remedy.
