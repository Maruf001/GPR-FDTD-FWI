# Experiment 298: Seed89 Target-2 Tx/Rx=50.3125 Linear-Receiver Diagnostic

## Purpose

Run 765 starts the linear receiver-sampling branch. The preceding nearest-grid
summary showed that fractional Tx/Rx offsets can duplicate receiver-index
layouts; this run makes Tx/Rx=50.3125 mm a true sub-grid receiver sample by
recording a weighted average of adjacent receiver cells.

## 765: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Tx/Rx=50.3125 Linear Receiver Ringdown025

Output:

```text
outputs/experiments/765_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p3125_linear_receiver_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 50.3125 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p3125_linear_receiver_ringdown025_objectives
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
absolute radius margin: 4.769427e-04
relative radius margin: 1.784121e-02
confidence label: weak
best misfit: 0.0267326398663861
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 4.769427e-04 | 1.000 |
| highband | 8.0 | 8.75 | 4.633331e-04 | 0.971 |
| late | 8.0 | 8.75 | 7.056496e-04 | 1.480 |
| late_high | 8.0 | 8.75 | 7.692222e-04 | 1.613 |
| veryhigh | 8.0 | 8.75 | 5.557763e-04 | 1.165 |
| early_high | 8.0 | 8.75 | 2.752698e-04 | 0.577 |

Nearest-grid comparison:

| Condition | Base margin | Confidence | Ratio to nearest Tx/Rx=50 |
| --- | ---: | --- | ---: |
| nearest Tx/Rx=50.000 | 9.935884e-04 | moderate | 1.000 |
| linear Tx/Rx=50.3125 | 4.769427e-04 | weak | 0.480 |
| nearest Tx/Rx=50.625/51.25 layout | 4.752760e-04 | weak | 0.478 |

## Interpretation

The interpolated midpoint does not recover the moderate Tx/Rx=50 margin. Its
base margin is essentially on the nearest-grid +51 weak branch, only 1.0035x
the nearest-grid Tx/Rx=50.625/51.25 margin and 0.480x the nearest-grid Tx/Rx=50
margin.

This indicates that receiver-index rounding was not the only issue. Under
linear sampling, target 2 weakens as soon as the receiver trace includes a
meaningful contribution from the +51 cell.

## Validation

```text
focused pytest: tests/test_multi_rebar_local_geometry_profile.py and tests/test_txrx_target2_threshold_summary.py -> 20 passed
tiny GPU smoke: linear 6-entry receiver positions run through gpu-cpml batch recorder without error
full pytest: 288 passed in 24.71s
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, nonblank
visual inspection: confidence figure is readable and correctly flags the weak row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 87-88%; RAM stayed healthy with about 100 GiB available
```

## Next Decision

Run linear receiver sampling at Tx/Rx=50.000 mm as a baseline. If it remains
moderate, the interpolated transition is between 50.000 and 50.3125 mm. If it
weakens, interpolation itself changes the branch and the linear-sampling
baseline set needs to be expanded before more midpoint bisection.
