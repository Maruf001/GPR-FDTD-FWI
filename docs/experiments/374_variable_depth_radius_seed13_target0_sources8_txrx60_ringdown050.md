# Experiment 374: Seed13 Target-0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Run 840 tests whether restoring the old target-0 source density strengthens
the boundary-level 5-source target-0 row from run 839 while keeping the
ringdown050 stress and Tx/Rx=60 aperture.

## 840: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/840_coordinate_optimizer_variable_depth_radius_seed13_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target0_sources8_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed13
target: 0
sources: 8
scan x positions: [50, 106, 162, 218, 274, 330, 386, 450] mm
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.625753e-04
relative radius margin: 3.541869e-02
confidence label: moderate
fallback warning: none
best misfit: 0.015883571436461096
next radius misfit: 0.01644614672520095
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 592.64 s
```

Diagnostic objective rows all preserved the true target-0 geometry:

| Objective | Margin | Ratio vs run 839 | Status |
| --- | ---: | ---: | --- |
| base | 5.625753e-04 | 1.107 | above cutoff |
| highband | 7.353899e-04 | 1.149 | above cutoff |
| late | 4.583314e-04 | 1.024 | below cutoff, truth-preserving |
| late_high | 5.369872e-04 | 1.095 | above cutoff |
| veryhigh | 6.669091e-04 | 0.984 | above cutoff |
| early_high | 5.906518e-04 | 1.112 | above cutoff |

## Interpretation

Run 840 shows that the run 839 target-0 weakness was mostly an acquisition
issue. Restoring 8 sources improves the production margin by `5.444e-05`
relative to the 5-source target-0 run 839, making target 0 stronger than
seed13 target 1 under the ringdown050 5-source policy from run 834. It is
still `1.787e-05` below the lower-stress 8-source target-0 run 817 and
`2.571e-05` below seed13 target 2 at ringdown050 from run 838.

The seed13 ringdown050 policy should therefore become target-specific:
`8/5/5` sources for targets `0/1/2`, using runs 840, 834, and 838. The only
remaining diagnostic fragility in this row is the late objective at
`4.583e-04`; it preserves the true geometry but stays below the 5e-04 cutoff.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.283745 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held around 90-91%; Python RSS stayed about 454-462 MiB; RAM stayed about 98 GiB available
elapsed: 592.64 s
```

## Next Decision

Create a seed13 all-target ringdown050 target-specific summary from runs 840,
834, and 838. If that summary confirms the policy is coherent, transfer the
`8/5/5` source-count policy to seed89 at ringdown050.
