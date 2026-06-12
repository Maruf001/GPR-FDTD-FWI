# Experiment 283: Seed89 Target-2 Tx/Rx=50 Ringdown035 Diagnostic

## Purpose

Run 750 continues the stronger ringdown035 branch after run 749 showed that
target 1 remained exact/moderate and slightly stronger than its ringdown025
counterpart. Target 2 is the next best check because late_high was strongest on
target 2 in both seed21 and seed89 ringdown025 summaries.

## 750: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Tx/Rx=50 Ringdown035 Objectives

Output:

```text
outputs/experiments/750_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50_ringdown035_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 50 \
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
  --z-offsets-mm=-1:0:1 \
  --radius-offsets-mm=-1:0:0.25 \
  --replication-cases source_mismatch_ringdown035_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.35,180.0,0.8 \
  --update-case-label source_mismatch_ringdown035_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 10 \
  --progress-every 5 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50_ringdown035_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 5
Tx/Rx offset: 50 mm
frequency: 1.5 GHz
truth x/z/r: [150,250,350] / [80,100,120] / [5,6,8] mm
initial x/z/r: truth final state
target index: 2
candidate grid: x offset 0, z offsets -1-0 mm, radius offsets -1-0 mm in 0.25 mm steps
candidate count: 10
source stress: frequency scale 1.1, time shift -50 ps, amplitude 1.1, noise 10%, seed 89, ringdown 0.35
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
case: source_mismatch_ringdown035_noise10_seed89
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 7.25 mm
absolute radius margin: 1.038879e-03
relative radius margin: 4.128001e-02
confidence label: strong
```

Objective diagnostics:

| Objective | Best x/z/r mm | Next radius mm | Margin abs | Ratio to base |
| --- | --- | ---: | ---: | ---: |
| base | 350 / 120 / 8.0 | 7.25 | 1.038879e-03 | 1.000 |
| highband | 350 / 120 / 8.0 | 7.25 | 1.220363e-03 | 1.175 |
| late | 350 / 120 / 8.0 | 7.25 | 1.598536e-03 | 1.539 |
| late_high | 350 / 120 / 8.0 | 7.25 | 1.681919e-03 | 1.619 |
| veryhigh | 350 / 120 / 8.0 | 7.25 | 1.407396e-03 | 1.355 |
| early_high | 350 / 120 / 8.0 | 7.25 | 7.400944e-04 | 0.712 |

Ringdown025 comparison:

```text
run 745 ringdown025 seed89 target 2:
  base margin: 9.935884e-04
  confidence: moderate
  late_high ratio: 1.516x

run 750 ringdown035 seed89 target 2:
  base margin: 1.038879e-03
  confidence: strong
  late_high ratio: 1.619x
```

## Interpretation

Target 2 remains exact under ringdown035 and improves from moderate to strong
base confidence. Late_high remains the strongest diagnostic and increases the
radius margin without changing geometry. This is consistent with the target-2
pattern from the ringdown025 branch and suggests that the stronger fitted
ringdown tail is not a failure mode for target 2.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=60, state history=2, candidates=10
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, nonblank
visual inspection: confidence figure is readable and matches the single strong row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization reached about 86-88%; RAM stayed healthy with about 100 GiB available after run
```

## Next Decision

Run ringdown035 target 0 next. That is the only remaining target before a
ringdown035 all-target package, and it tests whether target 0 still prefers
veryhigh under the stronger ringdown stress.
