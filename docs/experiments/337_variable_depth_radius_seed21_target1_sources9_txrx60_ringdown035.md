# Experiment 337: Seed21 Target-1 Sources=9 Tx/Rx=60 Ringdown035

## Purpose

Run 803 continues the seed21 replication of the target-specific Tx/Rx=60
source-count policy. After run 802 confirmed target 0 at 8 sources, this run
tests target 1 at the 9-source setting that was best for seed89 under
ringdown035.

## 803: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-1 Sources=9 Tx/Rx=60 Ringdown035

Output:

```text
outputs/experiments/803_coordinate_optimizer_variable_depth_radius_seed21_target1_sources9_txrx60_ringdown035_objectives
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
  --replication-cases source_mismatch_ringdown035_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.35,180.0,0.8 \
  --update-case-label source_mismatch_ringdown035_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target1_sources9_txrx60_ringdown035_objectives
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
case: source_mismatch_ringdown035_noise10_seed21
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.683415e-04
relative radius margin: 3.179154e-02
confidence label: moderate
best misfit: 0.017877133066408275
next radius misfit: 0.0184454746152229
competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 725.00 s
```

Cross-seed comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| seed89 target 1, 9 sources, ringdown025 | 786 | 5.181917e-04 | 1.097 vs run 786 | moderate |
| seed89 target 1, 9 sources, ringdown035 | 794 | 5.424900e-04 | 1.048 vs run 794 | moderate |
| seed89 target 1, union15, ringdown035 | 801 | 5.560820e-04 | 1.022 vs run 801 | moderate |
| seed21 target 1, 9 sources, ringdown035 | 803 | 5.683415e-04 | 1.000 | moderate |

## Interpretation

Run 803 is a positive seed21 target-1 replication. The 9-source Tx/Rx=60
ringdown035 row stays exact and moderate, and it is slightly stronger than the
comparable seed89 target-1 row from run 794. This means seed21 has now passed
the first two target-specific policy rows: target 0 at 8 sources and target 1
at 9 sources.

Late_high remains the strongest truth-preserving diagnostic for the center
target, matching the seed89 pattern. The base objective remains the production
policy metric and is already moderate.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.286 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 89-91%; Python RSS stayed about 453-461 MiB; RAM stayed about 98-99 GiB available
elapsed: 725.00 s
```

## Next Decision

Complete the seed21 target-specific policy replication with target 2 at
9 sources under the same Tx/Rx=60 ringdown035 stress.
