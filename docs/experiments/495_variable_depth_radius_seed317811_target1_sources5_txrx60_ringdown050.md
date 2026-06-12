# Experiment 495: Seed317811 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 961 tests seed317811 target1 at the standard 5-source control after target2
accepted only by a 9-source rescue.

## 961: Coordinate Optimizer Variable-Depth/Radius Seed317811 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/961_coordinate_optimizer_variable_depth_radius_seed317811_target1_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed317811:1.1,-50.0,1.1,0.10,317811,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed317811 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed317811_target1_sources5_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed317811
target: 1
sources: 5
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 6.017320e-04
offset from cutoff: +1.017320e-04
relative radius margin: 3.609362e-02
confidence label: moderate
fallback warning: none
best misfit: 0.016671422191882383
next radius misfit: 0.01727315419159255
listed competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: about 400.2 s
```

Diagnostic objective rows all preserve the true target1 geometry and all clear
the cutoff:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 6.017320e-04 | above cutoff |
| highband | 7.778784e-04 | above cutoff |
| late | 8.534321e-04 | above cutoff |
| late_high | 9.351331e-04 | above cutoff |
| veryhigh | 7.038860e-04 | above cutoff |
| early_high | 5.662074e-04 | above cutoff |

## Interpretation

Run 961 is accepted as the seed317811 target1 5-source control. It is cleaner
than the branch's target0/target2 rows because all diagnostic variants clear
the confidence cutoff. Close the seed317811 branch with a rescue summary.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.284638 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate row above the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target1 truth_radius_mm is 6.0 mm
resources: 5-source GPU checks were about 87-88% utilization with about 96-97 GiB RAM available
```

## Next Decision

Create the seed317811 target-specific rescue summary before starting
seed514229.
