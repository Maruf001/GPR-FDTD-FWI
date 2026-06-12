# Experiment 295: Seed89 Target-2 Tx/Rx=51.25 Ringdown025 Diagnostic

## Purpose

Run 762 narrows the target-2 Tx/Rx confidence transition. After run 761 showed
that Tx/Rx=52.5 is weak, this run tests the midpoint between Tx/Rx=50 and
Tx/Rx=52.5.

## 762: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Tx/Rx=51.25 Ringdown025 Objectives

Output:

```text
outputs/experiments/762_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx51p25_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 51.25 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_txrx51p25_ringdown025_objectives
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
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 4.752760e-04
relative radius margin: 1.809307e-02
confidence label: weak
best misfit: 0.026268405791449057
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 4.752760e-04 | 1.000 |
| highband | 8.0 | 8.75 | 4.611963e-04 | 0.970 |
| late | 8.0 | 8.75 | 7.030455e-04 | 1.479 |
| late_high | 8.0 | 8.75 | 7.659871e-04 | 1.612 |
| veryhigh | 8.0 | 8.75 | 5.517761e-04 | 1.161 |
| early_high | 8.0 | 8.75 | 2.763888e-04 | 0.582 |

Target-2 offset comparison:

| Tx/Rx offset | Base margin | Confidence | Ratio to 50 mm |
| ---: | ---: | --- | ---: |
| 50 mm | 9.935884e-04 | moderate | 1.000 |
| 51.25 mm | 4.752760e-04 | weak | 0.478 |
| 52.5 mm | 4.724547e-04 | weak | 0.475 |
| 55 mm | 4.604568e-04 | weak | 0.463 |
| 60 mm | 4.318875e-04 | weak | 0.435 |

## Interpretation

Tx/Rx=51.25 is still exact/weak. The confidence transition is now constrained
to the interval from Tx/Rx=50 to Tx/Rx=51.25.

The drop is abrupt: the margin is roughly half the Tx/Rx=50 margin already at
51.25 mm, then changes only gradually through 60 mm.

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

Run Tx/Rx=50.625 target 2 to refine the transition interval between the
moderate 50 mm result and weak 51.25 mm result.
