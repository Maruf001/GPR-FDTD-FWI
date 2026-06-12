# Experiment 347: Seed13 Target-1 Sources=9 Tx/Rx=60 Ringdown045625

## Purpose

Run 813 continues the stronger source-ringdown confidence threshold search for
the weakest replicated policy row. It repeats seed13 target 1 with 9 sources
and Tx/Rx=60 at the midpoint between the ringdown045 pass and the ringdown04625
weak row.

## 813: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-1 Sources=9 Tx/Rx=60 Ringdown045625

Output:

```text
outputs/experiments/813_coordinate_optimizer_variable_depth_radius_seed13_target1_sources9_txrx60_ringdown045625_objectives
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
  --replication-cases source_mismatch_ringdown045625_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.45625,180.0,0.8 \
  --update-case-label source_mismatch_ringdown045625_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target1_sources9_txrx60_ringdown045625_objectives
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
case: source_mismatch_ringdown045625_noise10_seed13
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.015250e-04
relative radius margin: 3.033628e-02
confidence label: moderate
fallback warning: none
best misfit: 0.01653218359882443
next radius misfit: 0.017033708628532738
competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 689.54 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.015250e-04 | 1.000 | 1.653218e-02 |
| highband | 6.808197e-04 | 1.357 | 2.805521e-04 |
| late | 7.304185e-04 | 1.456 | 1.969759e-02 |
| late_high | 8.906172e-04 | 1.776 | 3.194751e-04 |
| veryhigh | 6.642030e-04 | 1.324 | 3.275730e-04 |
| early_high | 5.085623e-04 | 1.014 | 9.331300e-05 |

Ringdown bracket:

| Condition | Run | Base margin | Offset from cutoff | Confidence |
| --- | ---: | ---: | ---: | --- |
| seed13 target 1, ringdown045 | 809 | 5.030490e-04 | +3.049e-06 | moderate |
| seed13 target 1, ringdown045625 | 813 | 5.015250e-04 | +1.525e-06 | moderate |
| seed13 target 1, ringdown04625 | 812 | 4.998907e-04 | -1.093e-07 | weak |
| seed13 target 1, ringdown0475 | 811 | 4.963021e-04 | -3.698e-06 | weak |
| seed13 target 1, ringdown050 | 810 | 4.879320e-04 | -1.207e-05 | weak |

## Interpretation

Run 813 shifts the lower side of the stronger-ringdown bracket upward. The
target remains exact and the production base row is moderate at ringdown045625,
with the base margin `1.525e-06` above the confidence cutoff.

The pass at 0.45625 and weak result at 0.4625 place the target-1 production
base-confidence threshold inside a narrow 0.00625 ringdown-scale interval. The
result is internally consistent with the previous sequence: as ringdown scale
increases from 0.45 to 0.4625, the base margin moves from a near-threshold pass
to a boundary weak row while all diagnostic objectives continue to preserve
the true geometry.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.246 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 91%; Python RSS stayed about 453-459 MiB; RAM stayed about 98-99 GiB available
elapsed: 689.54 s
```

## Next Decision

Run one quarter-point midpoint at ringdown0459375. If it passes, the threshold
falls between 0.459375 and 0.4625; if it is weak, the threshold falls between
0.45625 and 0.459375. After that, summarize the stronger-ringdown target-1
threshold branch.

