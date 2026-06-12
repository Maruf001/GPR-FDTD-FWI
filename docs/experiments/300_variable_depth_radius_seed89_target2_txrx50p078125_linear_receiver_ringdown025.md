# Experiment 300: Seed89 Target-2 Tx/Rx=50.078125 Linear-Receiver Diagnostic

## Purpose

Run 767 tests the next smaller nonzero linear receiver-sampling offset after
linear Tx/Rx=50.15625 and 50.3125 mm both returned exact/weak target-2
recoveries.

## 767: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Tx/Rx=50.078125 Linear Receiver Ringdown025

Output:

```text
outputs/experiments/767_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p078125_linear_receiver_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 50.078125 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p078125_linear_receiver_ringdown025_objectives
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
absolute radius margin: 4.774322e-04
relative radius margin: 1.775378e-02
confidence label: weak
best misfit: 0.0268918627211681
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 4.774322e-04 | 1.000 |
| highband | 8.0 | 8.75 | 4.639934e-04 | 0.972 |
| late | 8.0 | 8.75 | 7.064062e-04 | 1.480 |
| late_high | 8.0 | 8.75 | 7.701092e-04 | 1.613 |
| veryhigh | 8.0 | 8.75 | 5.569229e-04 | 1.166 |
| early_high | 8.0 | 8.75 | 2.748190e-04 | 0.576 |

## Interpretation

Linear Tx/Rx=50.078125 is exact/weak and is effectively on the same weak
plateau as linear Tx/Rx=50.15625 and 50.3125. The remaining transition interval
is between exact Tx/Rx=50.000 and linear Tx/Rx=50.078125.

The next step should be a compact branch summary before spending another GPU
run on Tx/Rx=50.0390625.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, nonblank
visual inspection: confidence figure is readable and correctly flags the weak row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 87-88%; RAM stayed healthy with about 100 GiB available
prior code validation: full pytest after linear receiver implementation -> 288 passed in 24.71s
```

## Next Decision

Create a linear-threshold summary from the exact Tx/Rx=50 baseline and runs
765-767, then decide whether Tx/Rx=50.0390625 is worth a final GPU bisection.
