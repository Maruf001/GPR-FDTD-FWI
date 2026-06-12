# Experiment 628: Seed20365011074 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Complete the seed20365011074 branch after target0 passed, target2 stayed
truth-preserving but unresolved under the simple source-density ladder, and the
next needed evidence was whether target1 also shows a low-margin pattern. This
run checks target1 with the standard 5-source Tx/Rx=60 control.

## 1094: Coordinate Optimizer Variable-Depth/Radius Seed20365011074 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1094_coordinate_optimizer_variable_depth_radius_seed20365011074_target1_sources5_txrx60_ringdown050_objectives
```

Command:

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
  --run-name coordinate_optimizer_variable_depth_radius_seed20365011074_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1094 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.319986e-04
offset from cutoff: +3.199862e-05
relative margin: 3.187056e-02
confidence label: moderate
fallback warning: none
best misfit: 1.669248e-02
next radius misfit: 1.722448e-02
elapsed: 394.2 s
```

Diagnostic objective margins:

```text
base       5.319986e-04  above cutoff
highband   6.829855e-04  above cutoff
late       8.085120e-04  above cutoff
late_high  9.204138e-04  above cutoff
veryhigh   6.546502e-04  above cutoff
early_high 5.088517e-04  above cutoff
```

All six objective variants rank the true target1 geometry first.

## Interpretation

Seed20365011074 is target2-limited under the current full-ringdown050 policy,
not broadly low-margin across all targets. Target0 passed the standard
8-source control with a late-window caveat, target1 passes the standard
5-source control cleanly, and target2 remains truth-preserving but technically
unaccepted after 5-, 7-, 9-, and 11-source checks. The best target2 row is the
9-source near miss from run 1092; keep that unresolved caveat visible rather
than silently promoting it.

This closes the seed20365011074 branch without a separate numbered summary
output folder. Continue the Fibonacci replication chain with seed32951280099
target0 after confirming the seed is accepted by the active NumPy random
generator.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.239174 and unique_colors=264
visual inspection: confidence figure is readable and shows one moderate target1 row above cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 86-89%; host RAM stayed about 94-95 GiB available
```

## Next Decision

Validate seed32951280099 and then run target0 with the standard 8-source
Tx/Rx=60 control.
