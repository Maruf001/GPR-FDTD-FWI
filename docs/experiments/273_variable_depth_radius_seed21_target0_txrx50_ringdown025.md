# Experiment 273: Seed21 Target-0 Tx/Rx=50 Fitted-Ringdown Diagnostic

## Purpose

Run 740 resumes the original substantive experiment style after the run 739
archive-health correction. The goal is not bookkeeping. The goal is to extend
the existing variable-depth/radius Tx/Rx=50 fitted-ringdown branch with one
additional bounded GPU diagnostic.

The pre-crash evidence package had already shown that target 0 recovered exact
geometry under seed55, seed13, and seed34 fitted-ringdown stresses. Run 740
adds seed21 using the same final-state geometry, the same target-0 local
candidate grid, the same source-mismatch/ringdown stress, and the same
diagnostic objective variants.

## 740: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-0 Tx/Rx=50 Ringdown025 Objectives

Output:

```text
outputs/experiments/740_coordinate_optimizer_variable_depth_radius_seed21_target0_txrx50_ringdown025_objectives
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
  --replication-cases source_mismatch_ringdown025_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.25,180.0,0.8 \
  --update-case-label source_mismatch_ringdown025_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 4 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target0_txrx50_ringdown025_objectives
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
source stress: frequency scale 1.1, time shift -50 ps, amplitude 1.1, noise 10%, seed 21, ringdown 0.25
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
case: source_mismatch_ringdown025_noise10_seed21
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.385658e-04
confidence label: moderate
ambiguity width: none recorded
```

Objective diagnostics:

| Objective | Best x/z/r mm | Next radius mm | Margin abs | Ratio to base |
| --- | --- | ---: | ---: | ---: |
| base | 150 / 80 / 5.0 | 5.25 | 5.385658e-04 | 1.000 |
| highband | 150 / 80 / 5.0 | 5.25 | 5.612532e-04 | 1.042 |
| late | 150 / 80 / 5.0 | 5.25 | 3.772010e-04 | 0.700 |
| late_high | 150 / 80 / 5.0 | 5.25 | 4.301148e-04 | 0.799 |
| veryhigh | 150 / 80 / 5.0 | 5.25 | 6.733696e-04 | 1.250 |
| early_high | 150 / 80 / 5.0 | 5.25 | 4.007065e-04 | 0.744 |

## Interpretation

Run 740 is consistent with the earlier target-0 fitted-ringdown evidence from
seed55, seed13, and seed34. The base production objective remains exact and
moderate on this additional seed21 stress. Veryhigh is the strongest tested
diagnostic for target 0 and improves the margin without changing geometry.
Late and late_high weaken target 0, which reinforces the previous conclusion
that late_high should not be promoted as a target-0 update rule even though it
helps targets 1 and 2.

The conservative branch-level conclusion is unchanged but stronger:

```text
Use base for the production coordinate update.
Use veryhigh as target-0 branch-level reporting evidence when it preserves geometry.
Do not promote veryhigh globally, and do not promote late_high for target 0.
```

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, nonblank
visual inspection: confidence figure is readable and matches the single moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization reached about 88%; RAM stayed healthy with about 100 GiB available after run
git diff --check: clean after run 740
```

## Next Decision

The restored marathon policy is now active:

```text
numbered outputs should be substantive experiments or decision-grade diagnostics,
admin/checkpoint/report churn should be consolidated or kept outside the main experiment sequence,
GPU should be used for bounded physics work when memory and RAM are healthy.
```

Before launching another GPU branch, run the archive-resolution audit requested
by the user: classify runs 535-735 into substantive versus admin/reporting
outputs, identify short tracker docs that can be appended into larger bundles,
and define a nonbreaking reorganization path.
