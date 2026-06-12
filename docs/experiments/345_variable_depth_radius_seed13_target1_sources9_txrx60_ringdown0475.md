# Experiment 345: Seed13 Target-1 Sources=9 Tx/Rx=60 Ringdown0475

## Purpose

Run 811 refines the stronger source-ringdown bracket for the weakest replicated
policy row. It repeats seed13 target 1 with 9 sources and Tx/Rx=60 at the
midpoint between the ringdown045 pass and the ringdown050 weak row.

## 811: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-1 Sources=9 Tx/Rx=60 Ringdown0475

Output:

```text
outputs/experiments/811_coordinate_optimizer_variable_depth_radius_seed13_target1_sources9_txrx60_ringdown0475_objectives
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
  --replication-cases source_mismatch_ringdown0475_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.475,180.0,0.8 \
  --update-case-label source_mismatch_ringdown0475_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target1_sources9_txrx60_ringdown0475_objectives
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
case: source_mismatch_ringdown0475_noise10_seed13
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 4.963021e-04
relative radius margin: 3.062499e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.01620579000382596
next radius misfit: 0.016702092098565754
competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 716.96 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 4.963021e-04 | 1.000 | 1.620579e-02 |
| highband | 6.870513e-04 | 1.384 | 2.805776e-04 |
| late | 7.287932e-04 | 1.468 | 1.945138e-02 |
| late_high | 8.924289e-04 | 1.798 | 3.167557e-04 |
| veryhigh | 6.691836e-04 | 1.348 | 3.251378e-04 |
| early_high | 5.189956e-04 | 1.046 | 9.440536e-05 |

Ringdown bracket:

| Condition | Run | Base margin | Offset from cutoff | Confidence |
| --- | ---: | ---: | ---: | --- |
| seed13 target 1, ringdown045 | 809 | 5.030490e-04 | +3.049e-06 | moderate |
| seed13 target 1, ringdown0475 | 811 | 4.963021e-04 | -3.698e-06 | weak |
| seed13 target 1, ringdown050 | 810 | 4.879320e-04 | -1.207e-05 | weak |

## Interpretation

Run 811 tightens the base-confidence transition. The target remains exact, but
the production base row is weak at ringdown0475. The confidence transition is
now bracketed between ringdown045 and ringdown0475 for seed13 target 1 at
9 sources.

The row is only slightly below the cutoff, and all diagnostic objective
variants are truth-preserving. That supports one tighter midpoint check at
ringdown04625 if a numeric threshold estimate is needed; otherwise the branch
can already be summarized as a target-1 base-margin threshold around
0.46-0.47 ringdown scale.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.249 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one weak row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 90-92%; Python RSS stayed about 453-460 MiB; RAM stayed about 98-99 GiB available
elapsed: 716.96 s
```

## Next Decision

Run one tighter midpoint at ringdown04625 to locate the threshold more
precisely before summarizing the stronger-ringdown target-1 branch.

