# Experiment 294: Seed89 Target-2 Tx/Rx=52.5 Ringdown025 Diagnostic

## Purpose

Run 761 narrows the target-2 acquisition transition. After run 760 showed that
Tx/Rx=55 is weak, this run tests the midpoint between Tx/Rx=50 and Tx/Rx=55.

## 761: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Tx/Rx=52.5 Ringdown025 Objectives

Output:

```text
outputs/experiments/761_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx52p5_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 52.5 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_txrx52p5_ringdown025_objectives
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
absolute radius margin: 4.724547e-04
relative radius margin: 1.848477e-02
confidence label: weak
best misfit: 0.025559134542240132
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 4.724547e-04 | 1.000 |
| highband | 8.0 | 8.75 | 4.576943e-04 | 0.969 |
| late | 8.0 | 8.75 | 6.976247e-04 | 1.477 |
| late_high | 8.0 | 8.75 | 7.591840e-04 | 1.607 |
| veryhigh | 8.0 | 8.75 | 5.453767e-04 | 1.154 |
| early_high | 8.0 | 8.75 | 2.779828e-04 | 0.588 |

Target-2 offset comparison:

| Tx/Rx offset | Base margin | Confidence | Ratio to 50 mm |
| ---: | ---: | --- | ---: |
| 50 mm | 9.935884e-04 | moderate | 1.000 |
| 52.5 mm | 4.724547e-04 | weak | 0.475 |
| 55 mm | 4.604568e-04 | weak | 0.463 |
| 60 mm | 4.318875e-04 | weak | 0.435 |

## Interpretation

Tx/Rx=52.5 remains exact but weak. The confidence transition is now narrowed
to the interval between Tx/Rx=50 and Tx/Rx=52.5.

The margin values suggest a sharp drop immediately beyond 50 mm rather than a
gradual decline across 52.5-60 mm. The next midpoint is Tx/Rx=51.25.

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

Run Tx/Rx=51.25 target 2 to refine the transition interval between the
moderate 50 mm result and weak 52.5 mm result.
