# Experiment 1007: Seed3524578 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Complete the seed3524578 target-specific branch by testing target1 at the
standard 5-source Tx/Rx=60 control.

## Command

```bash
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
  --replication-cases source_mismatch_ringdown050_noise10_seed3524578:1.1,-50.0,1.1,0.10,3524578,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed3524578 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed3524578_target1_sources5_txrx60_ringdown050_objectives
```

## Result

The final recovered coordinate state is exact:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

Base confidence:

```text
tx_rx_offset_mm: 60.0
target: 1
sources: 5
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.523984e-04
offset from cutoff: +5.239845e-05
relative margin: 3.246974e-02
confidence label: moderate
fallback warning: none
best misfit: 0.017012716975895435
next radius misfit: 0.017565115424529414
elapsed: 364.4 s
```

Diagnostic objective margins:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.523984e-04 | above cutoff |
| highband | 7.098408e-04 | above cutoff |
| late | 8.427641e-04 | above cutoff |
| late_high | 9.006698e-04 | above cutoff |
| veryhigh | 6.802116e-04 | above cutoff |
| early_high | 5.254032e-04 | above cutoff |

All six objective variants rank the true target1 geometry first.

## Interpretation

Target1 is clean at 5 sources and Tx/Rx=60. Together with runs 1004 and 1006,
this completes seed3524578 without any additional source-density rescue. The
branch-level caveat remains target2 early_high from run 1006.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.262412 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target1 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 89%; nvidia-smi process memory was about 252 MiB
```

## Next Decision

Run seed5702887 target0 at 8 sources and Tx/Rx=60. That run is experiment
1008.
