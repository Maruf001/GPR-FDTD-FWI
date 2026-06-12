# Experiment 453: Seed6765 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Run 919 starts the seed6765 branch with the standard target0 8-source
full-ringdown control.

## 919: Coordinate Optimizer Variable-Depth/Radius Seed6765 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/919_coordinate_optimizer_variable_depth_radius_seed6765_target0_sources8_txrx60_ringdown050_objectives
```

Command:

```text
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
  --replication-cases source_mismatch_ringdown050_noise10_seed6765:1.1,-50.0,1.1,0.10,6765,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed6765 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed6765_target0_sources8_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed6765
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 4.905837e-04
offset from cutoff: -9.416301e-06
relative radius margin: 3.107835e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.01578538552509494
next radius misfit: 0.016275969223640836
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: about 627.0 s
```

Diagnostic objective rows all preserve the true target0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.905837e-04 | below cutoff |
| highband | 6.738212e-04 | above cutoff |
| late | 4.395305e-04 | below cutoff |
| late_high | 5.235599e-04 | above cutoff |
| veryhigh | 6.147442e-04 | above cutoff |
| early_high | 5.679365e-04 | above cutoff |

## Interpretation

Run 919 is exact but rejected under the production cutoff. The base margin is
9.416e-06 below cutoff, the confidence label is weak, and the late objective
variant is also below cutoff. Since the true geometry is still rank 1, the
proper next action is the targeted 9-source target0 rescue.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.243411 and full dynamic range
visual inspection: confidence figure is readable and shows one weak row below the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target0 truth_radius_mm is 5.0 mm
resources: GPU utilization held around 90%; RAM stayed about 97 GiB available
```

## Next Decision

Run seed6765 target0 with 9 sources, Tx/Rx=60, and ringdown050.
