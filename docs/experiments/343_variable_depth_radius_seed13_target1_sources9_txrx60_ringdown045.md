# Experiment 343: Seed13 Target-1 Sources=9 Tx/Rx=60 Ringdown045

## Purpose

Run 809 starts a stronger source-condition stress branch from the weakest row
in the three-seed ringdown035 policy summary. It repeats seed13 target 1 with
9 sources and Tx/Rx=60, increasing the true ringdown scale from 0.35 to 0.45.

## 809: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-1 Sources=9 Tx/Rx=60 Ringdown045

Output:

```text
outputs/experiments/809_coordinate_optimizer_variable_depth_radius_seed13_target1_sources9_txrx60_ringdown045_objectives
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
  --replication-cases source_mismatch_ringdown045_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.45,180.0,0.8 \
  --update-case-label source_mismatch_ringdown045_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target1_sources9_txrx60_ringdown045_objectives
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
case: source_mismatch_ringdown045_noise10_seed13
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.030490e-04
relative radius margin: 3.023335e-02
confidence label: moderate
best misfit: 0.016638877625725034
next radius misfit: 0.01714192662476062
competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 713.95 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.030490e-04 | 1.000 | 1.663888e-02 |
| highband | 6.783714e-04 | 1.349 | 2.804559e-04 |
| late | 7.307518e-04 | 1.453 | 1.977900e-02 |
| late_high | 8.896187e-04 | 1.768 | 3.203231e-04 |
| veryhigh | 6.624670e-04 | 1.317 | 3.284533e-04 |
| early_high | 5.049040e-04 | 1.004 | 9.293355e-05 |

Ringdown comparison:

| Condition | Run | Base margin | Ratio vs ringdown035 | Confidence |
| --- | ---: | ---: | ---: | --- |
| seed13 target 1, ringdown035 | 806 | 5.109178e-04 | 1.000 | moderate |
| seed13 target 1, ringdown045 | 809 | 5.030490e-04 | 0.985 | moderate |

## Interpretation

Run 809 is an exact but near-threshold pass. Increasing the true ringdown scale
from 0.35 to 0.45 only reduces the base margin by about 1.5%, but the starting
row was already the weakest row in the three-seed policy summary. The margin is
now only 3.049e-06 above the moderate cutoff.

This means the 8/9/9 policy is not immediately broken by ringdown045 on the
weakest replicated row, but it is close enough to the cutoff that a single
ringdown050 target-1 check is justified before testing other targets or
summarizing the stronger-stress branch.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.255 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 90-91%; Python RSS stayed about 453-459 MiB; RAM stayed about 98-99 GiB available
elapsed: 713.95 s
```

## Next Decision

Run the same seed13 target-1 9-source Tx/Rx=60 check at ringdown050 to bracket
whether the weakest row crosses from moderate to weak under stronger source
ringdown.

