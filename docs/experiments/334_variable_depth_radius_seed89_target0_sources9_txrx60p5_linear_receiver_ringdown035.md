# Experiment 334: Seed89 Target-0 Sources=9 Tx/Rx=60.5 Linear Receiver Ringdown035

## Purpose

Run 800 is the true fractional receiver-interpolation check requested by run
799. It repeats the target-0 uniform 9-source ringdown035 case with
`--receiver-sampling linear`, but changes the Tx/Rx offset from 60.0 mm to
60.5 mm so the receiver interpolation has a nonzero fractional grid weight.

## 800: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-0 Sources=9 Tx/Rx=60.5 Linear Receiver Ringdown035

Output:

```text
outputs/experiments/800_coordinate_optimizer_variable_depth_radius_seed89_target0_sources9_txrx60p5_linear_receiver_ringdown035_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 9 \
  --tx-rx-offset-mm 60.5 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target0_sources9_txrx60p5_linear_receiver_ringdown035_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 9
scan x positions: [50, 98, 146, 194, 250, 298, 346, 394, 450] mm
Tx/Rx offset: 60.5 mm
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
Tx/Rx offset: 60.5 mm
target: 0
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 4.962654e-04
relative radius margin: 2.821130e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.017591016161937652
next radius misfit: 0.018087281531314774
competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 714.65 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 5.0 | 5.25 | 4.962654e-04 | 1.000 |
| highband | 5.0 | 5.25 | 5.911603e-04 | 1.191 |
| late | 5.0 | 5.25 | 3.620480e-04 | 0.730 |
| late_high | 5.0 | 5.25 | 3.948948e-04 | 0.796 |
| veryhigh | 5.0 | 5.25 | 6.606891e-04 | 1.331 |
| early_high | 5.0 | 5.25 | 4.816812e-04 | 0.971 |

Receiver/acquisition comparison:

| Condition | Run | Tx/Rx mm | Receiver sampling | Base margin | Confidence |
| --- | ---: | ---: | --- | ---: | --- |
| target 0, 9 sources, ringdown035 | 797 | 60.0 | nearest | 4.974546e-04 | weak |
| target 0, 9 sources, ringdown035 | 799 | 60.0 | linear | 4.974546e-04 | weak |
| target 0, 9 sources, ringdown035 | 800 | 60.5 | linear | 4.962654e-04 | weak |
| target 0, 8 sources, ringdown035 | 795 | 60.0 | nearest | 5.954728e-04 | moderate |

## Interpretation

Run 800 is a negative fractional receiver-interpolation control. The
60.5 mm offset creates a true interpolation case, but the base target-0 margin
is 4.963e-04, still weak and slightly lower than the 60.0 mm nearest/linear
rows from runs 797 and 799. It is also only 0.833x the target-0 8-source
ringdown035 margin from run 795.

Therefore the target-0 uniform 9-source weakness is robust to this small
fractional receiver-offset perturbation. Receiver interpolation at 60.5 mm does
not rescue uniform 9 as an all-target aperture. The highband and veryhigh
diagnostic objectives again raise the margin above the moderate threshold, but
the base objective remains the policy metric and stays weak.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.252 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly flags the weak row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held mostly about 90-91%; Python RSS stayed about 441-458 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Stop the receiver-sampling rescue path for this aperture. The next substantive
branch should either move the acquisition offset far enough to change the
physics, or use an explicit aperture-selection criterion rather than more
nearby hand-tuned receiver/interpolation checks.
