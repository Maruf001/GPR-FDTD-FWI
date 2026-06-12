# Experiment 372: Seed13 Target-2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 838 extends the 5-source ringdown050 policy from centered target 1 to
right-side target 2 for seed13. This checks whether the lower source count is
target-1-specific or can support another target that previously used the
9-source policy.

## 838: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/838_coordinate_optimizer_variable_depth_radius_seed13_target2_sources5_txrx60_ringdown050_objectives
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
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown050_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target2_sources5_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed13
target: 2
sources: 5
scan x positions: [50, 146, 250, 346, 450] mm
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.882895e-04
relative radius margin: 3.402730e-02
confidence label: moderate
fallback warning: none
best misfit: 0.017288749596645378
next radius misfit: 0.017877039143161154
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 384.57 s
```

Diagnostic objective rows all preserved the true target-2 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.882895e-04 | 1.000 | 1.728875e-02 |
| highband | 7.042113e-04 | 1.197 | 2.617388e-04 |
| late | 8.954015e-04 | 1.522 | 2.089346e-02 |
| late_high | 8.868481e-04 | 1.507 | 2.596133e-04 |
| veryhigh | 7.309414e-04 | 1.242 | 3.264007e-04 |
| early_high | 5.084462e-04 | 0.864 | 9.097209e-05 |

## Interpretation

Run 838 is a positive target-extension result. Seed13 target 2 remains
exact/moderate under the 5-source ringdown050 policy with a `5.882895e-04`
production margin, `8.829e-05` above cutoff.

It is stronger than seed13 target-2 9-source ringdown0459375 run 816 by
`3.491e-05`, and stronger than the seed13 target-2 9-source ringdown035
baseline run 807 by `2.370e-05`. This means the 5-source ringdown050 policy is
not limited to target 1.

The weakest diagnostic is early_high at `5.084e-04`, but it remains
truth-preserving and above cutoff.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.294672 and full 0-255 RGB-converted dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 8.0 mm
resources: GPU utilization held mostly about 87-88%; Python RSS stayed about 447-451 MiB; RAM stayed about 98 GiB available
elapsed: 384.57 s
```

## Next Decision

Run seed13 target 0 at ringdown050 with the same 5-source Tx/Rx=60 acquisition
and diagnostic objective suite. If target 0 also passes, summarize seed13
all-target ringdown050 under the 5-source policy.
