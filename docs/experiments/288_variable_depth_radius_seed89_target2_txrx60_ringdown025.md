# Experiment 288: Seed89 Target-2 Tx/Rx=60 Ringdown025 Diagnostic

## Purpose

Run 755 extends the Tx/Rx=60 acquisition-geometry stress to the deep target.
Run 754 showed target 1 remains exact/moderate but lower-margin than Tx/Rx=50.
This run checks whether the deep target remains exact and how much margin is
lost under the same widened acquisition geometry.

## 755: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Tx/Rx=60 Ringdown025 Objectives

Output:

```text
outputs/experiments/755_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx60_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_txrx60_ringdown025_objectives
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
next radius: 8.75 mm
absolute radius margin: 4.318875e-04
relative radius margin: 2.145013e-02
confidence label: weak
best misfit: 0.020134490802110043
```

Objective diagnostics:

| Objective | Best x/z/r mm | Next radius mm | Margin abs | Ratio to base |
| --- | --- | ---: | ---: | ---: |
| base | 350 / 120 / 8.0 | 8.75 | 4.318875e-04 | 1.000 |
| highband | 350 / 120 / 8.0 | 8.75 | 4.154480e-04 | 0.962 |
| late | 350 / 120 / 8.0 | 8.75 | 6.011155e-04 | 1.392 |
| late_high | 350 / 120 / 8.0 | 8.75 | 6.300136e-04 | 1.459 |
| veryhigh | 350 / 120 / 8.0 | 8.75 | 4.690339e-04 | 1.086 |
| early_high | 350 / 120 / 8.0 | 8.75 | 2.806038e-04 | 0.650 |

Tx/Rx=50 comparison:

| Metric | Run 745 Tx/Rx=50 | Run 755 Tx/Rx=60 | Tx/Rx60 / Tx/Rx50 |
| --- | ---: | ---: | ---: |
| Base margin | 9.935884e-04 | 4.318875e-04 | 0.435 |
| Late_high margin | 1.506552e-03 | 6.300136e-04 | 0.418 |
| Veryhigh margin | 1.358312e-03 | 4.690339e-04 | 0.345 |
| Early_high margin | 6.117933e-04 | 2.806038e-04 | 0.459 |

## Interpretation

Target 2 remains exact at Tx/Rx=60, but the confidence label drops from the
Tx/Rx=50 moderate row to weak. This is the strongest acquisition-geometry
sensitivity observed so far in the restored branch.

Late_high is still the strongest truth-preserving diagnostic, but both base
and diagnostic margins are much smaller than at Tx/Rx=50. This means the
branch should not be summarized as simply "robust"; it is exact but
margin-limited for the deep target.

The result should be carried forward as:

```text
Tx/Rx=60 target 2: exact geometry, weak radius confidence, late_high reporting evidence.
```

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, nonblank
visual inspection: confidence figure is readable and correctly flags the weak row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 87-88%; RAM stayed healthy with about 100 GiB available
```

## Next Decision

Run target 0 under the same Tx/Rx=60 branch. The branch now contains one
exact/moderate center target and one exact/weak deep target; the shallow
target is needed before packaging an all-target acquisition summary.
