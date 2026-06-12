# Experiment 406: Seed55 Target-1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 872 completes the seed55 target-specific policy set by testing target 1
with the 5-source full-ringdown050 policy.

## 872: Coordinate Optimizer Variable-Depth/Radius Seed55 Target-1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/872_coordinate_optimizer_variable_depth_radius_seed55_target1_sources5_txrx60_ringdown050_objectives
```

Command:

```text
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
  --replication-cases source_mismatch_ringdown050_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed55 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed55_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 872 is exact and accepted:

```text
target: 1
sources: 5
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.506251e-04
offset from cutoff: +5.063e-05
confidence label: moderate
fallback warning: none
elapsed: 364.59 s
```

Diagnostic objective rows all preserve the true target-1 geometry and all clear
cutoff:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.506251e-04 | above cutoff |
| highband | 7.372422e-04 | above cutoff |
| late | 8.415132e-04 | above cutoff |
| late_high | 9.673456e-04 | above cutoff |
| veryhigh | 6.631702e-04 | above cutoff |
| early_high | 5.474839e-04 | above cutoff |

## Interpretation

Seed55 passes all three promoted full-ringdown050 policy rows:

| Target | Run | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 870 | 8 | 5.079048e-04 | +7.905e-06 | accepted |
| 1 | 872 | 5 | 5.506251e-04 | +5.063e-05 | accepted |
| 2 | 871 | 5 | 5.677153e-04 | +6.772e-05 | accepted |

Seed55 therefore joins seed13 as an `8/5/5` full-ringdown050 seed, while
seed89 and seed34 remain `8/5/9` and seed21 remains target-0 limited below
ringdown050.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.278334 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row above the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target1 truth_radius_mm is 6.0 mm
source validation: all six diagnostic objectives preserve target1 truth geometry and clear cutoff
resources: GPU utilization held around 87-88%; RAM stayed about 97-98 GiB available
elapsed: 364.59 s
```

## Next Decision

Create the seed55 full-ringdown050 `8/5/5` summary and continue target-0
lower-tail replication.
