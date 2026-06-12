# Experiment 351: Seed13 Target-0 Sources=8 Tx/Rx=60 Ringdown0459375

## Purpose

Run 817 completes the seed13 all-target check at the highest passing target-1
stress level. It tests target 0 with the established target-specific policy of
8 sources and Tx/Rx=60 at ringdown0459375.

## 817: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-0 Sources=8 Tx/Rx=60 Ringdown0459375

Output:

```text
outputs/experiments/817_coordinate_optimizer_variable_depth_radius_seed13_target0_sources8_txrx60_ringdown0459375_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 8 \
  --tx-rx-offset-mm 60 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 150,250,350 \
  --initial-z-values-mm 80,100,120 \
  --initial-radius-values-mm 5,6,8 \
  --target-indices 0 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown0459375_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.459375,180.0,0.8 \
  --update-case-label source_mismatch_ringdown0459375_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target0_sources8_txrx60_ringdown0459375_objectives
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
case: source_mismatch_ringdown0459375_noise10_seed13
target: 0
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.804441e-04
relative radius margin: 3.466838e-02
confidence label: moderate
fallback warning: none
best misfit: 0.016742751253594507
next radius misfit: 0.017323195317587668
competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 609.18 s
```

Diagnostic objective rows all preserved the true target-0 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.804441e-04 | 1.000 | 1.674275e-02 |
| highband | 7.336722e-04 | 1.264 | 2.220947e-04 |
| late | 4.473734e-04 | 0.771 | 2.017569e-02 |
| late_high | 5.241691e-04 | 0.903 | 2.375712e-04 |
| veryhigh | 6.629822e-04 | 1.142 | 2.490280e-04 |
| early_high | 5.739683e-04 | 0.989 | 7.673057e-05 |

## Interpretation

Target 0 remains exact/moderate at the highest passing target-1 stress level.
The production base margin is `8.044e-05` above the cutoff, about 0.955x the
seed13 target-0 ringdown035 baseline from run 805, and stronger than the
target-1 and target-2 ringdown0459375 rows.

The late diagnostic margin is below `5e-04`, but it remains truth-preserving.
Therefore the target-0 stress result supports the target-specific 8/9/9 policy
at ringdown0459375 while identifying late-window evidence as the weakest
diagnostic view for the shallow target.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.278 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held mostly about 90-91%; Python RSS stayed about 451-460 MiB; RAM stayed about 98-99 GiB available
elapsed: 609.18 s
```

## Next Decision

Create an all-target ringdown0459375 policy summary for seed13 runs 817, 814,
and 816. The expected conclusion is that the 8/9/9 policy remains exact and
production-moderate for all targets at the highest passing target-1 stress
level.

