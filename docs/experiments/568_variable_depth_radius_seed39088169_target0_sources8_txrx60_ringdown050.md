# Experiment 568: Seed39088169 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Start the seed39088169 branch with the target0 8-source Tx/Rx=60 control after
closing seed24157817.

## 1034: Coordinate Optimizer Variable-Depth/Radius Seed39088169 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1034_coordinate_optimizer_variable_depth_radius_seed39088169_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed39088169:1.1,-50.0,1.1,0.10,39088169,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed39088169 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed39088169_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1034 is exact and base-accepted with late-window caveats:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.545304e-04
offset from cutoff: +5.453038e-05
relative margin: 3.472376e-02
confidence label: moderate
fallback warning: none
best misfit: 1.596977e-02
next radius misfit: 1.652430e-02
elapsed: 573.3 s
```

Diagnostic objective margins:

```text
base       5.545304e-04  above cutoff
highband   7.356704e-04  above cutoff
late       3.832558e-04  below cutoff
late_high  4.605248e-04  below cutoff
veryhigh   7.132365e-04  above cutoff
early_high 6.147796e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

Seed39088169 target0 is accepted at the planned 8-source Tx/Rx=60 control. As
with several earlier target0 branches, late and late_high remain below the
working cutoff even though they keep the exact target0 geometry ranked first.

Do not run a target0 rescue at this point. Carry the late-window caveat forward
and continue the branch with target2 at the standard 5-source Tx/Rx=60
control.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.258960 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target0 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91%; system memory remained near 95 GiB available
```

## Next Decision

Run seed39088169 target2 with 5 sources and Tx/Rx=60. That control is
experiment 1035.
