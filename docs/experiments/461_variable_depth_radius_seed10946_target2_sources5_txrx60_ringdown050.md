# Experiment 461: Seed10946 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 927 tests seed10946 target2 at the standard 5-source full-ringdown control
after target0 was rescued at 9 sources.

## 927: Coordinate Optimizer Variable-Depth/Radius Seed10946 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/927_coordinate_optimizer_variable_depth_radius_seed10946_target2_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed10946:1.1,-50.0,1.1,0.10,10946,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed10946 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed10946_target2_sources5_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed10946
target: 2
sources: 5
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 4.932705e-04
offset from cutoff: -6.729525e-06
relative radius margin: 2.919276e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.0168970148036774
next radius misfit: 0.01739028527881966
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: about 399.1 s
```

Diagnostic objective rows all preserve the true target2 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.932705e-04 | below cutoff |
| highband | 5.927207e-04 | above cutoff |
| late | 7.359370e-04 | above cutoff |
| late_high | 7.890547e-04 | above cutoff |
| veryhigh | 5.943745e-04 | above cutoff |
| early_high | 4.055549e-04 | below cutoff |

## Interpretation

Run 927 is exact but rejected under the production cutoff. Base is only
6.730e-06 below cutoff, but early_high is much weaker. The targeted target2
9-source rescue is the next action.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.241648 and full dynamic range
visual inspection: confidence figure is readable and shows one weak row below the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target2 truth_radius_mm is 8.0 mm
resources: GPU utilization held around 87%; RAM stayed about 97 GiB available
```

## Next Decision

Run seed10946 target2 with 9 sources, Tx/Rx=60, and ringdown050.
