# Experiment 287: Seed89 Target-1 Tx/Rx=60 Ringdown025 Diagnostic

## Purpose

Run 754 starts the next substantive GPU branch after closing the ringdown035
summary. It widens the Tx/Rx offset from 50 mm to 60 mm while keeping the
seed89 ringdown025 source-mismatch stress, final truth state, source-fit grid,
and objective diagnostics fixed.

The center target is run first because it was the most seed-sensitive row in
the seed21/seed89 comparison.

## 754: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-1 Tx/Rx=60 Ringdown025 Objectives

Output:

```text
outputs/experiments/754_coordinate_optimizer_variable_depth_radius_seed89_target1_txrx60_ringdown025_objectives
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
  --target-indices 1 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target1_txrx60_ringdown025_objectives
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
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.319351e-04
relative radius margin: 2.641910e-02
confidence label: moderate
best misfit: 0.020134490802110043
```

Objective diagnostics:

| Objective | Best x/z/r mm | Next radius mm | Margin abs | Ratio to base |
| --- | --- | ---: | ---: | ---: |
| base | 250 / 100 / 6.0 | 6.25 | 5.319351e-04 | 1.000 |
| highband | 250 / 100 / 6.0 | 6.25 | 5.728960e-04 | 1.077 |
| late | 250 / 100 / 6.0 | 6.25 | 7.173641e-04 | 1.349 |
| late_high | 250 / 100 / 6.0 | 6.25 | 7.784420e-04 | 1.463 |
| veryhigh | 250 / 100 / 6.0 | 6.25 | 6.542461e-04 | 1.230 |
| early_high | 250 / 100 / 6.0 | 6.25 | 3.953794e-04 | 0.743 |

Tx/Rx=50 comparison:

| Metric | Run 746 Tx/Rx=50 | Run 754 Tx/Rx=60 | Tx/Rx60 / Tx/Rx50 |
| --- | ---: | ---: | ---: |
| Base margin | 5.982895e-04 | 5.319351e-04 | 0.889 |
| Late_high margin | 8.565618e-04 | 7.784420e-04 | 0.909 |
| Veryhigh margin | 7.305676e-04 | 6.542461e-04 | 0.896 |
| Early_high margin | 3.964496e-04 | 3.953794e-04 | 0.997 |

## Interpretation

The acquisition-geometry stress is not a geometry failure: target 1 remains
exact and moderate at Tx/Rx=60.

It is, however, a real margin sensitivity. The base margin drops to 0.889x the
Tx/Rx=50 seed89 target-1 margin, and late_high also drops to 0.909x the
Tx/Rx=50 late_high margin. Late_high still has the strongest truth-preserving
diagnostic ratio, increasing the Tx/Rx=60 base margin by 1.463x.

This preserves the production rule:

```text
Use base for coordinate updates.
Use late_high as target-1 reporting evidence when geometry is preserved.
Report Tx/Rx=60 as lower-margin but still exact/moderate so far.
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

Run Tx/Rx=60 seed89 ringdown025 target 2 next. Target 1 is exact but lower
margin than Tx/Rx=50, so the acquisition-geometry branch needs the deep target
before deciding whether to complete the all-target package.
