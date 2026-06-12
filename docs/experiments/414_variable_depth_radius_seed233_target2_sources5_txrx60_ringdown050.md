# Experiment 414: Seed233 Target-2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 880 tests seed233 target 2 at full ringdown050 with 5 sources.

## 880: Coordinate Optimizer Variable-Depth/Radius Seed233 Target-2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/880_coordinate_optimizer_variable_depth_radius_seed233_target2_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed233:1.1,-50.0,1.1,0.10,233,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed233 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed233_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 880 is exact and accepted:

```text
target: 2
sources: 5
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.878754e-04
offset from cutoff: +8.788e-05
confidence label: moderate
fallback warning: none
elapsed: 362.32 s
```

Diagnostic objective rows all preserve the true target-2 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.878754e-04 | above cutoff |
| highband | 7.209866e-04 | above cutoff |
| late | 8.740772e-04 | above cutoff |
| late_high | 9.064916e-04 | above cutoff |
| veryhigh | 7.455708e-04 | above cutoff |
| early_high | 5.377057e-04 | above cutoff |

## Interpretation

Seed233 target 2 passes at 5 sources:

| Seed | Run | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | --- |
| 13 | 838 | 5 | 5.882895e-04 | +8.829e-05 | accepted |
| 89 | 843 | 5 | 4.414917e-04 | -5.851e-05 | rejected |
| 34 | 861 | 5 | 4.575126e-04 | -4.249e-05 | rejected |
| 55 | 871 | 5 | 5.677153e-04 | +6.772e-05 | accepted |
| 144 | 875 | 5 | 5.470037e-04 | +4.700e-05 | accepted |
| 233 | 880 | 5 | 5.878754e-04 | +8.788e-05 | accepted |

Seed233 aligns with the accepted 5-source target-2 seeds, not the seed89/seed34
9-source rescue branch.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.291118 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row above the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target2 truth_radius_mm is 8.0 mm
source validation: all six diagnostic objectives preserve target2 truth geometry; 6/6 clear cutoff
resources: GPU production run; RAM stayed around 97-98 GiB available
elapsed: 362.32 s
```

## Next Decision

Run seed233 target 1 at 5 sources and full ringdown050. If accepted, summarize
seed233 as another `8/5/5` policy seed.
