# Experiment 626: Seed20365011074 Target2 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Escalate seed20365011074 target2 after both the 5-source control and 7-source
source-density bracket recovered the exact geometry but remained below the
base confidence cutoff. This run tests the established 9-source Tx/Rx=60
target2 rescue.

## 1092: Coordinate Optimizer Variable-Depth/Radius Seed20365011074 Target2 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1092_coordinate_optimizer_variable_depth_radius_seed20365011074_target2_sources9_txrx60_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed20365011074_target2_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1092 is exact and much stronger than the 7-source bracket, but still
technically weak by the base confidence rule:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 4.981292e-04
offset from cutoff: -1.870782e-06
relative margin: 3.167762e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.572496e-02
next radius misfit: 1.622309e-02
elapsed: 721.9 s
```

Diagnostic objective margins:

```text
base       4.981292e-04  weak, below cutoff
highband   6.849456e-04  above cutoff
late       7.609248e-04  above cutoff
late_high  8.948292e-04  above cutoff
veryhigh   6.943830e-04  above cutoff
early_high 5.115786e-04  above cutoff
```

All six objective variants rank the true target2 geometry first.

## Interpretation

The 9-source escalation nearly rescues seed20365011074 target2. It improves
the base margin over the 7-source bracket and makes every diagnostic objective
except base clear cutoff. However, the production base row still misses the
`5.0e-4` cutoff by `1.870782e-06`, so this should not be silently promoted as
accepted. Prior target2 policy for weak 9-source rows runs one 11-source
source-density test before declaring the simple source-density path
unresolved. That is the next substantive experiment.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.225663 and unique_colors=264
visual inspection: confidence figure is readable and shows one weak target2 row just below cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91-92%; host RAM stayed about 94-95 GiB available
```

## Next Decision

Run seed20365011074 target2 with an 11-source Tx/Rx=60 source-density test.
