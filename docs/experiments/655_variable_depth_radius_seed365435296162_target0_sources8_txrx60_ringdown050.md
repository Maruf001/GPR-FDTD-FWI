# Experiment 655: Seed365435296162 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Resume the Fibonacci replication chain after the field-data intake/QC pause.
This run tests seed365435296162 target0 at the standard 8-source Tx/Rx=60
control under the ringdown050 source-mismatch/noise condition.

Seed validation:

```text
np.random.default_rng(365435296162) succeeded in the active FNO environment.
```

## 1120: Coordinate Optimizer Variable-Depth/Radius Seed365435296162 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1120_coordinate_optimizer_variable_depth_radius_seed365435296162_target0_sources8_txrx60_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 8 \
  --tx-rx-offset-mm 60 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 150,250,350 \
  --initial-z-values-mm 80,100,120 \
  --initial-radius-values-mm 5,6,8 \
  --target-indices 0 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown050_noise10_seed365435296162:1.1,-50.0,1.1,0.10,365435296162,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed365435296162 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed365435296162_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1120 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 4.624478e-04
offset from cutoff: -3.755221e-05
relative margin: 2.947461e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.568970e-02
next radius misfit: 1.615215e-02
```

Diagnostic objective margins:

```text
base       4.624478e-04  weak, below cutoff
highband   5.888621e-04  above cutoff
late       3.471904e-04  weak, below cutoff
late_high  3.897570e-04  weak, below cutoff
veryhigh   5.788499e-04  above cutoff
early_high 4.938086e-04  weak, just below cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
distinct-radius competitor is `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.00 mm` at `z=81 mm`.

## Interpretation

The state recovery is exact, but target0 cannot be accepted at the standard
Tx/Rx=60 control because the base margin is below the `5.0e-4` cutoff and the
late-window diagnostics are also weak. This matches the recent
acquisition-sensitive target0 pattern from seeds701408733 and 7778742049.

Do not close seed365435296162 target0 yet. The established next action is the
8-source Tx/Rx=52.5 acquisition probe before moving to target2.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png unique=235 nonwhite_fraction=0.3045
figure validation: coordinate_radius_decision_panel.png unique=794 nonwhite_fraction=0.1754
figure validation: coordinate_objective_radius_candidates.png unique=3161 nonwhite_fraction=0.0679
figure validation: system_scene_geometry.png unique=1843 nonwhite_fraction=0.5402
visual inspection: decision panel shows selected r=5.00 mm, next r=5.25 mm, competing geometry r=6.00 mm at z=81 mm, and base below cutoff
visual inspection: scene geometry figure includes bar-top cover and Tx-Rx offset callouts
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in about 604 s
```

## Next Decision

Run seed365435296162 target0 with 8 sources and Tx/Rx=52.5 as the acquisition
probe. Do not move to target2 until target0 is accepted or explicitly marked
unresolved under the established rescue policy.
