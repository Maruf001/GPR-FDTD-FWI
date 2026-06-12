# Experiment 395: Seed34 Target-2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 861 tests seed34 target 2 under the 5-source ringdown050 policy after
seed34 target 0 and target 1 passed in runs 859 and 860.

## 861: Coordinate Optimizer Variable-Depth/Radius Seed34 Target-2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/861_coordinate_optimizer_variable_depth_radius_seed34_target2_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed34:1.1,-50.0,1.1,0.10,34,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed34 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed34_target2_sources5_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed34
target: 2
sources: 5
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 4.575126e-04
relative radius margin: 2.691283e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.016999792690426792
next radius misfit: 0.017457305279057634
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 384.28 s
```

Diagnostic objective rows all preserved the true target-2 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.575126e-04 | below cutoff, weak |
| highband | 5.244607e-04 | above cutoff |
| late | 6.685927e-04 | above cutoff |
| late_high | 7.097801e-04 | above cutoff |
| veryhigh | 5.776986e-04 | above cutoff |
| early_high | 3.690947e-04 | below cutoff, truth-preserving |

## Interpretation

Run 861 is exact but weak. It rejects the 5-source seed34 target-2 policy and
matches the seed89 pattern more than the seed13 pass.

Target-2 ringdown050 context:

| Run | Noise seed | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | --- |
| 838 | 13 | 5 | 5.882895e-04 | +8.829e-05 | accepted |
| 843 | 89 | 5 | 4.414917e-04 | -5.851e-05 | rejected |
| 844 | 89 | 9 | 5.821195e-04 | +8.212e-05 | accepted rescue |
| 861 | 34 | 5 | 4.575126e-04 | -4.249e-05 | rejected |

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.234286 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one weak row below the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 8.0 mm
resources: GPU utilization held around 88%; RAM stayed about 97-98 GiB available
elapsed: 384.28 s
```

## Next Decision

Run the seed34 target-2 9-source rescue at ringdown050 and Tx/Rx=60.
