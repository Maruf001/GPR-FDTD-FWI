# Experiment 317: Seed89 Target-0 Sources=7 Tx/Rx=60 Ringdown025

## Purpose

Run 784 checks whether the 7-source Tx/Rx=60 mitigation is target-2-specific.
It repeats run 756's target-0 Tx/Rx=60 ringdown025 setup, changing only the
scan from 5 to 7 sources while keeping the same 12-candidate local z/radius
grid.

## 784: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-0 Sources=7 Tx/Rx=60 Ringdown025

Output:

```text
outputs/experiments/784_coordinate_optimizer_variable_depth_radius_seed89_target0_sources7_txrx60_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 7 \
  --tx-rx-offset-mm 60 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target0_sources7_txrx60_ringdown025_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 7
scan x positions: [50, 114, 178, 250, 314, 378, 450] mm
Tx/Rx offset: 60 mm
receiver sampling: nearest
frequency: 1.5 GHz
truth x/z/r: [150,250,350] / [80,100,120] / [5,6,8] mm
initial x/z/r: truth final state
target index: 0
candidate grid: x offset 0, z offsets 0/+1 mm, radius offsets 0 to +1.25 mm in 0.25 mm steps
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
receiver sampling: nearest
target: 0
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm at z=81 mm
absolute radius margin: 5.677174e-04
relative radius margin: 3.112768e-02
confidence label: moderate
best misfit: 0.0182383444111407
elapsed: 522.56 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 5.0 | 5.25 | 5.677174e-04 | 1.000 |
| highband | 5.0 | 5.25 | 5.857831e-04 | 1.032 |
| late | 5.0 | 5.25 | 5.294302e-04 | 0.933 |
| late_high | 5.0 | 5.25 | 5.513723e-04 | 0.971 |
| veryhigh | 5.0 | 5.25 | 5.551443e-04 | 0.978 |
| early_high | 5.0 | 5.25 | 4.313636e-04 | 0.760 |

Target/source-density comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| target 0, Tx/Rx=60, 5 sources | 756 | 5.193087e-04 | 1.000 | moderate |
| target 0, Tx/Rx=60, 7 sources | 784 | 5.677174e-04 | 1.093 vs run 756 | moderate |
| target 2, Tx/Rx=60, 7 sources | 783 | 5.100529e-04 | 1.113 vs run 783 | moderate |

## Interpretation

Run 784 shows that the 7-source benefit is not target-2-only. Target 0 already
had moderate confidence at Tx/Rx=60 with 5 sources, and 7 sources raises its
base margin by 9.3% while preserving exact geometry.

The effect is smaller than the target-2 classification rescue from run 783.
For target 0, source density improves an already moderate row; for target 2, it
crosses weak to moderate.

Unlike target 2, the base objective is the strongest target-0 variant in this
run.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with full RGB dynamic range
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 89-90%; Python RSS stayed about 453 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Run target 1 at the same Tx/Rx=60, 7-source condition to complete the all-target
source-density comparison before creating any summary figure.
