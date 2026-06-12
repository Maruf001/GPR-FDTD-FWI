# Experiment 310: Seed89 Target-0 Tx/Rx=50.3125 Linear-Receiver Diagnostic

## Purpose

Run 777 completes the seed89 target-specific linear receiver check at
Tx/Rx=50.3125. It tests whether the target-2 weak plateau appears on the
shallow target.

## 777: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-0 Tx/Rx=50.3125 Linear Receiver Ringdown025

Output:

```text
outputs/experiments/777_coordinate_optimizer_variable_depth_radius_seed89_target0_txrx50p3125_linear_receiver_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 50.3125 \
  --receiver-sampling linear \
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
  --replication-cases source_mismatch_ringdown025_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.25,180.0,0.8 \
  --update-case-label source_mismatch_ringdown025_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 4 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target0_txrx50p3125_linear_receiver_ringdown025_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 5
Tx/Rx offset: 50.3125 mm
receiver sampling: linear
frequency: 1.5 GHz
truth x/z/r: [150,250,350] / [80,100,120] / [5,6,8] mm
initial x/z/r: truth final state
target index: 0
candidate grid: x offset 0, z offsets 0-1 mm, radius offsets 0-1.25 mm in 0.25 mm steps
candidate count: 12
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
data/coordinate_step_01_target_0_candidates.csv
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
target: 0
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.789458e-04
relative radius margin: 2.165689e-02
confidence label: moderate
best misfit: 0.0267326398663862
elapsed: 395.97 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 5.0 | 5.25 | 5.789458e-04 | 1.000 |
| highband | 5.0 | 5.25 | 5.867086e-04 | 1.013 |
| late | 5.0 | 5.25 | 4.025862e-04 | 0.695 |
| late_high | 5.0 | 5.25 | 4.227987e-04 | 0.730 |
| veryhigh | 5.0 | 5.25 | 7.833627e-04 | 1.353 |
| early_high | 5.0 | 5.25 | 4.304631e-04 | 0.744 |

Target comparison:

| Seed89 target | Condition | Base margin | Ratio to nearest Tx/Rx=50 | Confidence |
| --- | --- | ---: | ---: | --- |
| target 0 | nearest Tx/Rx=50 (run 744) | 5.798369e-04 | 1.000 | moderate |
| target 0 | linear Tx/Rx=50.3125 (run 777) | 5.789458e-04 | 0.999 | moderate |
| target 1 | linear Tx/Rx=50.3125 (run 776) | 5.985570e-04 | 1.000 | moderate |
| target 2 | linear Tx/Rx=50.3125 (run 765) | 4.769427e-04 | 0.480 | weak |

## Interpretation

Target 0 remains exact/moderate under linear Tx/Rx=50.3125. Combined with run
776, this shows the seed89 target-2 weak plateau is not shared by targets 0 or
1. The effect is target-specific under the tested acquisition and source
stress.

Veryhigh remains the strongest truth-preserving target-0 diagnostic at 1.353x
base.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, grayscale std 67.8487
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 87%; RAM stayed healthy with about 99-100 GiB available
```

## Next Decision

Create a compact all-target seed89 linear receiver summary.
