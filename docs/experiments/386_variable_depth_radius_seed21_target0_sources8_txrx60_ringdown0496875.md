# Experiment 386: Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown0496875

## Purpose

Run 852 refines the seed21 target-0 stress threshold between the accepted
ringdown049375 row from run 849 and the rejected ringdown050 row from run 846.

## 852: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown0496875

Output:

```text
outputs/experiments/852_coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown0496875_objectives
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
  --replication-cases source_mismatch_ringdown0496875_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.496875,180.0,0.8 \
  --update-case-label source_mismatch_ringdown0496875_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown0496875_objectives
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
case: source_mismatch_ringdown0496875_noise10_seed21
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 4.989535e-04
relative radius margin: 3.172563e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.015727130437018018
next radius misfit: 0.016226083935724826
elapsed: 602.0 s
```

Diagnostic objective rows all preserved the true target-0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.989535e-04 | below cutoff, weak |
| highband | 6.452596e-04 | above cutoff |
| late | 3.294412e-04 | below cutoff, truth-preserving |
| late_high | 4.128190e-04 | below cutoff, truth-preserving |
| veryhigh | 6.088103e-04 | above cutoff |
| early_high | 5.512056e-04 | above cutoff |

## Interpretation

Run 852 is an exact but weak near-miss and is rejected as a production policy
row. It is `1.0465e-06` below cutoff, `1.436e-06` weaker than accepted
ringdown049375 run 849, and `1.449e-06` stronger than rejected ringdown050
run 846.

The seed21 target-0 stress threshold is now tightly bracketed between
ringdown049375 and ringdown0496875. Ringdown049375 remains the highest
accepted seed21 target-0 point under the current 8-source Tx/Rx=60 policy.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.242508 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one weak row
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held around 90-91%; RAM stayed about 98 GiB available
elapsed: 602.0 s
```

## Next Decision

Run seed21 target 0 at ringdown04953125 with the same 8-source Tx/Rx=60
configuration. That midpoint is the correct next bracket because the upper
half already failed at ringdown0496875.
