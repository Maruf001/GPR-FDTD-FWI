# Experiment 348: Seed13 Target-1 Sources=9 Tx/Rx=60 Ringdown0459375

## Purpose

Run 814 resolves the quarter-point between the passing ringdown045625 row and
the weak ringdown04625 row for the weakest replicated policy case. It repeats
seed13 target 1 with 9 sources and Tx/Rx=60 at ringdown scale 0.459375.

## 814: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-1 Sources=9 Tx/Rx=60 Ringdown0459375

Output:

```text
outputs/experiments/814_coordinate_optimizer_variable_depth_radius_seed13_target1_sources9_txrx60_ringdown0459375_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 9 \
  --tx-rx-offset-mm 60 \
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
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown0459375_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.459375,180.0,0.8 \
  --update-case-label source_mismatch_ringdown0459375_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target1_sources9_txrx60_ringdown0459375_objectives
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
case: source_mismatch_ringdown0459375_noise10_seed13
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.007215e-04
relative radius margin: 3.038652e-02
confidence label: moderate
fallback warning: none
best misfit: 0.0164784067129565
next radius misfit: 0.01697912819723996
competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 688.74 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.007215e-04 | 1.000 | 1.647841e-02 |
| highband | 6.819755e-04 | 1.362 | 2.805839e-04 |
| late | 7.302125e-04 | 1.458 | 1.965674e-02 |
| late_high | 8.910427e-04 | 1.780 | 3.190399e-04 |
| veryhigh | 6.650569e-04 | 1.328 | 3.271457e-04 |
| early_high | 5.103593e-04 | 1.019 | 9.350001e-05 |

Ringdown bracket:

| Condition | Run | Base margin | Offset from cutoff | Confidence |
| --- | ---: | ---: | ---: | --- |
| seed13 target 1, ringdown045 | 809 | 5.030490e-04 | +3.049e-06 | moderate |
| seed13 target 1, ringdown045625 | 813 | 5.015250e-04 | +1.525e-06 | moderate |
| seed13 target 1, ringdown0459375 | 814 | 5.007215e-04 | +7.215e-07 | moderate |
| seed13 target 1, ringdown04625 | 812 | 4.998907e-04 | -1.093e-07 | weak |
| seed13 target 1, ringdown0475 | 811 | 4.963021e-04 | -3.698e-06 | weak |
| seed13 target 1, ringdown050 | 810 | 4.879320e-04 | -1.207e-05 | weak |

## Interpretation

Run 814 tightens the stronger-ringdown target-1 threshold branch to a
0.003125-wide interval. The production base row still passes at ringdown
0.459375 with a `5.007e-04` margin, while run 812 is weak at 0.4625 with a
`4.999e-04` margin.

The sequence is now precise enough for a threshold summary: the estimated
cutoff lies between 0.459375 and 0.4625, with midpoint 0.4609375. The target
geometry stays exact throughout runs 809-814, so this threshold is a
confidence-margin limit, not a coordinate/radius-selection limit.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.243 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 91%; Python RSS stayed about 453-459 MiB; RAM stayed about 98-99 GiB available
elapsed: 688.74 s
```

## Next Decision

Create a compact threshold summary for runs 809-814, then move the stronger
ringdown stress to another target rather than continuing to slice target 1
below a 0.003125 ringdown-scale bracket.

