# Experiment 627: Seed20365011074 Target2 Sources=11 Tx/Rx=60 Ringdown050

## Purpose

Run the capped source-density follow-up for seed20365011074 target2 after the
9-source Tx/Rx=60 escalation nearly rescued the base margin but remained just
below the `5.0e-4` cutoff. This 11-source test follows the prior target2
policy for weak 9-source rows.

## 1093: Coordinate Optimizer Variable-Depth/Radius Seed20365011074 Target2 Sources=11 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1093_coordinate_optimizer_variable_depth_radius_seed20365011074_target2_sources11_txrx60_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 11 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed20365011074_target2_sources11_txrx60_ringdown050_objectives
```

## Results

Run 1093 is exact but a clear confidence regression:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 11
tx_rx_offset_mm: 60.0
absolute radius margin: 4.033775e-04
offset from cutoff: -9.662249e-05
relative margin: 2.755449e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.463927e-02
next radius misfit: 1.504264e-02
elapsed: 940.3 s
```

Diagnostic objective margins:

```text
base       4.033775e-04  weak, below cutoff
highband   5.072260e-04  above cutoff
late       5.662041e-04  above cutoff
late_high  5.963000e-04  above cutoff
veryhigh   4.923525e-04  weak, below cutoff
early_high 3.742475e-04  weak, below cutoff
```

All six objective variants rank the true target2 geometry first.

## Interpretation

The 11-source test does not rescue target2. It worsens the base margin relative
to the near-threshold 9-source row and introduces additional weak veryhigh and
early_high diagnostics. This closes the simple source-density ladder for
seed20365011074 target2. The best full-ringdown050 source-count row remains
the 9-source near miss from run 1092, but target2 is not formally accepted by
the current base-confidence cutoff. Continue the branch with target1 at the
standard 5-source Tx/Rx=60 control to determine whether seed20365011074 is a
target2-specific near-miss or a broader low-margin seed.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.186897 and unique_colors=264
visual inspection: confidence figure is readable and shows one weak target2 row clearly below cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=11; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 92-93%; host RAM stayed about 94-95 GiB available
```

## Next Decision

Run seed20365011074 target1 with the standard 5-source Tx/Rx=60 control.

## 2026-06-17 Addendum

A specialized target2 acquisition-offset probe has now been run:

```text
run:      1225_coordinate_optimizer_variable_depth_radius_seed20365011074_target2_sources5_txrx50_ringdown050_objectives
target:   target2
sources:  5
Tx/Rx:    50.0 mm
```

Run 1225 rescues the target2 branch. It preserves exact x/z/r geometry and
clears the strict base-margin cutoff:

| Run | Sources | Tx/Rx mm | Base margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1090 | 5 | 60.0 | 4.964072e-4 | -3.593e-6 | weak |
| 1091 | 7 | 60.0 | 4.743122e-4 | -2.569e-5 | weak |
| 1092 | 9 | 60.0 | 4.981292e-4 | -1.871e-6 | weak |
| 1093 | 11 | 60.0 | 4.033775e-4 | -9.662e-5 | weak |
| 1225 | 5 | 50.0 | 5.181019e-4 | +1.810e-5 | accepted |

All six diagnostic objective variants in run 1225 rank the exact geometry
first and clear the cutoff. This changes the seed20365011074 target2 status
from source-density unresolved to Tx/Rx=50 acquisition-offset rescued.
