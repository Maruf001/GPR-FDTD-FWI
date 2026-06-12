# Experiment 274: Seed21 Target-2 Tx/Rx=50 Fitted-Ringdown Diagnostic

## Purpose

Run 741 extends the restored substantive experiment sequence from run 740. It
uses the same seed21 source-mismatch/ringdown stress but targets the right
rebar, target 2. This is a bounded GPU diagnostic on the already-established
Tx/Rx=50 mm variable-depth/radius final-state branch.

The previous three-seed target-2 package showed exact recovery for seed55,
seed13, and seed34. Run 741 asks whether the same behavior holds under the
additional seed21 stress.

## 741: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-2 Tx/Rx=50 Ringdown025 Objectives

Output:

```text
outputs/experiments/741_coordinate_optimizer_variable_depth_radius_seed21_target2_txrx50_ringdown025_objectives
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
  --replication-cases source_mismatch_ringdown025_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.25,180.0,0.8 \
  --update-case-label source_mismatch_ringdown025_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 10 \
  --progress-every 5 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target2_txrx50_ringdown025_objectives
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
case: source_mismatch_ringdown025_noise10_seed21
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 7.25 mm
absolute radius margin: 8.000475e-04
confidence label: moderate
ambiguity width: none recorded
```

Objective diagnostics:

| Objective | Best x/z/r mm | Next radius mm | Margin abs | Ratio to base |
| --- | --- | ---: | ---: | ---: |
| base | 350 / 120 / 8.0 | 7.25 | 8.000475e-04 | 1.000 |
| highband | 350 / 120 / 8.0 | 7.25 | 8.108765e-04 | 1.014 |
| late | 350 / 120 / 8.0 | 7.25 | 1.130809e-03 | 1.413 |
| late_high | 350 / 120 / 8.0 | 7.25 | 1.204660e-03 | 1.506 |
| veryhigh | 350 / 120 / 8.0 | 7.25 | 9.813856e-04 | 1.227 |
| early_high | 350 / 120 / 8.0 | 7.25 | 4.539323e-04 | 0.567 |

## Interpretation

Run 741 is consistent with the prior target-2 fitted-ringdown package. The base
objective remains exact and moderate under seed21. Late_high is the strongest
target-2 diagnostic, with a 1.506x margin ratio to base, while veryhigh also
improves the row without changing geometry.

Together with run 740, this shows the fourth-seed stress is not exposing a
new target-0 or target-2 failure in the Tx/Rx=50 final-state fitted-ringdown
branch.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=60, state history=2, candidates=10
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, nonblank
visual inspection: confidence figure is readable and matches the single moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: RAM healthy with about 100 GiB available after run
git diff --check: clean after run 741
```

## Next Decision

If the GPU remains healthy, run the heavier seed21 target-1 fitted-ringdown
diagnostic to complete the additional-seed all-target package. Keep the admin
cleanup outside numbered experiments, using the audit and append-only bundles
already created.
