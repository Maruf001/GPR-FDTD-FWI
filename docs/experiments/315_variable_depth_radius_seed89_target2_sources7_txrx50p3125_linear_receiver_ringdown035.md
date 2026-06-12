# Experiment 315: Seed89 Target-2 Sources=7 Linear Receiver Ringdown035

## Purpose

Run 782 tests whether the 7-source mitigation from run 780 transfers from
ringdown025 to the stronger ringdown035 source condition. It repeats run 779's
linear Tx/Rx=50.3125 mm ringdown035 target-2 setup, but increases the scan from
5 to 7 sources and keeps the full 27-candidate local z/radius grid.

## 782: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Sources=7 Tx/Rx=50.3125 Linear Receiver Ringdown035

Output:

```text
outputs/experiments/782_coordinate_optimizer_variable_depth_radius_seed89_target2_sources7_txrx50p3125_linear_receiver_ringdown035_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 7 \
  --tx-rx-offset-mm 50.3125 \
  --receiver-sampling linear \
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
  --z-offsets-mm=-1:1:1 \
  --radius-offsets-mm=-1:1:0.25 \
  --replication-cases source_mismatch_ringdown035_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.35,180.0,0.8 \
  --update-case-label source_mismatch_ringdown035_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 27 \
  --progress-every 5 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_sources7_txrx50p3125_linear_receiver_ringdown035_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 7
scan x positions: [50, 114, 178, 250, 314, 378, 450] mm
Tx/Rx offset: 50.3125 mm
receiver sampling: linear
frequency: 1.5 GHz
truth x/z/r: [150,250,350] / [80,100,120] / [5,6,8] mm
initial x/z/r: truth final state
target index: 2
candidate grid: x offset 0, z offsets -1/0/+1 mm, radius offsets -1 to +1 mm in 0.25 mm steps
candidate count: 27
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
case: source_mismatch_ringdown035_noise10_seed89
receiver sampling: linear
target: 2
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm at z=121 mm
absolute radius margin: 6.319852e-04
relative radius margin: 2.504789e-02
confidence label: moderate
best misfit: 0.0252310727166986
elapsed: 1192.12 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 6.319852e-04 | 1.000 |
| highband | 8.0 | 8.75 | 8.041313e-04 | 1.272 |
| late | 8.0 | 8.75 | 8.993099e-04 | 1.423 |
| late_high | 8.0 | 8.75 | 1.108424e-03 | 1.754 |
| veryhigh | 8.0 | 8.75 | 8.303698e-04 | 1.314 |
| early_high | 8.0 | 8.75 | 4.028774e-04 | 0.637 |

Cross-ringdown comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| ringdown035, 5 sources, linear Tx/Rx=50.3125 | 779 | 4.945264e-04 | 1.000 | weak |
| ringdown035, 7 sources, linear Tx/Rx=50.3125 | 782 | 6.319852e-04 | 1.278 vs run 779 | moderate |
| ringdown025, 7 sources, linear Tx/Rx=50.3125 | 780 | 6.453160e-04 | 0.979 vs run 780 | moderate |
| ringdown035, 5 sources, nearest Tx/Rx=50 | 750 | 1.038879e-03 | 0.608 vs run 750 | strong |

## Interpretation

Run 782 shows that the 7-source mitigation transfers to ringdown035. The
5-source ringdown035 linear row from run 779 was exact/weak; the 7-source row
is exact/moderate and improves the base margin by 27.8%.

The 7-source ringdown035 and ringdown025 linear rows are very close: run 782 is
0.979x run 780. This supports a source-density mitigation claim that is not
specific to the ringdown025 stress level. The same `z=121 mm, r=8.75 mm`
competitor remains the limiting next-radius geometry.

The result still does not fully recover the nearest-grid ringdown035 baseline:
run 782 is 0.608x run 750. The correct claim is mitigation to moderate
confidence, not restoration to the original nearest-grid strength.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=162, state history=2, candidates=27
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with full RGB dynamic range
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 89-90%; Python RSS stayed about 457 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Close the target-2 linear receiver source-density branch unless a compact
decision figure is needed. The next substantive GPU branch should test whether
7-source density also mitigates a different weak target-2 acquisition condition,
such as Tx/Rx=60.
