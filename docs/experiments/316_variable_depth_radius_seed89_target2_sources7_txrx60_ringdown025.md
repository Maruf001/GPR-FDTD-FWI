# Experiment 316: Seed89 Target-2 Sources=7 Tx/Rx=60 Ringdown025

## Purpose

Run 783 tests whether the 7-source mitigation also transfers to the separate
Tx/Rx=60 target-2 weak acquisition condition. It repeats run 755's Tx/Rx=60
ringdown025 target-2 setup, changing only the scan from 5 to 7 sources while
keeping the same 12-candidate local z/radius grid.

## 783: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Sources=7 Tx/Rx=60 Ringdown025

Output:

```text
outputs/experiments/783_coordinate_optimizer_variable_depth_radius_seed89_target2_sources7_txrx60_ringdown025_objectives
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
  --target-indices 2 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_sources7_txrx60_ringdown025_objectives
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
target index: 2
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
receiver sampling: nearest
target: 2
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm at z=121 mm
absolute radius margin: 5.100529e-04
relative radius margin: 2.796597e-02
confidence label: moderate
best misfit: 0.0182383444111407
elapsed: 524.17 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 5.100529e-04 | 1.000 |
| highband | 8.0 | 8.75 | 5.538466e-04 | 1.086 |
| late | 8.0 | 8.75 | 6.904350e-04 | 1.354 |
| late_high | 8.0 | 8.75 | 7.902812e-04 | 1.549 |
| veryhigh | 8.0 | 8.75 | 5.771242e-04 | 1.131 |
| early_high | 8.0 | 8.75 | 3.146680e-04 | 0.617 |

Tx/Rx=60 source-density comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| Tx/Rx=60, 5 sources | 755 | 4.318875e-04 | 1.000 | weak |
| Tx/Rx=60, 7 sources | 783 | 5.100529e-04 | 1.181 vs run 755 | moderate |
| Tx/Rx=50, 5 sources | 745 | 9.935884e-04 | 0.513 vs run 745 | moderate |

## Interpretation

Run 783 shows that the 7-source mitigation transfers beyond the linear
receiver branch. The Tx/Rx=60 target-2 row was exact/weak with 5 sources in run
755; with 7 sources it remains exact and crosses to moderate, with an 18.1%
larger base margin.

This is still not a restoration to the Tx/Rx=50 baseline. The 7-source Tx/Rx=60
margin is only 0.513x run 745, so the widened Tx/Rx geometry remains a
lower-margin acquisition condition.

Late_high remains the strongest truth-preserving diagnostic at 1.549x base.
The same `z=121 mm, r=8.75 mm` competitor remains the limiting geometry.

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

The 7-source mitigation now transfers across both linear receiver sampling and
Tx/Rx=60. The next useful step is to test whether this source-density effect is
target-2-specific by checking one shallower target under a weak or
margin-limited acquisition condition, or to create one compact decision figure
if reporting needs it.
