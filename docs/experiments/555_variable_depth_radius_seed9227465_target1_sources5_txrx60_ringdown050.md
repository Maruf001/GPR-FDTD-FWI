# Experiment 555: Seed9227465 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Test the seed9227465 target1 control at the standard 5-source Tx/Rx=60 setting
after target0 was base-accepted with a late-window caveat and target2 was
cleanly accepted.

## 1021: Coordinate Optimizer Variable-Depth/Radius Seed9227465 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1021_coordinate_optimizer_variable_depth_radius_seed9227465_target1_sources5_txrx60_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed9227465_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1021 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 4.964603e-04
offset from cutoff: -3.539731e-06
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 366.7 s
```

Diagnostic objective margins:

```text
base       4.964603e-04  below cutoff by 3.539731e-06
highband   6.423867e-04  above cutoff
late       7.663228e-04  above cutoff
late_high  8.729030e-04  above cutoff
veryhigh   5.963128e-04  above cutoff
early_high 4.696610e-04  below cutoff by 3.033902e-05
```

All six objective variants rank the true target1 geometry first.

## Interpretation

The target1 control is not accepted even though it is exact and
truth-preserving. The miss is narrow for the base objective, only
3.539731e-06 below cutoff, but early_high is also weak. This is closer to the
target1 rescue cases than to a geometry failure.

The next rescue should be the 5-source Tx/Rx=52.5 acquisition probe. That is
the least speculative first intervention because it rescued seed2178309
target1, was clean for seed1346269 target1, and costs less than immediate
source-density escalation. If Tx/Rx=52.5 fails for seed9227465 target1, then
a source-density or combined-policy rescue is justified.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.237207 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target1 row just below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88%; nvidia-smi process memory was about 252 MiB
```

## Next Decision

Run seed9227465 target1 with 5 sources and Tx/Rx=52.5. That production GPU
rescue is experiment 1022.
