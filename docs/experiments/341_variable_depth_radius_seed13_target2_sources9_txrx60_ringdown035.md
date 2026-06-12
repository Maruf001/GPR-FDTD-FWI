# Experiment 341: Seed13 Target-2 Sources=9 Tx/Rx=60 Ringdown035

## Purpose

Run 807 completes the seed13 replication of the target-specific Tx/Rx=60
source-count policy. Runs 805 and 806 passed target 0 at 8 sources and target 1
at 9 sources; this run tests whether target 2 remains exact/moderate at the
9-source policy row under the same ringdown035, 10% noise, source-mismatch
stress.

## 807: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-2 Sources=9 Tx/Rx=60 Ringdown035

Output:

```text
outputs/experiments/807_coordinate_optimizer_variable_depth_radius_seed13_target2_sources9_txrx60_ringdown035_objectives
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
  --replication-cases source_mismatch_ringdown035_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.35,180.0,0.8 \
  --update-case-label source_mismatch_ringdown035_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target2_sources9_txrx60_ringdown035_objectives
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
case: source_mismatch_ringdown035_noise10_seed13
target: 2
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.645862e-04
relative radius margin: 3.118216e-02
confidence label: moderate
best misfit: 0.01810606219354359
next radius misfit: 0.01867064837726647
competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 717.58 s
```

Diagnostic objective rows all preserved the true target-2 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.645862e-04 | 1.000 | 1.810606e-02 |
| highband | 6.380133e-04 | 1.130 | 2.735978e-04 |
| late | 8.231840e-04 | 1.458 | 2.098798e-02 |
| late_high | 8.959702e-04 | 1.587 | 3.294012e-04 |
| veryhigh | 7.185914e-04 | 1.273 | 3.469224e-04 |
| early_high | 4.152391e-04 | 0.735 | 8.627182e-05 |

Cross-seed target-2 comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| seed89 target 2, 9 sources, ringdown035 | 796 | 6.058657e-04 | 0.932 vs run 796 | moderate |
| seed21 target 2, 9 sources, ringdown035 | 804 | 5.337948e-04 | 1.058 vs run 804 | moderate |
| seed13 target 2, 9 sources, ringdown035 | 807 | 5.645862e-04 | 1.000 | moderate |

## Interpretation

Run 807 is a positive seed13 target-2 replication. The selected geometry is
exact and the base confidence label remains moderate. Seed13 is weaker than
seed89 on target 2 but stronger than seed21, placing it between the previous
two seeds.

Together, runs 805-807 complete a three-row seed13 replication of the
target-specific Tx/Rx=60 source-count policy: target 0 at 8 sources, target 1
at 9 sources, and target 2 at 9 sources all remain exact/moderate under
ringdown035 source mismatch. This justifies a compact three-seed policy summary
before launching a new acquisition branch.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.284 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 8.0 mm
resources: GPU utilization held mostly about 90-91%; Python RSS stayed about 453-461 MiB; RAM stayed about 98-99 GiB available
elapsed: 717.58 s
```

## Next Decision

Create a compact three-seed target-specific 8/9/9 policy summary from runs
795-796, 802-807, and the target-1 seed89 row in run 794. The summary should
include a real comparison table and figure, not a short administrative-only
tracker.

