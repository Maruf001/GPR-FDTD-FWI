# Experiment 333: Seed89 Target-0 Sources=9 Tx/Rx=60 Linear Receiver Ringdown035

## Purpose

Run 799 checks whether the target-0 uniform 9-source ringdown035 weakness from
run 797 is caused by nearest receiver sampling. It repeats run 797 with
`--receiver-sampling linear` while keeping Tx/Rx=60 mm and the same source
positions.

## 799: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-0 Sources=9 Tx/Rx=60 Linear Receiver Ringdown035

Output:

```text
outputs/experiments/799_coordinate_optimizer_variable_depth_radius_seed89_target0_sources9_txrx60_linear_receiver_ringdown035_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 9 \
  --tx-rx-offset-mm 60 \
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
  --replication-cases source_mismatch_ringdown035_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.35,180.0,0.8 \
  --update-case-label source_mismatch_ringdown035_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 4 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target0_sources9_txrx60_linear_receiver_ringdown035_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 9
scan x positions: [50, 98, 146, 194, 250, 298, 346, 394, 450] mm
Tx/Rx offset: 60 mm
receiver sampling: linear
frequency: 1.5 GHz
truth x/z/r: [150,250,350] / [80,100,120] / [5,6,8] mm
initial x/z/r: truth final state
target index: 0
candidate grid: x offset 0, z offsets 0/+1 mm, radius offsets 0 to +1.25 mm in 0.25 mm steps
candidate count: 12
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
case: source_mismatch_ringdown035_noise10_seed89
receiver sampling: linear
target: 0
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 4.974546e-04
relative radius margin: 2.792554e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.017813609736609577
next radius misfit: 0.018311064325363394
competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 712.65 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 5.0 | 5.25 | 4.974546e-04 | 1.000 |
| highband | 5.0 | 5.25 | 5.922920e-04 | 1.191 |
| late | 5.0 | 5.25 | 3.629550e-04 | 0.730 |
| late_high | 5.0 | 5.25 | 3.930506e-04 | 0.790 |
| veryhigh | 5.0 | 5.25 | 6.620189e-04 | 1.331 |
| early_high | 5.0 | 5.25 | 4.824350e-04 | 0.970 |

Receiver-sampling comparison:

| Condition | Run | Receiver sampling | Base margin | Confidence |
| --- | ---: | --- | ---: | --- |
| target 0, 9 sources, Tx/Rx=60, ringdown035 | 797 | nearest | 4.974546e-04 | weak |
| target 0, 9 sources, Tx/Rx=60, ringdown035 | 799 | linear | 4.974546e-04 | weak |

## Interpretation

Run 799 is a no-effect control. Linear receiver sampling gives the same target
0 margin as nearest receiver sampling in run 797. This is expected in hindsight
because the scan positions and Tx/Rx=60 mm offset lie on the 1 mm grid, so the
linear interpolation weight is effectively zero and the linear receiver
collapses to the nearest receiver.

Therefore the target-0 uniform 9-source weakness is not rescued by simply
switching the receiver sampling mode at this integer-grid offset. A true
receiver-interpolation test would need a fractional Tx/Rx offset, such as
60.5 mm, or a fractional scan-position aperture.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.252 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly flags the weak row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held mostly about 90-91%; Python RSS stayed about 441-459 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Do not treat integer-grid linear receiver sampling as a separate physical
condition. If receiver interpolation remains the acquisition question, run a
fractional-offset check such as Tx/Rx=60.5 mm with linear receiver sampling.
Otherwise move to a different acquisition variable or an explicit
aperture-selection method.
