# Experiment 560: Seed14930352 Target0 Sources=11 Tx/Rx=60 Ringdown050

## Purpose

Run the final source-density escalation for seed14930352 target0 after
8-source Tx/Rx=60, 8-source Tx/Rx=52.5, and 9-source Tx/Rx=60 were all exact
but weak.

## 1026: Coordinate Optimizer Variable-Depth/Radius Seed14930352 Target0 Sources=11 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1026_coordinate_optimizer_variable_depth_radius_seed14930352_target0_sources11_txrx60_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 11 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed14930352:1.1,-50.0,1.1,0.10,14930352,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed14930352 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed14930352_target0_sources11_txrx60_ringdown050_objectives
```

## Results

Run 1026 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 11
tx_rx_offset_mm: 60.0
absolute radius margin: 4.500005e-04
offset from cutoff: -4.999952e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 863.7 s
```

Diagnostic objective margins:

```text
base       4.500005e-04  below cutoff by 4.999952e-05
highband   5.731147e-04  above cutoff
late       3.562438e-04  below cutoff by 1.437562e-04
late_high  3.869276e-04  below cutoff by 1.130724e-04
veryhigh   5.554823e-04  above cutoff
early_high 4.962452e-04  below cutoff by 3.754811e-06
```

All six objective variants rank the true target0 geometry first.

## Interpretation

The 11-source escalation does not rescue seed14930352 target0. It is the
weakest base row among the tested target0 mechanisms:

```text
1023: 8 sources,  Tx/Rx=60.0   base=4.932234e-04
1024: 8 sources,  Tx/Rx=52.5   base=4.842836e-04
1025: 9 sources,  Tx/Rx=60.0   base=4.784595e-04
1026: 11 sources, Tx/Rx=60.0   base=4.500005e-04
```

Stop seed14930352 target0 escalation for now. The target is exact and
truth-ranked under every tested objective, but base confidence remains weak
after the acquisition probe and source-density bracket. Continue the branch
with target2 at the standard 5-source Tx/Rx=60 control; keep target0 marked
unresolved rather than burying it under more ad hoc rescue runs.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.214746 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target0 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=11; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 93%; nvidia-smi process memory was about 333 MiB
```

## Next Decision

Run seed14930352 target2 with 5 sources and Tx/Rx=60. That control is
experiment 1027.
