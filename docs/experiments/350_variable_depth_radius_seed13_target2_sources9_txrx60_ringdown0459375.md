# Experiment 350: Seed13 Target-2 Sources=9 Tx/Rx=60 Ringdown0459375

## Purpose

Run 816 moves the stronger-ringdown stress from the closed target-1 threshold
branch to seed13 target 2. It uses the highest passing target-1 stress level,
ringdown0459375, with the established target-specific policy of 9 sources and
Tx/Rx=60.

## 816: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-2 Sources=9 Tx/Rx=60 Ringdown0459375

Output:

```text
outputs/experiments/816_coordinate_optimizer_variable_depth_radius_seed13_target2_sources9_txrx60_ringdown0459375_objectives
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
  --target-indices 2 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target2_sources9_txrx60_ringdown0459375_objectives
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
target: 2
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.533762e-04
relative radius margin: 3.358190e-02
confidence label: moderate
fallback warning: none
best misfit: 0.0164784067129565
next radius misfit: 0.01703178292805864
competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 708.09 s
```

Diagnostic objective rows all preserved the true target-2 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.533762e-04 | 1.000 | 1.647841e-02 |
| highband | 6.912984e-04 | 1.249 | 2.805839e-04 |
| late | 8.336375e-04 | 1.506 | 1.965674e-02 |
| late_high | 9.298595e-04 | 1.680 | 3.190399e-04 |
| veryhigh | 7.398640e-04 | 1.337 | 3.271457e-04 |
| early_high | 4.766756e-04 | 0.861 | 9.350001e-05 |

## Interpretation

Target 2 remains exact/moderate at the highest passing target-1 stress level.
The production base margin is `5.338e-05` above the cutoff and only slightly
reduced relative to the seed13 target-2 ringdown035 baseline from run 807
(0.980x). This makes target 2 stronger than target 1 under the same
ringdown0459375 stress: run 816 is about 1.105x the base margin of run 814.

The early-high diagnostic margin is below `5e-04`, but it remains
truth-preserving. Therefore the run does not indicate a target-2 geometry
failure; it indicates that early-window high-band evidence is less separable
for the larger/deeper target under this source stress.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.266 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 8.0 mm
resources: GPU utilization held mostly about 91%; Python RSS stayed about 453-459 MiB; RAM stayed about 98-99 GiB available
elapsed: 708.09 s
```

## Next Decision

Complete the ringdown0459375 all-target policy check with seed13 target 0 at
8 sources and Tx/Rx=60.

