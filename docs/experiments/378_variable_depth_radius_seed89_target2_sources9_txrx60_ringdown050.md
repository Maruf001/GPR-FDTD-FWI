# Experiment 378: Seed89 Target-2 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Run 844 tests whether restoring the old 9-source target-2 acquisition rescues
the weak seed89 target-2 5-source ringdown050 row from run 843.

## 844: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/844_coordinate_optimizer_variable_depth_radius_seed89_target2_sources9_txrx60_ringdown050_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 9 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_sources9_txrx60_ringdown050_objectives
```

## Results

The final recovered coordinate state is exact:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

Base confidence row:

```text
case: source_mismatch_ringdown050_noise10_seed89
target: 2
sources: 9
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.821195e-04
relative radius margin: 3.757048e-02
confidence label: moderate
fallback warning: none
best misfit: 0.015494066110077377
next radius misfit: 0.016076185604553057
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 684.68 s
```

Diagnostic objective rows all preserved the true target-2 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.821195e-04 | above cutoff |
| highband | 7.350847e-04 | above cutoff |
| late | 8.993137e-04 | above cutoff |
| late_high | 9.670123e-04 | above cutoff |
| veryhigh | 7.945777e-04 | above cutoff |
| early_high | 5.537299e-04 | above cutoff |

## Interpretation

Run 844 rescues seed89 target 2. The 9-source row improves over weak 5-source
run 843 by `1.406e-04`, removes `radius_weak_confidence`, and leaves all six
diagnostic objective rows above cutoff. It retains `0.977x` of the lower-stress
seed89 target-2 9-source row from run 822 and is only `6.170e-06` below
seed13 target-2 5-source ringdown050 run 838.

Seed89 should not use the seed13 `8/5/5` source-count policy. The evidence
supports `8/5/9` for seed89 at ringdown050: target 0 from run 842, target 1
from run 835, and target 2 from run 844.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.292780 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 8.0 mm
resources: GPU utilization held around 91-92%; Python RSS stayed about 453-461 MiB; RAM stayed about 98 GiB available
elapsed: 684.68 s
```

## Next Decision

Create a seed89 all-target ringdown050 summary from runs 842, 835, and 844.
The summary should retain run 843 as a negative 5-source target-2 result but
exclude it from the promoted policy rows.
