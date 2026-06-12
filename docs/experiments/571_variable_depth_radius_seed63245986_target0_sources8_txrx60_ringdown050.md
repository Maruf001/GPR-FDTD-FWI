# Experiment 571: Seed63245986 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Start the seed63245986 branch with the target0 8-source Tx/Rx=60 control after
closing seed39088169.

## 1037: Coordinate Optimizer Variable-Depth/Radius Seed63245986 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1037_coordinate_optimizer_variable_depth_radius_seed63245986_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed63245986:1.1,-50.0,1.1,0.10,63245986,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed63245986 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed63245986_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1037 is exact and base-accepted with a small reserve and late-window
caveats:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.107136e-04
offset from cutoff: +1.071355e-05
relative margin: 3.221568e-02
confidence label: moderate
fallback warning: none
best misfit: 1.585295e-02
next radius misfit: 1.636366e-02
elapsed: 568.8 s
```

Diagnostic objective margins:

```text
base       5.107136e-04  above cutoff
highband   6.835769e-04  above cutoff
late       3.496583e-04  below cutoff
late_high  4.513516e-04  below cutoff
veryhigh   6.166947e-04  above cutoff
early_high 5.573153e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

Seed63245986 target0 is accepted at the planned 8-source Tx/Rx=60 control, but
the base reserve is smaller than the previous seed39088169 target0 branch.
Late and late_high are again below cutoff while still ranking the exact
geometry first.

Carry both caveats forward: target0 has a small base margin reserve and weak
late-window diagnostics. Continue with target2 at the standard 5-source
Tx/Rx=60 control before deciding whether this seed requires any later cleanup.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.240932 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target0 row just above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91%; system memory remained near 95 GiB available
```

## Next Decision

Run seed63245986 target2 with 5 sources and Tx/Rx=60. That control is
experiment 1038.
