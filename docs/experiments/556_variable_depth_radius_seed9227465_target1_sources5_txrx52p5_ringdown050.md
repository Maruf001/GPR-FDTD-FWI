# Experiment 556: Seed9227465 Target1 Sources=5 Tx/Rx=52.5 Ringdown050

## Purpose

Run a targeted acquisition rescue for seed9227465 target1 after the standard
5-source Tx/Rx=60 control was exact but weak by 3.539731e-06 on the base
objective.

## 1022: Coordinate Optimizer Variable-Depth/Radius Seed9227465 Target1 Sources=5 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1022_coordinate_optimizer_variable_depth_radius_seed9227465_target1_sources5_txrx52p5_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 52.5 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed9227465:1.1,-50.0,1.1,0.10,9227465,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed9227465 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed9227465_target1_sources5_txrx52p5_ringdown050_objectives
```

## Results

Run 1022 is exact and base-accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 52.5
absolute radius margin: 5.043777e-04
offset from cutoff: +4.377660e-06
confidence label: moderate
fallback warning: none
elapsed: 363.4 s
```

Diagnostic objective margins:

```text
base       5.043777e-04  above cutoff
highband   6.677380e-04  above cutoff
late       7.883081e-04  above cutoff
late_high  8.615534e-04  above cutoff
veryhigh   6.060802e-04  above cutoff
early_high 4.557493e-04  below cutoff by 4.425073e-05
```

All six objective variants rank the true target1 geometry first.

## Interpretation

Tx/Rx=52.5 rescues seed9227465 target1 base confidence without increasing
source density. The reserve is small, so this is an accepted but caveated
target1 policy rather than a clean row. The remaining caveat is early_high,
which is below cutoff while still ranking the true geometry first.

Seed9227465 branch summary:

```text
target0: accepted at 8 sources and Tx/Rx=60; late and late_high caveats remain.
target2: cleanly accepted at 5 sources and Tx/Rx=60.
target1: Tx/Rx=60 control was exact but weak; Tx/Rx=52.5 accepted base
         confidence with an early_high caveat and a razor base reserve.
```

Do not run an immediate 9-source target1 cleanup. The accepted 5-source
Tx/Rx=52.5 result matches the seed2178309 precedent, where the branch carried
an early_high caveat; source-density escalation is reserved for cases like
seed832040 where 5-source acquisition rows remained weak.

Continue the Fibonacci replication chain with seed14930352 target0 at
8 sources and Tx/Rx=60.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.240813 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target1 row just above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88-89%; nvidia-smi process memory was about 252 MiB
```

## Next Decision

Run seed14930352 target0 with 8 sources and Tx/Rx=60. That production GPU run
is experiment 1023.
