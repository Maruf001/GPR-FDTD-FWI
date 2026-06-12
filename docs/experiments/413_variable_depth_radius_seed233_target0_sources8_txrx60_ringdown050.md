# Experiment 413: Seed233 Target-0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Run 878 extends the full-ringdown050 target-0 lower-tail replication to the
next Fibonacci noise seed after seed144.

## 878: Coordinate Optimizer Variable-Depth/Radius Seed233 Target-0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/878_coordinate_optimizer_variable_depth_radius_seed233_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed233:1.1,-50.0,1.1,0.10,233,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed233 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed233_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 878 is exact and accepted:

```text
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.434236e-04
offset from cutoff: +4.342e-05
confidence label: moderate
fallback warning: none
elapsed: 557.96 s
```

Diagnostic objective rows all preserve the true target-0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.434236e-04 | above cutoff |
| highband | 7.098527e-04 | above cutoff |
| late | 3.779758e-04 | below cutoff |
| late_high | 4.571601e-04 | below cutoff |
| veryhigh | 6.584969e-04 | above cutoff |
| early_high | 6.058978e-04 | above cutoff |

## Interpretation

Seed233 is another target-0 full-ringdown050 pass:

| Seed | Run | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 13 | 840 | 5.625753e-04 | +6.258e-05 | accepted |
| 89 | 842 | 5.460353e-04 | +4.604e-05 | accepted |
| 21 | 846 | 4.975041e-04 | -2.496e-06 | rejected |
| 34 | 859 | 5.310935e-04 | +3.109e-05 | accepted |
| 55 | 870 | 5.079048e-04 | +7.905e-06 | accepted |
| 144 | 873 | 6.144391e-04 | +1.144e-04 | accepted |
| 233 | 878 | 5.434236e-04 | +4.342e-05 | accepted |

Seed233 does not repeat the seed21 target-0 failure. The target-0 lower tail is
still important, but this row shifts the evidence toward seed21 being an
outlier rather than a common full-ringdown050 target-0 failure mode.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.270394 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row above the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target0 truth_radius_mm is 5.0 mm
source validation: all six diagnostic objectives preserve target0 truth geometry; 4/6 clear cutoff
resources: GPU utilization held around 91-92%; RAM stayed around 97-98 GiB available
elapsed: 557.96 s
```

## Next Decision

Run seed233 target 2 at 5 sources and full ringdown050.
