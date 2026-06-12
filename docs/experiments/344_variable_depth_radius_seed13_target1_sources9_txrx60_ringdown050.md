# Experiment 344: Seed13 Target-1 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Run 810 continues the stronger source-condition bracket on the weakest
replicated policy row. It repeats seed13 target 1 with 9 sources and Tx/Rx=60,
increasing the true ringdown scale from the near-threshold 0.45 case to 0.50.

## 810: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-1 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/810_coordinate_optimizer_variable_depth_radius_seed13_target1_sources9_txrx60_ringdown050_objectives
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
  --target-indices 1 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown050_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.50,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target1_sources9_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed13
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 4.879320e-04
relative radius margin: 3.095998e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.015760086450305986
next radius misfit: 0.01624801843501028
competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 716.50 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 4.879320e-04 | 1.000 | 1.576009e-02 |
| highband | 6.926420e-04 | 1.420 | 2.799889e-04 |
| late | 7.252013e-04 | 1.486 | 1.912066e-02 |
| late_high | 8.920830e-04 | 1.828 | 3.127529e-04 |
| veryhigh | 6.752800e-04 | 1.384 | 3.223781e-04 |
| early_high | 5.314503e-04 | 1.089 | 9.573564e-05 |

Ringdown bracket:

| Condition | Run | Base margin | Ratio vs ringdown035 | Confidence |
| --- | ---: | ---: | ---: | --- |
| seed13 target 1, ringdown035 | 806 | 5.109178e-04 | 1.000 | moderate |
| seed13 target 1, ringdown045 | 809 | 5.030490e-04 | 0.985 | moderate |
| seed13 target 1, ringdown050 | 810 | 4.879320e-04 | 0.955 | weak |

## Interpretation

Run 810 preserves exact geometry but crosses the production confidence cutoff.
The ringdown050 row is the first weak row in the stronger source-condition
target-1 bracket, and the threshold is now between ringdown045 and
ringdown050.

The diagnostic objectives remain truth-preserving and late_high is still the
strongest diagnostic margin. That does not override the production base-row
classification; it means the failure is a base-confidence margin failure, not a
geometry-selection failure.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.248 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one weak row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 90-91%; Python RSS stayed about 453-462 MiB; RAM stayed about 98-99 GiB available
elapsed: 716.50 s
```

## Next Decision

Run a single midpoint bracket check at ringdown0475 on the same seed13 target-1
row. That will locate the confidence transition more tightly before extending
the stronger-ringdown branch to other targets or summarizing it.

