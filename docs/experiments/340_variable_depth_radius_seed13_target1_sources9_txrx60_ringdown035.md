# Experiment 340: Seed13 Target-1 Sources=9 Tx/Rx=60 Ringdown035

## Purpose

Run 806 continues the seed13 replication of the target-specific Tx/Rx=60
source-count policy. Run 805 passed target 0 at 8 sources; this run tests
whether target 1 remains exact/moderate at the 9-source policy row under the
same ringdown035, 10% noise, source-mismatch stress.

## 806: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-1 Sources=9 Tx/Rx=60 Ringdown035

Output:

```text
outputs/experiments/806_coordinate_optimizer_variable_depth_radius_seed13_target1_sources9_txrx60_ringdown035_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target1_sources9_txrx60_ringdown035_objectives
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
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.109178e-04
relative radius margin: 2.821805e-02
confidence label: moderate
best misfit: 0.01810606219354359
next radius misfit: 0.01861698004047896
competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 713.84 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.109178e-04 | 1.000 | 1.810606e-02 |
| highband | 6.185319e-04 | 1.211 | 2.735978e-04 |
| late | 7.218364e-04 | 1.413 | 2.098798e-02 |
| late_high | 8.485641e-04 | 1.661 | 3.294012e-04 |
| veryhigh | 6.299861e-04 | 1.233 | 3.469224e-04 |
| early_high | 4.387882e-04 | 0.859 | 8.627182e-05 |

Cross-seed target-1 comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| seed89 target 1, 9 sources, ringdown035 | 794 | 5.424900e-04 | 0.942 vs run 794 | moderate |
| seed21 target 1, 9 sources, ringdown035 | 803 | 5.683415e-04 | 0.899 vs run 803 | moderate |
| seed13 target 1, 9 sources, ringdown035 | 806 | 5.109178e-04 | 1.000 | moderate |

## Interpretation

Run 806 is a positive but weaker seed13 target-1 replication. The selected
geometry is exact and the base confidence label remains moderate, so seed13 has
now passed target 0 at 8 sources and target 1 at 9 sources. The target-1 margin
is lower than both comparable seed89 and seed21 rows, so the result should be
recorded as a pass with reduced margin rather than as a strengthened policy
row.

The diagnostic objectives strengthen the row except for `early_high`, and no
diagnostic variant changes the selected radius. That supports continuing the
seed13 replication to target 2 at 9 sources before making a three-seed policy
summary.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.259 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 90-91%; Python RSS stayed about 453-459 MiB; RAM stayed about 98-99 GiB available
elapsed: 713.84 s
```

## Next Decision

Complete seed13 replication with target 2 at 9 sources under the same Tx/Rx=60
ringdown035 stress. If target 2 remains exact/moderate, create a compact
three-seed target-specific 8/9/9 policy summary.

