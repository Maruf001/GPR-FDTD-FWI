# Experiment 404: Seed55 Target-0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Run 870 tests target 0 at full ringdown050 on a fifth noise seed. This
directly probes whether seed21's target-0 near-miss is isolated or recurring.

## 870: Coordinate Optimizer Variable-Depth/Radius Seed55 Target-0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/870_coordinate_optimizer_variable_depth_radius_seed55_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed55 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed55_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 870 is exact and accepted:

```text
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.079048e-04
offset from cutoff: +7.905e-06
confidence label: moderate
fallback warning: none
elapsed: 579.40 s
```

Diagnostic objective rows all preserve the true target-0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.079048e-04 | above cutoff |
| highband | 6.733503e-04 | above cutoff |
| late | 3.985385e-04 | below cutoff |
| late_high | 4.961680e-04 | below cutoff |
| veryhigh | 6.257398e-04 | above cutoff |
| early_high | 5.631874e-04 | above cutoff |

## Interpretation

Seed55 target 0 passes full ringdown050, but with low reserve:

| Seed | Run | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 13 | 840 | 5.625753e-04 | +6.258e-05 | accepted |
| 89 | 842 | 5.460353e-04 | +4.604e-05 | accepted |
| 21 | 846 | 4.975041e-04 | -2.496e-06 | rejected |
| 34 | 859 | 5.310935e-04 | +3.109e-05 | accepted |
| 55 | 870 | 5.079048e-04 | +7.905e-06 | accepted |

Seed21 remains the only target-0 full-ringdown050 failure in the tested set,
but seed55's small reserve means the shallow-target policy should not be
described as wide-margin robust.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.258524 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row above the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target0 truth_radius_mm is 5.0 mm
source validation: all six diagnostic objectives preserve target0 truth geometry; 4/6 clear cutoff
resources: GPU utilization held around 90-91%; RAM stayed about 97-98 GiB available
elapsed: 579.40 s
```

## Next Decision

Run seed55 target 2 at 5 sources and full ringdown050 to determine whether
seed55 follows the seed13 target2 5-source pass pattern or the seed89/seed34
9-source rescue pattern.
