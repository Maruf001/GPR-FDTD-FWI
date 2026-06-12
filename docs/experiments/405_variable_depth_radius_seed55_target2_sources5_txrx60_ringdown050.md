# Experiment 405: Seed55 Target-2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 871 tests whether seed55 target 2 passes at 5 sources under full
ringdown050. This distinguishes seed55 from the seed89/seed34 target-2 rescue
pattern if it passes.

## 871: Coordinate Optimizer Variable-Depth/Radius Seed55 Target-2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/871_coordinate_optimizer_variable_depth_radius_seed55_target2_sources5_txrx60_ringdown050_objectives
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
  --target-indices 2 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed55_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 871 is exact and accepted:

```text
target: 2
sources: 5
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.677153e-04
offset from cutoff: +6.772e-05
confidence label: moderate
fallback warning: none
elapsed: 392.27 s
```

Diagnostic objective rows all preserve the true target-2 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.677153e-04 | above cutoff |
| highband | 7.019763e-04 | above cutoff |
| late | 8.812680e-04 | above cutoff |
| late_high | 9.384895e-04 | above cutoff |
| veryhigh | 7.310345e-04 | above cutoff |
| early_high | 4.871218e-04 | below cutoff |

## Interpretation

Seed55 target 2 passes at 5 sources, unlike seed89 and seed34:

| Seed | Run | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | --- |
| 13 | 838 | 5 | 5.882895e-04 | +8.829e-05 | accepted |
| 89 | 843 | 5 | 4.414917e-04 | -5.851e-05 | rejected |
| 34 | 861 | 5 | 4.575126e-04 | -4.249e-05 | rejected |
| 55 | 871 | 5 | 5.677153e-04 | +6.772e-05 | accepted |

Seed55 now has target0 and target2 accepted at full ringdown050. Target1
should complete the seed55 policy set.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.286459 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row above the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target2 truth_radius_mm is 8.0 mm
source validation: all six diagnostic objectives preserve target2 truth geometry; 5/6 clear cutoff
resources: GPU utilization held around 87-88%; RAM stayed about 97-98 GiB available
elapsed: 392.27 s
```

## Next Decision

Run seed55 target 1 at 5 sources and full ringdown050.
