# Experiment 370: Seed21 Target-1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 836 completes the three-seed target-1 transfer set for the 5-source
ringdown050 policy. Seed13 and seed89 already passed in runs 834 and 835; this
run checks whether seed21 also supports the higher ringdown stress.

## 836: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/836_coordinate_optimizer_variable_depth_radius_seed21_target1_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target1_sources5_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed21
target: 1
sources: 5
scan x positions: [50, 146, 250, 346, 450] mm
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.799191e-04
relative radius margin: 3.439684e-02
confidence label: moderate
fallback warning: none
best misfit: 0.016859659349330584
next radius misfit: 0.01743957841767568
listed competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 384.62 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.799191e-04 | 1.000 | 1.685966e-02 |
| highband | 7.550503e-04 | 1.302 | 2.821059e-04 |
| late | 8.166866e-04 | 1.408 | 2.066253e-02 |
| late_high | 9.428009e-04 | 1.626 | 2.723230e-04 |
| veryhigh | 6.754687e-04 | 1.165 | 3.241786e-04 |
| early_high | 5.578231e-04 | 0.962 | 9.565358e-05 |

## Interpretation

Run 836 is a positive seed21 transfer result and the strongest target-1
ringdown050 row among the three seeds so far. It remains exact/moderate with a
`5.799191e-04` production margin, `7.992e-05` above cutoff.

Relative to seed13 run 834 at the same policy, run 836 is stronger by
`5.053e-05` and a 1.095x ratio. Relative to seed89 run 835, it is stronger by
`2.083e-05`. It is also stronger than seed21's 9-source ringdown0459375
transfer row from run 820 by `2.386e-05`, despite the higher ringdown stress.

All objective diagnostics are truth-preserving and above cutoff. The
early_high diagnostic is the smallest diagnostic row but still clears cutoff
by `5.782e-05`.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.291050 and full 0-255 RGB-converted dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 88%; Python RSS stayed about 447-453 MiB; RAM stayed about 98-99 GiB available
elapsed: 384.62 s
```

## Next Decision

Create a three-seed target-1 transfer summary for the 5-source ringdown050
policy from runs 834, 835, and 836. If the summary confirms all rows are
exact/moderate and all diagnostics preserve truth, extend the policy to the
remaining targets.
