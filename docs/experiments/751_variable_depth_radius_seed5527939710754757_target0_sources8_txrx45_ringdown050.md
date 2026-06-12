# Experiment 751: Seed5527939710754757 Target0 Sources=8 Tx/Rx=45 Ringdown050

## Purpose

Check the lower edge of the seed5527939710754757 target0 acquisition bracket.
The target0 sequence was weak at Tx/Rx=60, near-miss weak at 52.5, and
accepted with very small reserve at 50, so this run tests whether 45 mm gives a
stronger accepted point before closing target0.

## 1214: Coordinate Optimizer Variable-Depth/Radius Seed5527939710754757 Target0 Sources=8 Tx/Rx=45 Ringdown050

Output:

```text
outputs/experiments/1214_coordinate_optimizer_variable_depth_radius_seed5527939710754757_target0_sources8_txrx45_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 8 \
  --tx-rx-offset-mm 45 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed5527939710754757:1.1,-50.0,1.1,0.10,5527939710754757,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed5527939710754757 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed5527939710754757_target0_sources8_txrx45_ringdown050_objectives
```

## Results

Run 1214 selected the exact target0 geometry and produced the strongest base
margin in the tested acquisition bracket:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 45.0
absolute radius margin: 5.149536e-04
offset from cutoff: 1.495360e-05
relative margin: 2.431476e-02
confidence label: moderate
fallback warning: none
best misfit: 2.117864e-02
next radius misfit: 2.169359e-02
elapsed: 592.7 s
```

Diagnostic objective margins:

```text
base       5.149536e-04  above cutoff
highband   6.519562e-04  above cutoff
late       3.417784e-04  below cutoff
late_high  4.140862e-04  below cutoff
veryhigh   6.876563e-04  above cutoff
early_high 5.323056e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
base objective distinct-radius competitor is `r=5.25 mm`; the closest
changed-geometry competitor is `x=150 mm`, `z=81 mm`, `r=6.0 mm`.

## Interpretation

Tx/Rx=45 is the strongest tested seed5527939710754757 target0 acquisition
point. It improves the base margin by about `1.25e-05` over Tx/Rx=50,
`2.19e-05` over Tx/Rx=52.5, and `6.44e-05` over Tx/Rx=60. Late and late_high
remain below cutoff, but the exact geometry is stable across all diagnostic
objectives. Stop the target0 acquisition sweep here and continue to target2 at
the standard 5-source Tx/Rx=60 control.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB and nonblank
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB and nonblank
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB and nonblank
figure validation: system_scene_geometry.png is 1769x1065 RGB and nonblank
figure notes: figures/FIGURE_NOTES.md present and reports moderate confidence plus below-cutoff variants
metadata validation: tx_rx_offset_mm is 45.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 592.7 s through the candidate sweep
```

## Next Decision

Continue seed5527939710754757 with target2 at the standard 5-source Tx/Rx=60 mm
control.
