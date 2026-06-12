# Experiment 570: Seed39088169 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run the seed39088169 target1 standard control after target0 accepted with a
late-window caveat and target2 accepted with an early_high caveat.

## 1036: Coordinate Optimizer Variable-Depth/Radius Seed39088169 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1036_coordinate_optimizer_variable_depth_radius_seed39088169_target1_sources5_txrx60_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 60 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 150,250,350 \
  --initial-z-values-mm 80,100,120 \
  --initial-radius-values-mm 5,6,8 \
  --target-indices 1 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed39088169_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1036 is exact and base-accepted with a narrow early_high caveat:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.481852e-04
offset from cutoff: +4.818516e-05
relative margin: 3.242624e-02
confidence label: moderate
fallback warning: none
best misfit: 1.690560e-02
next radius misfit: 1.745379e-02
elapsed: 365.1 s
```

Diagnostic objective margins:

```text
base       5.481852e-04  above cutoff
highband   6.901726e-04  above cutoff
late       8.156615e-04  above cutoff
late_high  8.881424e-04  above cutoff
veryhigh   6.408418e-04  above cutoff
early_high 4.986964e-04  below cutoff
```

All six objective variants rank the true target1 geometry first.

## Interpretation

Target1 is accepted at the standard 5-source Tx/Rx=60 control. The only
diagnostic caveat is early_high, which misses the 5.0e-4 working cutoff by
about 1.30e-06 while still ranking the true geometry first. Because the base
margin has a 4.82e-05 reserve and the other diagnostic variants clear cutoff,
no target1 rescue is needed for this seed.

This closes the seed39088169 branch:

```text
target0: accepted at 8-source Tx/Rx=60 with late-window caveats.
target2: accepted at 5-source Tx/Rx=60 with an early_high caveat.
target1: accepted at 5-source Tx/Rx=60 with a narrow early_high caveat.
```

Continue the Fibonacci replication chain with seed63245986 target0 at
8 sources and Tx/Rx=60.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.256234 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target1 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88%; system memory remained near 95 GiB available
```

## Next Decision

Run seed63245986 target0 with 8 sources and Tx/Rx=60. That control is
experiment 1037.
