# Experiment 309: Seed89 Target-1 Tx/Rx=50.3125 Linear-Receiver Diagnostic

## Purpose

Run 776 changes the factor from target-2 seed replication to target-specific
linear receiver sensitivity. It tests seed89 target 1 with the same linear
Tx/Rx=50.3125 offset that created a weak target-2 plateau.

## 776: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-1 Tx/Rx=50.3125 Linear Receiver Ringdown025

Output:

```text
outputs/experiments/776_coordinate_optimizer_variable_depth_radius_seed89_target1_txrx50p3125_linear_receiver_ringdown025_objectives
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
  --target-indices 1 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target1_txrx50p3125_linear_receiver_ringdown025_objectives
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
target index: 1
candidate grid: x offset 0, z offsets -1/0/1 mm, radius offsets -1.0 to +1.0 mm in 0.25 mm steps
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
data/coordinate_step_01_target_1_candidates.csv
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
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.985570e-04
relative radius margin: 2.239049e-02
confidence label: moderate
best misfit: 0.0267326398663862
elapsed: 894.26 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 6.0 | 6.25 | 5.985570e-04 | 1.000 |
| highband | 6.0 | 6.25 | 6.329445e-04 | 1.057 |
| late | 6.0 | 6.25 | 7.728819e-04 | 1.291 |
| late_high | 6.0 | 6.25 | 8.592397e-04 | 1.436 |
| veryhigh | 6.0 | 6.25 | 7.325700e-04 | 1.224 |
| early_high | 6.0 | 6.25 | 3.978084e-04 | 0.665 |

Target comparison:

| Seed89 target | Condition | Base margin | Ratio to nearest Tx/Rx=50 | Confidence |
| --- | --- | ---: | ---: | --- |
| target 1 | nearest Tx/Rx=50 (run 746) | 5.982895e-04 | 1.000 | moderate |
| target 1 | linear Tx/Rx=50.3125 (run 776) | 5.985570e-04 | 1.000 | moderate |
| target 2 | linear Tx/Rx=50.3125 (run 765) | 4.769427e-04 | 0.480 | weak |

## Interpretation

Target 1 does not show the seed89 target-2 weak plateau. The base margin is
1.0004x the nearest-grid target-1 baseline and remains moderate. This points
to target-2 depth/position sensitivity rather than a global linear receiver
sampling failure.

Late_high remains the strongest truth-preserving target-1 diagnostic at 1.436x
base.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=162, state history=2, candidates=27
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, grayscale std 68.4185
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 86-88%; RAM stayed healthy with about 99-100 GiB available
```

## Next Decision

Run seed89 target 0 at linear Tx/Rx=50.3125, or generate a target-sensitivity
summary if a target-0 run is not needed immediately.
