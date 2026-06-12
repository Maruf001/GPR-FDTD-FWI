# Experiment 336: Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown035

## Purpose

Run 802 begins the cross-seed replication of the target-specific Tx/Rx=60
source-count policy. After seed89 showed target 0 prefers the 8-source aperture
under ringdown035, this run repeats that target-0 setting with seed21.

## 802: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown035

Output:

```text
outputs/experiments/802_coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown035_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown035_objectives
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
target: 0
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.444706e-04
relative radius margin: 2.911167e-02
confidence label: moderate
best misfit: 0.018702830286537325
next radius misfit: 0.01924730085075955
competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 617.66 s
```

Cross-seed comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| seed89 target 0, 8 sources, ringdown025 | 789 | 5.899921e-04 | 0.923 vs run 789 | moderate |
| seed89 target 0, 8 sources, ringdown035 | 795 | 5.954728e-04 | 0.914 vs run 795 | moderate |
| seed21 target 0, 8 sources, ringdown035 | 802 | 5.444706e-04 | 1.000 | moderate |
| seed89 target 0, union15, ringdown035 | 801 | 4.521727e-04 | 1.204 vs run 801 | weak |

## Interpretation

Run 802 is a positive first cross-seed check for the target-specific Tx/Rx=60
source-count policy. The target-0 8-source row remains exact and moderate under
seed21 ringdown035. The margin is about 0.914x the comparable seed89
ringdown035 row from run 795, so seed21 is weaker than seed89 for this row but
still above the moderate threshold.

This result supports continuing the seed21 target-specific policy replication
with target 1 at 9 sources, then target 2 at 9 sources. It also reinforces the
run-801 conclusion: target 0 is better served by the 8-source aperture than by
the dense union15 aperture.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.275 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held mostly about 90%; Python RSS stayed about 451-460 MiB; RAM stayed about 98-99 GiB available
elapsed: 617.66 s
```

## Next Decision

Continue seed21 replication of the target-specific policy with target 1 at
9 sources under the same Tx/Rx=60 ringdown035 stress. If target 1 remains
moderate, run target 2 at 9 sources next and then summarize the seed21
target-specific 8/9/9 result.
