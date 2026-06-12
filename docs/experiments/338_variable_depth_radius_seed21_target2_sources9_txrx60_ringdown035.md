# Experiment 338: Seed21 Target-2 Sources=9 Tx/Rx=60 Ringdown035

## Purpose

Run 804 completes the seed21 replication of the target-specific Tx/Rx=60
source-count policy. Runs 802 and 803 already confirmed seed21 target 0 at
8 sources and target 1 at 9 sources; this run tests target 2 at 9 sources.

## 804: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-2 Sources=9 Tx/Rx=60 Ringdown035

Output:

```text
outputs/experiments/804_coordinate_optimizer_variable_depth_radius_seed21_target2_sources9_txrx60_ringdown035_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target2_sources9_txrx60_ringdown035_objectives
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
target: 2
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.337948e-04
relative radius margin: 2.985908e-02
confidence label: moderate
best misfit: 0.017877133066408275
next radius misfit: 0.018410927839334644
competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 714.24 s
```

Seed21 policy comparison:

| Target | Source count | Run | Base margin | Confidence |
| ---: | ---: | ---: | ---: | --- |
| 0 | 8 | 802 | 5.444706e-04 | moderate |
| 1 | 9 | 803 | 5.683415e-04 | moderate |
| 2 | 9 | 804 | 5.337948e-04 | moderate |

## Interpretation

Run 804 is a positive completion of the seed21 target-specific policy
replication. Target 2 remains exact and moderate at 9 sources under Tx/Rx=60
ringdown035. The margin is weaker than the comparable seed89 target-2 rows, but
still above the moderate threshold.

Together, runs 802-804 show that the target-specific 8/9/9 source-count policy
transfers from seed89 to seed21 under the stronger ringdown035 stress:
target 0 at 8 sources is moderate, target 1 at 9 sources is moderate, and
target 2 at 9 sources is moderate. The weakest seed21 row is target 2 at
5.338e-04.

Late_high remains the strongest truth-preserving diagnostic for target 2, again
matching the seed89 pattern. The base objective is already moderate and remains
the production policy metric.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.269 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 8.0 mm
resources: GPU utilization held mostly about 90-91%; Python RSS stayed about 453-461 MiB; RAM stayed about 98-99 GiB available
elapsed: 714.24 s
```

## Next Decision

The seed21 8/9/9 replication is complete and positive. The next branch should
either replicate the same target-specific policy on seed13, or create one
compact summary/figure for the seed89-vs-seed21 target-specific policy before
starting a third seed.
