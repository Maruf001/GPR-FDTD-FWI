# Experiment 314: Seed89 Target-2 Sources=9 Linear Receiver Ringdown025

## Purpose

Run 781 completes the bounded source-density check for the seed89 target-2
linear-receiver ambiguity. It repeats the run 780 setup with 9 scan sources to
test whether increasing from 7 to 9 sources keeps improving the target-2 radius
margin or plateaus.

## 781: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Sources=9 Tx/Rx=50.3125 Linear Receiver Ringdown025

Output:

```text
outputs/experiments/781_coordinate_optimizer_variable_depth_radius_seed89_target2_sources9_txrx50p3125_linear_receiver_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 9 \
  --tx-rx-offset-mm 50.3125 \
  --receiver-sampling linear \
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
  --z-offsets-mm=-1:1:1 \
  --radius-offsets-mm=-1:1:0.25 \
  --replication-cases source_mismatch_ringdown025_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.25,180.0,0.8 \
  --update-case-label source_mismatch_ringdown025_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 27 \
  --progress-every 5 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_sources9_txrx50p3125_linear_receiver_ringdown025_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 9
scan x positions: [50, 98, 146, 194, 250, 298, 346, 394, 450] mm
Tx/Rx offset: 50.3125 mm
receiver sampling: linear
frequency: 1.5 GHz
truth x/z/r: [150,250,350] / [80,100,120] / [5,6,8] mm
initial x/z/r: truth final state
target index: 2
candidate grid: x offset 0, z offsets -1/0/+1 mm, radius offsets -1 to +1 mm in 0.25 mm steps
candidate count: 27
source stress: frequency scale 1.1, time shift -50 ps, amplitude 1.1, noise 10%, seed 89, ringdown 0.25
ringdown delay/frequency: 180 ps / 0.8
source fit: frequency grid 0.9/1.0/1.1, time shifts -50/0/50 ps, fitted ringdown coefficient
```

## Artifacts

```text
README.md
data/coordinate_confidence_report.csv
data/coordinate_objective_diagnostics.csv
data/coordinate_objective_top_candidates.csv
data/coordinate_state_history.csv
data/coordinate_step_01_target_2_candidates.csv
data/multi_rebar_coordinate_optimizer_summary.json
figures/coordinate_confidence_margins.png
figures/FIGURE_NOTES.md
run_manifest.json
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
case: source_mismatch_ringdown025_noise10_seed89
receiver sampling: linear
target: 2
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm at z=121 mm
absolute radius margin: 5.438787e-04
relative radius margin: 2.378974e-02
confidence label: moderate
best misfit: 0.0228618996445411
elapsed: 1605.99 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 5.438787e-04 | 1.000 |
| highband | 8.0 | 8.75 | 5.513892e-04 | 1.014 |
| late | 8.0 | 8.75 | 7.436442e-04 | 1.367 |
| late_high | 8.0 | 8.75 | 7.504162e-04 | 1.380 |
| veryhigh | 8.0 | 8.75 | 7.014494e-04 | 1.290 |
| early_high | 8.0 | 8.75 | 3.495032e-04 | 0.643 |

Source-density comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| 5 sources, linear Tx/Rx=50.3125 | 765 | 4.769427e-04 | 1.000 | weak |
| 7 sources, linear Tx/Rx=50.3125 | 780 | 6.453160e-04 | 1.353 vs run 765 | moderate |
| 9 sources, linear Tx/Rx=50.3125 | 781 | 5.438787e-04 | 1.140 vs run 765 | moderate |
| 5 sources, nearest Tx/Rx=50 | 745 | 9.935884e-04 | 0.547 vs run 745 | moderate |

## Interpretation

Run 781 confirms that added source density mitigates the seed89 target-2
linear-receiver weak plateau, but the improvement is not monotonic. The
9-source row remains exact/moderate and improves over the 5-source linear
baseline by 14.0%, but it is only 0.843x the 7-source margin from run 780.

The same coupled `z=121 mm, r=8.75 mm` competitor remains the limiting
next-radius candidate. The source aperture changes the separation strength but
does not change the ambiguity mechanism.

The best practical source-density setting in this 5/7/9 sweep is 7 sources.
Do not claim that adding more sources is monotonically beneficial for this
geometry.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=162, state history=2, candidates=27
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with full RGB dynamic range
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 90-91%; Python RSS stayed about 456-463 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Close the ringdown025 source-density sweep. The best next GPU check is the
7-source setting under ringdown035, because run 779 showed that 5 sources stay
weak under ringdown035 while run 780 showed that 7 sources rescue ringdown025.
