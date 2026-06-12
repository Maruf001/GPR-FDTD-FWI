# Experiment 663: Seed591286729879 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Continue the Fibonacci replication chain after closing seed365435296162 and
splitting measured field-data outputs into their own archive. This run tests
seed591286729879 target0 at the standard 8-source Tx/Rx=60 control under the
ringdown050 source-mismatch/noise condition.

Seed validation had already succeeded in the active FNO environment:

```text
np.random.default_rng(591286729879) succeeded
```

## 1126: Coordinate Optimizer Variable-Depth/Radius Seed591286729879 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1126_coordinate_optimizer_variable_depth_radius_seed591286729879_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed591286729879:1.1,-50.0,1.1,0.10,591286729879,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed591286729879 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed591286729879_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1126 is exact and accepted with the recurring target0 late-window caveat:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.491301e-04
offset from cutoff: +4.913014e-05
relative margin: 3.497781e-02
confidence label: moderate
fallback warning: none
best misfit: 1.569939e-02
next radius misfit: 1.624852e-02
elapsed: 596.7 s
```

Diagnostic objective margins:

```text
base       5.491301e-04  above cutoff
highband   6.958209e-04  above cutoff
late       4.420546e-04  weak, below cutoff
late_high  4.584529e-04  weak, below cutoff
veryhigh   6.620532e-04  above cutoff
early_high 5.957421e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
distinct-radius competitor is `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.00 mm` at `z=81 mm`.

## Interpretation

The base confidence rule accepts target0 with about `4.91e-05` reserve over
the `5.0e-4` cutoff. Late and late_high are both weak, but this matches prior
accepted target0 controls, including seeds where the base row passed and both
late-window diagnostics stayed below cutoff. Because the selected geometry is
exact and every diagnostic objective ranks the true radius/depth first, no
target0 Tx/Rx probe is justified for this seed.

Close target0 as exact and accepted with a recurring late-window caveat, then
continue seed591286729879 with target2 at the standard 5-source Tx/Rx=60
control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3545 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1889 and unique_colors=822
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and unique_colors=3167
figure validation: system_scene_geometry.png is 1776x1065 RGB with nonwhite_fraction=0.6308 and unique_colors=2102
figure notes: figures/FIGURE_NOTES.md present, lists late and late_high below cutoff, and includes the system scene geometry section
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90%; run completed in 596.7 s
```

## Next Decision

Continue seed591286729879 with target2 at the standard 5-source Tx/Rx=60
control under the same ringdown050 objective suite.
