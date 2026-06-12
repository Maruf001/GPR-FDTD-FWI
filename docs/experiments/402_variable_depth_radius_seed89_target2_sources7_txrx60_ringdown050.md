# Experiment 402: Seed89 Target-2 Sources=7 Tx/Rx=60 Ringdown050

## Purpose

Run 868 tests the 7-source intermediate for seed89 target 2 at full
ringdown050, between rejected 5-source run 843 and accepted 9-source run 844.

## 868: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Sources=7 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/868_coordinate_optimizer_variable_depth_radius_seed89_target2_sources7_txrx60_ringdown050_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 7 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_sources7_txrx60_ringdown050_objectives
```

## Results

Run 868 is exact but weak:

```text
target: 2
sources: 7
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 4.616187e-04
offset from cutoff: -3.838e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 534.10 s
```

Diagnostic objective rows all preserve the true target-2 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.616187e-04 | below cutoff |
| highband | 5.946083e-04 | above cutoff |
| late | 6.479546e-04 | above cutoff |
| late_high | 7.401057e-04 | above cutoff |
| veryhigh | 6.148736e-04 | above cutoff |
| early_high | 3.881831e-04 | below cutoff |

## Interpretation

Seven sources are not enough for seed89 target 2 at full ringdown050:

| Run | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 843 | 5 | 4.414917e-04 | -5.851e-05 | rejected |
| 868 | 7 | 4.616187e-04 | -3.838e-05 | rejected |
| 844 | 9 | 5.821195e-04 | +8.212e-05 | accepted |

The 7-source result is closer to cutoff than the 5-source control, but it is
still weak. A direct 8-source check is required before deciding whether seed89
target 2 also requires 9 sources.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.236886 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one weak row below the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target2 truth_radius_mm is 8.0 mm
source validation: all six diagnostic objectives preserve target2 truth geometry; 4/6 clear cutoff
resources: GPU utilization held around 89-90%; RAM stayed about 97-98 GiB available
elapsed: 534.10 s
```

## Next Decision

Run seed89 target 2 at 8 sources and full ringdown050.
