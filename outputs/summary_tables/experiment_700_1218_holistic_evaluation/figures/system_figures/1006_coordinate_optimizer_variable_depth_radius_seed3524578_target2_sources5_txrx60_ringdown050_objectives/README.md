# Experiment 1006: Seed3524578 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Continue the seed3524578 branch with the original target2 control: 5 sources
and Tx/Rx=60 under the source_mismatch_ringdown050_noise10_seed3524578 case.

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
  --target-indices 2 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed3524578_target2_sources5_txrx60_ringdown050_objectives
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
target: 2
sources: 5
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.691824e-04
offset from cutoff: +6.918241e-05
relative margin: 3.345629e-02
confidence label: moderate
fallback warning: none
best misfit: 0.017012716975895435
next radius misfit: 0.017581899387696626
elapsed: 367.1 s
```

Diagnostic objective margins:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.691824e-04 | above cutoff |
| highband | 6.895847e-04 | above cutoff |
| late | 8.693891e-04 | above cutoff |
| late_high | 8.982087e-04 | above cutoff |
| veryhigh | 6.876029e-04 | above cutoff |
| early_high | 4.897265e-04 | below cutoff by 1.027346e-05 |

All six objective variants rank the true target2 geometry first.

## Interpretation

The seed3524578 target2 5-source Tx/Rx=60 control is base-accepted and
truth-preserving. It is not fully clean because early_high is fractionally
below the 5.0e-4 cutoff. Continue to target1 before spending GPU time on a
target2 rescue, and keep the early_high caveat for the branch summary.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.269636 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target2 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88-89%; nvidia-smi process memory was about 252 MiB
```

## Next Decision

Run seed3524578 target1 at 5 sources and Tx/Rx=60. That run is experiment
1007.
