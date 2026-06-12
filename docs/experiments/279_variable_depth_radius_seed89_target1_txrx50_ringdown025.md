# Experiment 279: Seed89 Target-1 Tx/Rx=50 Fitted-Ringdown Diagnostic

## Purpose

Run 746 completes the seed89 fitted-ringdown target-specific replication. Runs
744 and 745 already checked target 0 and target 2. This run checks target 1,
the heavier center-target grid, under the same Tx/Rx=50 mm final-state branch,
source-mismatch/ringdown stress, fitted source profile, and diagnostic
objective variants.

The purpose is not to inflate the experiment count. The purpose is to close the
all-target seed89 evidence gap before creating a compact summary comparable to
run 743.

## 746: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-1 Tx/Rx=50 Ringdown025 Objectives

Output:

```text
outputs/experiments/746_coordinate_optimizer_variable_depth_radius_seed89_target1_txrx50_ringdown025_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target1_txrx50_ringdown025_objectives
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
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.982895e-04
relative radius margin: 2.220412e-02
confidence label: moderate
```

Objective diagnostics:

| Objective | Best x/z/r mm | Next radius mm | Margin abs | Ratio to base |
| --- | --- | ---: | ---: | ---: |
| base | 250 / 100 / 6.0 | 6.25 | 5.982895e-04 | 1.000 |
| highband | 250 / 100 / 6.0 | 6.25 | 6.320683e-04 | 1.056 |
| late | 250 / 100 / 6.0 | 6.25 | 7.697763e-04 | 1.287 |
| late_high | 250 / 100 / 6.0 | 6.25 | 8.565618e-04 | 1.432 |
| veryhigh | 250 / 100 / 6.0 | 6.25 | 7.305676e-04 | 1.221 |
| early_high | 250 / 100 / 6.0 | 6.25 | 3.964496e-04 | 0.663 |

Seed-to-seed target-1 comparison:

```text
seed21 base margin: 7.175881e-04, exact/moderate, late_high ratio 1.279x
seed89 base margin: 5.982895e-04, exact/moderate, late_high ratio 1.432x
```

## Interpretation

Run 746 is consistent with the target-1 fitted-ringdown evidence because the
base objective still recovers exact truth under seed89. It is also the one
seed89 target where the base margin is lower than the seed21 counterpart. That
does not overturn the branch conclusion, but it should be reported in the
seed89 all-target summary as a real seed sensitivity.

Late_high remains the strongest tested center-target diagnostic and improves
the margin without changing geometry. The branch-level conclusion is:

```text
Use base for the production coordinate update.
Use late_high as target-1 branch-level reporting evidence when it preserves geometry.
Do not promote diagnostic objectives to production without a separate update-rule study.
```

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=162, state history=2, candidates=27
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, nonblank
visual inspection: confidence figure is readable and matches the single moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization reached about 87-88%; RAM stayed healthy with about 100 GiB available after run
```

## Next Decision

Package runs 744-746 into a seed89 all-target fitted-ringdown summary. The
summary should compare seed89 against seed21, emphasize that all three targets
remain exact/moderate, and call out that target 1 has a lower base gap under
seed89 even though late_high gives a stronger diagnostic ratio.
