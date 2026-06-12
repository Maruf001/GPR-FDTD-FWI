# Experiment 625: Seed20365011074 Target2 Sources=7 Tx/Rx=60 Ringdown050

## Purpose

Follow up the weak seed20365011074 target2 5-source control. Run 1090 recovered
the exact target2 geometry, but the base margin was just below the confidence
cutoff and early_high was also weak. This run tests whether a 7-source Tx/Rx=60
source-density bracket strengthens the same target2 geometry.

## 1091: Coordinate Optimizer Variable-Depth/Radius Seed20365011074 Target2 Sources=7 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1091_coordinate_optimizer_variable_depth_radius_seed20365011074_target2_sources7_txrx60_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 7 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed20365011074:1.1,-50.0,1.1,0.10,20365011074,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed20365011074 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed20365011074_target2_sources7_txrx60_ringdown050_objectives
```

## Results

Run 1091 is exact but remains weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 7
tx_rx_offset_mm: 60.0
absolute radius margin: 4.743122e-04
offset from cutoff: -2.568781e-05
relative margin: 3.238666e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.464530e-02
next radius misfit: 1.511961e-02
elapsed: 538.2 s
```

Diagnostic objective margins:

```text
base       4.743122e-04  weak, below cutoff
highband   6.109779e-04  above cutoff
late       6.972120e-04  above cutoff
late_high  7.680690e-04  above cutoff
veryhigh   6.535169e-04  above cutoff
early_high 4.035822e-04  weak, below cutoff
```

All six objective variants rank the true target2 geometry first.

## Interpretation

The 7-source source-density bracket does not rescue target2. It keeps the
geometry exact, but the base margin worsens from `4.964072e-04` in the
5-source control to `4.743122e-04`, and early_high remains weak. Because this
matches the earlier weak-target2 pattern where a 7-source bracket was
insufficient, the justified next step is the 9-source Tx/Rx=60 escalation. Do
not move to target1 yet.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.215746 and unique_colors=264
visual inspection: confidence figure is readable and shows one weak target2 row below cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=7; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 89-90%; host RAM stayed about 94-95 GiB available
```

## Next Decision

Run seed20365011074 target2 with a 9-source Tx/Rx=60 source-density escalation.
