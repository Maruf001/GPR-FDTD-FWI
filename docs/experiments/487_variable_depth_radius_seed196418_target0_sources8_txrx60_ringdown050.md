# Experiment 487: Seed196418 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Run 953 starts the seed196418 Fibonacci replication branch with the standard
8-source target0 full-ringdown production row after seed121393 target0 failed
source-density rescue.

## 953: Coordinate Optimizer Variable-Depth/Radius Seed196418 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/953_coordinate_optimizer_variable_depth_radius_seed196418_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed196418:1.1,-50.0,1.1,0.10,196418,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed196418 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed196418_target0_sources8_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed196418
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 6.119611e-04
offset from cutoff: +1.119611e-04
relative radius margin: 3.917625e-02
confidence label: moderate
fallback warning: none
best misfit: 0.015620716591450977
next radius misfit: 0.01623267771538999
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: about 610.2 s
```

Diagnostic objective rows all preserve the true target0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 6.119611e-04 | above cutoff |
| highband | 8.141765e-04 | above cutoff |
| late | 5.317649e-04 | above cutoff |
| late_high | 6.091862e-04 | above cutoff |
| veryhigh | 7.548079e-04 | above cutoff |
| early_high | 6.620326e-04 | above cutoff |

## Interpretation

Run 953 is accepted as the seed196418 target0 8-source control. It is a strong
reset after seed121393 target0 was unresolved: every diagnostic objective
clears cutoff and the base margin has more than 1.1e-04 reserve. Continue to
target2 at 5 sources.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.289483 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate row well above the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target0 truth_radius_mm is 5.0 mm
resources: GPU utilization held around 90-91%; RAM stayed about 96 GiB available
```

## Next Decision

Continue the seed196418 branch with target2, sources=5, Tx/Rx=60, and
ringdown050. That run is underway as experiment 954.
