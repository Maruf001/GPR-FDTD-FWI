# Experiment 339: Seed13 Target-0 Sources=8 Tx/Rx=60 Ringdown035

## Purpose

Run 805 begins the seed13 replication of the target-specific Tx/Rx=60
source-count policy. Seed89 and seed21 both kept target 0 exact/moderate with
the 8-source aperture under ringdown035; this run tests the same row on seed13.

## 805: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-0 Sources=8 Tx/Rx=60 Ringdown035

Output:

```text
outputs/experiments/805_coordinate_optimizer_variable_depth_radius_seed13_target0_sources8_txrx60_ringdown035_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target0_sources8_txrx60_ringdown035_objectives
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
target: 0
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 6.074783e-04
relative radius margin: 3.201822e-02
confidence label: moderate
best misfit: 0.018972897547170332
next radius misfit: 0.019580375887313654
competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 621.34 s
```

Cross-seed comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| seed89 target 0, 8 sources, ringdown025 | 789 | 5.899921e-04 | 1.030 vs run 789 | moderate |
| seed89 target 0, 8 sources, ringdown035 | 795 | 5.954728e-04 | 1.020 vs run 795 | moderate |
| seed21 target 0, 8 sources, ringdown035 | 802 | 5.444706e-04 | 1.116 vs run 802 | moderate |
| seed13 target 0, 8 sources, ringdown035 | 805 | 6.074783e-04 | 1.000 | moderate |

## Interpretation

Run 805 is a positive seed13 target-0 replication. The 8-source Tx/Rx=60
ringdown035 row remains exact and moderate, and it is stronger than both the
seed89 and seed21 target-0 8-source ringdown035 rows. Seed13 therefore passes
the first row of the target-specific 8/9/9 policy.

The target-0 diagnostic pattern remains consistent: highband and veryhigh
strengthen the base margin, while late-window objectives weaken the row. The
base objective is already moderate and remains the production policy metric.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.302 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held mostly about 90-91%; Python RSS stayed about 452-458 MiB; RAM stayed about 98 GiB available
elapsed: 621.34 s
```

## Next Decision

Continue seed13 replication with target 1 at 9 sources under the same Tx/Rx=60
ringdown035 stress.
