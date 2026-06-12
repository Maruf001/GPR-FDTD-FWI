# Experiment 292: Tx/Rx=60 Target-2 Fine-Radius Diagnostic

## Purpose

Run 759 follows up the exact/weak Tx/Rx=60 target-2 row from run 755. It fixes
target 2 at the recovered x/z truth position and evaluates a 0.125 mm radius
grid from 7.5 mm to 9.5 mm under the same seed89 ringdown025 source stress.

The goal is to decide whether the weak confidence row is a coarse-grid artifact
or a genuine shallow radius basin.

## 759: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Tx/Rx=60 Fine-Radius Objectives

Output:

```text
outputs/experiments/759_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx60_ringdown025_fine_radius_objectives
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
  --z-offsets-mm=0 \
  --radius-offsets-mm=-0.5:1.5:0.125 \
  --replication-cases source_mismatch_ringdown025_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.25,180.0,0.8 \
  --update-case-label source_mismatch_ringdown025_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 17 \
  --progress-every 4 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_txrx60_ringdown025_fine_radius_objectives
```

Artifacts:

```text
README.md
data/coordinate_confidence_report.csv
data/coordinate_objective_diagnostics.csv
data/coordinate_objective_top_candidates.csv
data/coordinate_state_history.csv
data/coordinate_step_01_target_2_candidates.csv
data/fine_radius_objective_curves.csv
data/multi_rebar_coordinate_optimizer_summary.json
figures/coordinate_confidence_margins.png
figures/txrx60_target2_fine_radius_objective_curves.png
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
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 7.875 mm
absolute radius margin: 4.330190e-04
relative radius margin: 2.150633e-02
confidence label: weak
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 7.875 | 4.330190e-04 | 1.000 |
| highband | 8.0 | 7.875 | 4.462036e-04 | 1.030 |
| late | 8.0 | 7.875 | 6.749730e-04 | 1.559 |
| late_high | 8.0 | 7.875 | 6.850906e-04 | 1.582 |
| veryhigh | 8.0 | 7.875 | 4.681221e-04 | 1.081 |
| early_high | 8.0 | 7.875 | 2.749939e-04 | 0.635 |

Coarse-to-fine comparison:

| Run | Radius step | Best radius | Next radius | Base margin | Confidence |
| --- | ---: | ---: | ---: | ---: | --- |
| 755 | 0.25 mm with z 0/1 mm | 8.0 | 8.75 | 4.318875e-04 | weak |
| 759 | 0.125 mm at fixed x/z | 8.0 | 7.875 | 4.330190e-04 | weak |

## Interpretation

The fine-radius grid confirms the weak target-2 confidence under Tx/Rx=60. The
truth radius remains the best candidate, but the nearest fine-grid competitor
is close. The weak label is therefore a real shallow-radius-basin result, not
a coarse-grid artifact.

Late_high continues to provide the strongest truth-preserving diagnostic
margin. It is useful for reporting the basin shape, but it does not alter the
production update rule.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=102, state history=2, candidates=17
fine-radius curve CSV rows: 102
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255
figure validation: txrx60_target2_fine_radius_objective_curves.png is 1515x869, dynamic range 255
visual inspection: both figures are readable
figure notes: figures/FIGURE_NOTES.md present and describes both figures
```

## Next Decision

Run an intermediate Tx/Rx=55 target-2 row. This should locate whether the
confidence degradation begins gradually between Tx/Rx=50 and Tx/Rx=60, or
whether the weak label appears abruptly near the wider offset.
