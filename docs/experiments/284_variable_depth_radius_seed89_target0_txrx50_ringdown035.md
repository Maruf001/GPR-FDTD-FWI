# Experiment 284: Seed89 Target-0 Tx/Rx=50 Ringdown035 Diagnostic

## Purpose

Run 751 completes the all-target ringdown035 target-specific diagnostic set.
Runs 749 and 750 showed that target 1 and target 2 remain exact under the
stronger ringdown stress. This run checks target 0, where veryhigh was the
strongest diagnostic under ringdown025 and late/late_high weakened the row.

## 751: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-0 Tx/Rx=50 Ringdown035 Objectives

Output:

```text
outputs/experiments/751_coordinate_optimizer_variable_depth_radius_seed89_target0_txrx50_ringdown035_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target0_txrx50_ringdown035_objectives
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
target index: 0
candidate grid: x offset 0, z offsets 0-1 mm, radius offsets 0-1.25 mm in 0.25 mm steps
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
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 6.141948e-04
relative radius margin: 2.440511e-02
confidence label: moderate
```

Objective diagnostics:

| Objective | Best x/z/r mm | Next radius mm | Margin abs | Ratio to base |
| --- | --- | ---: | ---: | ---: |
| base | 150 / 80 / 5.0 | 5.25 | 6.141948e-04 | 1.000 |
| highband | 150 / 80 / 5.0 | 5.25 | 6.912218e-04 | 1.125 |
| late | 150 / 80 / 5.0 | 5.25 | 4.628803e-04 | 0.754 |
| late_high | 150 / 80 / 5.0 | 5.25 | 4.932054e-04 | 0.803 |
| veryhigh | 150 / 80 / 5.0 | 5.25 | 8.228751e-04 | 1.340 |
| early_high | 150 / 80 / 5.0 | 5.25 | 5.238073e-04 | 0.853 |

Ringdown025 comparison:

```text
run 744 ringdown025 seed89 target 0:
  base margin: 5.798369e-04
  confidence: moderate
  veryhigh ratio: 1.355x

run 751 ringdown035 seed89 target 0:
  base margin: 6.141948e-04
  confidence: moderate
  veryhigh ratio: 1.340x
```

## Interpretation

Target 0 remains exact under ringdown035. The base margin improves relative to
ringdown025, and veryhigh remains strongest. Late and late_high still weaken
target 0, so the target-specific diagnostic pattern remains stable under the
stronger ringdown tail.

Runs 749-751 now support a ringdown035 all-target summary:

```text
target 0: exact/moderate, veryhigh strongest
target 1: exact/moderate, late_high strongest
target 2: exact/strong, late_high strongest
```

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, nonblank
visual inspection: confidence figure is readable and matches the single moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization reached about 87-88%; RAM stayed healthy with about 100 GiB available after run
```

## Next Decision

Package runs 751, 749, and 750 into a compact ringdown035 all-target summary
using the generalized fitted-ringdown summary helper.
