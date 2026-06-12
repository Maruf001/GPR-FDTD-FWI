# Experiment 278: Seed89 Target-2 Tx/Rx=50 Fitted-Ringdown Diagnostic

## Purpose

Run 745 continues the restored substantive marathon branch with a second
seed89 GPU CPML diagnostic. The goal is to test target 2 under the same
source-mismatch/ringdown/noise condition used for run 744, and to check whether
the late_high target-2 diagnostic improvement seen in seed21 survives a new
noise seed.

This is deliberately narrow: one target, one source-mismatch case, one local
candidate grid, and the same objective diagnostics. That keeps GPU use high
without expanding RAM pressure.

## 745: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Tx/Rx=50 Ringdown025 Objectives

Output:

```text
outputs/experiments/745_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50_ringdown025_objectives
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
  --replication-cases source_mismatch_ringdown025_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.25,180.0,0.8 \
  --update-case-label source_mismatch_ringdown025_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 10 \
  --progress-every 5 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50_ringdown025_objectives
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
source stress: frequency scale 1.1, time shift -50 ps, amplitude 1.1, noise 10%, seed 89, ringdown 0.25
ringdown delay/frequency: 180 ps / 0.8
source fit: frequency grid 0.9/1.0/1.1, time shifts -50/0/50 ps, fitted ringdown coefficient
```

Diagnostic objective variants:

```text
base
highband
late
late_high
veryhigh
early_high
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
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 7.25 mm
absolute radius margin: 9.935884e-04
relative radius margin: 3.687471e-02
confidence label: moderate
```

Objective diagnostics:

| Objective | Best x/z/r mm | Next radius mm | Margin abs | Ratio to base |
| --- | --- | ---: | ---: | ---: |
| base | 350 / 120 / 8.0 | 7.25 | 9.935884e-04 | 1.000 |
| highband | 350 / 120 / 8.0 | 7.25 | 1.052263e-03 | 1.059 |
| late | 350 / 120 / 8.0 | 7.25 | 1.455306e-03 | 1.465 |
| late_high | 350 / 120 / 8.0 | 7.25 | 1.506552e-03 | 1.516 |
| veryhigh | 350 / 120 / 8.0 | 7.25 | 1.358312e-03 | 1.367 |
| early_high | 350 / 120 / 8.0 | 7.25 | 6.117933e-04 | 0.616 |

Seed-to-seed target-2 comparison:

```text
seed21 base margin: 8.000475e-04, exact/moderate, late_high ratio 1.506x
seed89 base margin: 9.935884e-04, exact/moderate, late_high ratio 1.516x
```

## Interpretation

Run 745 is consistent with the target-2 fitted-ringdown evidence from seed21
and the earlier seed55/13/34 package. The base production objective remains
exact and moderate under seed89. Late_high remains the strongest tested
target-2 diagnostic and increases the radius gap without changing geometry.

The target-specific branch policy is now better supported:

```text
Use base for the production coordinate update.
Use late_high as target-2 branch-level reporting evidence when it preserves geometry.
Do not promote late_high blindly to target 0.
```

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=60, state history=2, candidates=10
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, nonblank
visual inspection: confidence figure is readable and matches the single moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization reached about 87-88%; RAM stayed healthy with about 100 GiB available after run
```

## Next Decision

Run the seed89 target-1 fitted-ringdown diagnostic next if resources remain
healthy. Target 1 is the remaining all-target gap before packaging a seed89
all-target summary comparable to run 743.
