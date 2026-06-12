# Experiment 615: Seed7778742049 Target0 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Run the source-density bracket for seed7778742049 target0 after both the
8-source Tx/Rx=60 control and the 8-source Tx/Rx=52.5 acquisition probe were
exact but weak.

## 1081: Coordinate Optimizer Variable-Depth/Radius Seed7778742049 Target0 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1081_coordinate_optimizer_variable_depth_radius_seed7778742049_target0_sources9_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed7778742049:1.1,-50.0,1.1,0.10,7778742049,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed7778742049 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed7778742049_target0_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1081 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 5.583698e-04
offset from cutoff: +5.836979e-05
relative margin: 3.587279e-02
confidence label: moderate
fallback warning: none
best misfit: 1.556527e-02
next radius misfit: 1.612364e-02
elapsed: 715.4 s
```

Diagnostic objective margins:

```text
base       5.583698e-04  above cutoff
highband   7.519866e-04  above cutoff
late       4.117004e-04  weak, below cutoff
late_high  4.677905e-04  weak, below cutoff
veryhigh   8.057408e-04  above cutoff
early_high 6.558477e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

The 9-source Tx/Rx=60 source-density bracket rescues seed7778742049 target0.
It improves the base margin by about 9.51e-05 relative to run 1079 and by
about 1.15e-04 relative to the failed Tx/Rx=52.5 acquisition probe in run
1080. Late and late_high remain below cutoff, so carry the recurring target0
late-window caveat forward, but no 11-source escalation is justified because
base confidence is now accepted and every diagnostic objective ranks the true
geometry first.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.253557 and unique_colors=264
visual inspection: confidence figure is readable and shows one moderate target0 row above cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90-92%; host RAM stayed about 94-95 GiB available
```

## Next Decision

Continue the seed7778742049 branch with target2 at the standard 5-source
Tx/Rx=60 control.
