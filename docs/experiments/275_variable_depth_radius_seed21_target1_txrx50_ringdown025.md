# Experiment 275: Seed21 Target-1 Tx/Rx=50 Fitted-Ringdown Diagnostic

## Purpose

Run 742 completes the added seed21 all-target fitted-ringdown robustness check.
Runs 740 and 741 already tested target 0 and target 2. This run tests the
center target, target 1, which uses the heavier 27-candidate z/r grid.

This is a substantive GPU diagnostic, not a checkpoint.

## 742: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-1 Tx/Rx=50 Ringdown025 Objectives

Output:

```text
outputs/experiments/742_coordinate_optimizer_variable_depth_radius_seed21_target1_txrx50_ringdown025_objectives
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
  --target-indices 1 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=-1:1:1 \
  --radius-offsets-mm=-1:1:0.25 \
  --replication-cases source_mismatch_ringdown025_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.25,180.0,0.8 \
  --update-case-label source_mismatch_ringdown025_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 27 \
  --progress-every 5 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target1_txrx50_ringdown025_objectives
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
target index: 1
candidate grid: x offset 0, z offsets -1-1 mm, radius offsets -1-1 mm in 0.25 mm steps
candidate count: 27
source stress: frequency scale 1.1, time shift -50 ps, amplitude 1.1, noise 10%, seed 21, ringdown 0.25
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
case: source_mismatch_ringdown025_noise10_seed21
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 7.175881e-04
confidence label: moderate
ambiguity width: none recorded
```

Objective diagnostics:

| Objective | Best x/z/r mm | Next radius mm | Margin abs | Ratio to base |
| --- | --- | ---: | ---: | ---: |
| base | 250 / 100 / 6.0 | 6.25 | 7.175881e-04 | 1.000 |
| highband | 250 / 100 / 6.0 | 6.25 | 7.149820e-04 | 0.996 |
| late | 250 / 100 / 6.0 | 6.25 | 8.451155e-04 | 1.178 |
| late_high | 250 / 100 / 6.0 | 6.25 | 9.179762e-04 | 1.279 |
| veryhigh | 250 / 100 / 6.0 | 6.25 | 7.307254e-04 | 1.018 |
| early_high | 250 / 100 / 6.0 | 6.25 | 4.226969e-04 | 0.589 |

## Interpretation

Run 742 closes the added-seed target set. The seed21 stress did not introduce a
new failure on any of the three targets:

```text
run 740 target 0: exact, moderate
run 741 target 2: exact, moderate
run 742 target 1: exact, moderate
```

The objective diagnostics remain target-specific. Veryhigh is strongest for
target 0; late_high is strongest for targets 1 and 2. This supports using
objective variants as reporting diagnostics rather than replacing the base
production update rule.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=162, state history=2, candidates=27
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, nonblank
visual inspection: confidence figure is readable and matches the single moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held near 88%; RAM remained healthy with about 100 GiB available
git diff --check: clean after run 742
```

## Next Decision

Generate a compact all-target seed21 fitted-ringdown summary from runs 740-742
with one table and one figure. That summary can be a decision-grade analysis
artifact, unlike the earlier pointer/checkpoint churn.
