# Experiment 289: Seed89 Target-0 Tx/Rx=60 Ringdown025 Diagnostic

## Purpose

Run 756 completes the target-specific Tx/Rx=60 acquisition-geometry branch.
Runs 754 and 755 showed exact target 1 and target 2 geometry, with target 2
dropping to weak confidence. This run checks whether the shallow target keeps
the established target-0 diagnostic pattern under the widened offset.

## 756: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-0 Tx/Rx=60 Ringdown025 Objectives

Output:

```text
outputs/experiments/756_coordinate_optimizer_variable_depth_radius_seed89_target0_txrx60_ringdown025_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target0_txrx60_ringdown025_objectives
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
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.193087e-04
relative radius margin: 2.579200e-02
confidence label: moderate
best misfit: 0.020134490802110043
```

Objective diagnostics:

| Objective | Best x/z/r mm | Next radius mm | Margin abs | Ratio to base |
| --- | --- | ---: | ---: | ---: |
| base | 150 / 80 / 5.0 | 5.25 | 5.193087e-04 | 1.000 |
| highband | 150 / 80 / 5.0 | 5.25 | 5.244956e-04 | 1.010 |
| late | 150 / 80 / 5.0 | 5.25 | 2.705668e-04 | 0.521 |
| late_high | 150 / 80 / 5.0 | 5.25 | 2.771375e-04 | 0.534 |
| veryhigh | 150 / 80 / 5.0 | 5.25 | 6.449654e-04 | 1.242 |
| early_high | 150 / 80 / 5.0 | 5.25 | 4.109750e-04 | 0.791 |

Tx/Rx=50 comparison:

| Metric | Run 744 Tx/Rx=50 | Run 756 Tx/Rx=60 | Tx/Rx60 / Tx/Rx50 |
| --- | ---: | ---: | ---: |
| Base margin | 5.798369e-04 | 5.193087e-04 | 0.896 |
| Veryhigh margin | 7.857061e-04 | 6.449654e-04 | 0.821 |
| Late_high margin | 4.266862e-04 | 2.771375e-04 | 0.650 |
| Early_high margin | 4.304748e-04 | 4.109750e-04 | 0.955 |

## Interpretation

Target 0 remains exact/moderate at Tx/Rx=60, but the base margin is 0.896x
the Tx/Rx=50 seed89 target-0 margin. The target-specific objective pattern is
unchanged: veryhigh is strongest, while late and late_high weaken the shallow
target.

Together with runs 754-755, this closes the target-specific Tx/Rx=60 branch:

```text
target 0: exact/moderate, lower margin, veryhigh strongest
target 1: exact/moderate, lower margin, late_high strongest
target 2: exact/weak, sharply lower margin, late_high strongest
```

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, nonblank
visual inspection: confidence figure is readable and matches the single moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 87-88%; RAM stayed healthy with about 100 GiB available
```

## Next Decision

Package a Tx/Rx=60 all-target summary using runs 756, 754, and 755. That
summary should compare directly against the Tx/Rx=50 seed89 package and call
out target 2 as exact but weak.
