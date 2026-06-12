# Experiment 516: Seed2178309 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 982 tests seed2178309 target1 at the standard 5-source control after
target0 and target2 were accepted with diagnostic caveats.

## 982: Coordinate Optimizer Variable-Depth/Radius Seed2178309 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/982_coordinate_optimizer_variable_depth_radius_seed2178309_target1_sources5_txrx60_ringdown050_objectives
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
  --target-indices 1 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown050_noise10_seed2178309:1.1,-50.0,1.1,0.10,2178309,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed2178309 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed2178309_target1_sources5_txrx60_ringdown050_objectives
```

## Results

The final recovered coordinate state is exact, but the base confidence margin
is weak:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

Base confidence row:

```text
case: source_mismatch_ringdown050_noise10_seed2178309
target: 1
sources: 5
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 4.821346e-04
offset from cutoff: -1.786535e-05
relative radius margin: 2.827483e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.017051728526273475
next radius misfit: 0.017533863173256
listed competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: about 389.5 s
```

Diagnostic objective rows preserve the true target1 geometry, but base and
early_high fail cutoff:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.821346e-04 | below cutoff |
| highband | 6.104248e-04 | above cutoff |
| late | 7.771451e-04 | above cutoff |
| late_high | 8.359646e-04 | above cutoff |
| veryhigh | 5.628775e-04 | above cutoff |
| early_high | 4.647245e-04 | below cutoff |

## Interpretation

Run 982 is exact but rejected as a weak 5-source target1 control. Because the
geometry is truth-preserving, this is a confidence/reserve failure rather than
a localization failure. Escalate to a 9-source target1 rescue.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.230895 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak row below the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target1 truth_radius_mm is 6.0 mm
resources: 5-source GPU checks were about 87% utilization during this branch
```

## Next Decision

Run the seed2178309 target1 9-source rescue. That run is underway as
experiment 983.
