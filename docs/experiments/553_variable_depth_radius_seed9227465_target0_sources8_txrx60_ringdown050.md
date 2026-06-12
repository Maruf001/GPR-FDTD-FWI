# Experiment 553: Seed9227465 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Start the seed9227465 Fibonacci replication branch with the same target0
control used for the recent variable-depth/radius multi-rebar policy checks:
8 sources, Tx/Rx=60, source mismatch, 10% noise, and ringdown scale 0.5.

## 1019: Coordinate Optimizer Variable-Depth/Radius Seed9227465 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1019_coordinate_optimizer_variable_depth_radius_seed9227465_target0_sources8_txrx60_ringdown050_objectives
```

Command:

```bash
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
  --replication-cases source_mismatch_ringdown050_noise10_seed9227465:1.1,-50.0,1.1,0.10,9227465,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed9227465 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed9227465_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1019 is exact and base-accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.252030e-04
offset from cutoff: +2.520298e-05
confidence label: moderate
fallback warning: none
elapsed: 562.7 s
```

Diagnostic objective margins:

```text
base       5.252030e-04  above cutoff
highband   6.804875e-04  above cutoff
late       4.390867e-04  below cutoff by 6.091330e-05
late_high  4.894696e-04  below cutoff by 1.053035e-05
veryhigh   6.270358e-04  above cutoff
early_high 5.602431e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

The seed9227465 target0 control is accepted at the original 8-source
Tx/Rx=60 setting. This differs from seed5702887 target0, which needed a lower
Tx/Rx bracket for a stronger base margin, but it still follows the broader
target0 pattern: late-window objectives can be weaker even when the true
geometry is rank 1. Carry the late/late_high caveat instead of launching an
immediate acquisition rescue, because base confidence is already accepted.

Continue the seed9227465 branch with target2 at the standard 5-source
Tx/Rx=60 control. If target2 is weak, use the existing evidence tree:
source-density brackets first at Tx/Rx=60, then acquisition brackets only if
source density fails or a target-specific transfer hypothesis is justified.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.249850 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target0 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91%; nvidia-smi process memory was about 294 MiB
```

## Next Decision

Run seed9227465 target2 with 5 sources and Tx/Rx=60. That production GPU run
is experiment 1020.
