# Experiment 559: Seed14930352 Target0 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Run the first source-density rescue bracket for seed14930352 target0 after
both the 8-source Tx/Rx=60 control and the 8-source Tx/Rx=52.5 acquisition
probe were exact but weak.

## 1025: Coordinate Optimizer Variable-Depth/Radius Seed14930352 Target0 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1025_coordinate_optimizer_variable_depth_radius_seed14930352_target0_sources9_txrx60_ringdown050_objectives
```

Command:

```bash
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
  --target-indices 0 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown050_noise10_seed14930352:1.1,-50.0,1.1,0.10,14930352,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed14930352 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed14930352_target0_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1025 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 4.784595e-04
offset from cutoff: -2.154054e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 657.9 s
```

Diagnostic objective margins:

```text
base       4.784595e-04  below cutoff by 2.154054e-05
highband   6.805538e-04  above cutoff
late       3.295757e-04  below cutoff by 1.704243e-04
late_high  4.128739e-04  below cutoff by 8.712613e-05
veryhigh   7.353566e-04  above cutoff
early_high 6.147386e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

The 9-source bracket does not rescue seed14930352 target0. It is exact and
truth-ranked, but base confidence is weaker than both 8-source rows. This does
not yet close the rescue branch because seed1346269 target0 showed the same
qualitative pattern: 8 and 9 sources were weak, then 11 sources accepted.

Run one 11-source Tx/Rx=60 escalation. If that also remains weak, the branch
should treat seed14930352 target0 as unresolved under the tested mechanisms
before moving on to target2.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.226466 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target0 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 92%; nvidia-smi process memory was about 307 MiB
```

## Next Decision

Run seed14930352 target0 with 11 sources and Tx/Rx=60. That escalation is
experiment 1026.
