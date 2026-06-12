# Experiment 302: Seed89 Target-2 Tx/Rx=50.0390625 Linear-Receiver Diagnostic

## Purpose

Run 769 is the final planned lower-bound bisection for the target-2 linear
receiver-sampling branch. It tests whether a very small nonzero +51 receiver
contribution still pushes the target-2 radius confidence into the weak regime.

## 769: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Tx/Rx=50.0390625 Linear Receiver Ringdown025

Output:

```text
outputs/experiments/769_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p0390625_linear_receiver_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 50.0390625 \
  --receiver-sampling linear \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p0390625_linear_receiver_ringdown025_objectives
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
receiver sampling: linear
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 4.775098e-04
relative radius margin: 1.773915e-02
confidence label: weak
best misfit: 0.0269184201326113
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 4.775098e-04 | 1.000 |
| highband | 8.0 | 8.75 | 4.641001e-04 | 0.972 |
| late | 8.0 | 8.75 | 7.065257e-04 | 1.480 |
| late_high | 8.0 | 8.75 | 7.702463e-04 | 1.613 |
| veryhigh | 8.0 | 8.75 | 5.571031e-04 | 1.167 |
| early_high | 8.0 | 8.75 | 2.747406e-04 | 0.575 |

## Interpretation

Linear Tx/Rx=50.0390625 is exact/weak. Its margin is essentially the same as
the larger nonzero linear offsets and remains about 0.481x the nearest-grid
Tx/Rx=50 baseline margin.

This closes the practical linear receiver bisection: target 2 weakens for every
tested nonzero receiver perturbation away from the integer Tx/Rx=50 baseline.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, nonblank
visual inspection: confidence figure is readable and correctly flags the weak row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 87-88%; RAM stayed healthy with about 100 GiB available
prior code validation: full pytest after linear receiver implementation and summary script -> 292 passed in 24.68s
```

## Next Decision

Create a final linear receiver threshold summary including run 769, then stop
linear Tx/Rx bisection for this target/case.
