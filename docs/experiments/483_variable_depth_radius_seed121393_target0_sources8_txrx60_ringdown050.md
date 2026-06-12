# Experiment 483: Seed121393 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Run 949 starts the seed121393 Fibonacci replication branch with the standard
8-source target0 full-ringdown production row after seed75025 was accepted only
after a fragile target2 rescue.

## 949: Coordinate Optimizer Variable-Depth/Radius Seed121393 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/949_coordinate_optimizer_variable_depth_radius_seed121393_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed121393:1.1,-50.0,1.1,0.10,121393,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed121393 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed121393_target0_sources8_txrx60_ringdown050_objectives
```

## Results

The final recovered coordinate state is exact, but base confidence is below
cutoff:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

Base confidence row:

```text
case: source_mismatch_ringdown050_noise10_seed121393
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 4.651123e-04
offset from cutoff: -3.488769e-05
relative radius margin: 2.978815e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.015614002821777136
next radius misfit: 0.01607911513589835
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: about 630.5 s
```

Diagnostic objective rows all preserve the true target0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.651123e-04 | below cutoff |
| highband | 6.435403e-04 | above cutoff |
| late | 3.973800e-04 | below cutoff |
| late_high | 4.775535e-04 | below cutoff |
| veryhigh | 6.147780e-04 | above cutoff |
| early_high | 5.145201e-04 | above cutoff |

## Interpretation

Run 949 is exact but weak. It is rejected as the seed121393 target0 8-source
control because the base margin is 3.489e-05 below cutoff. Since every
objective variant still ranks the true geometry first, the correct next action
is a source-density rescue rather than a change in coordinate window.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.226339 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak row below the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and flags target0 as weak
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target0 truth_radius_mm is 5.0 mm
resources: GPU utilization held around 90-91%; RAM stayed about 96 GiB available
```

## Next Decision

Run the seed121393 target0 9-source rescue. That run is underway as experiment
950.
