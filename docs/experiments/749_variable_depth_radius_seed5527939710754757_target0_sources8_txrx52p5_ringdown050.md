# Experiment 749: Seed5527939710754757 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

## Purpose

Run the first target0 acquisition-offset rescue for seed5527939710754757. Run
1211 was exact but weak at the standard 8-source Tx/Rx=60 control, so this run
keeps the source count fixed and reduces Tx/Rx to 52.5 mm.

## 1212: Coordinate Optimizer Variable-Depth/Radius Seed5527939710754757 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1212_coordinate_optimizer_variable_depth_radius_seed5527939710754757_target0_sources8_txrx52p5_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 8 \
  --tx-rx-offset-mm 52.5 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed5527939710754757_target0_sources8_txrx52p5_ringdown050_objectives
```

## Results

Run 1212 selected the exact target0 geometry and improved the base margin, but
it remained just below the moderate-confidence cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 52.5
absolute radius margin: 4.930069e-04
offset from cutoff: -6.993121e-06
relative margin: 2.692209e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.831236e-02
next radius misfit: 1.880536e-02
elapsed: 579.3 s
```

Diagnostic objective margins:

```text
base       4.930069e-04  below cutoff
highband   6.305737e-04  above cutoff
late       3.023563e-04  below cutoff
late_high  3.747556e-04  below cutoff
veryhigh   6.092756e-04  above cutoff
early_high 5.349299e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
base objective distinct-radius competitor is `r=5.25 mm`; the closest
changed-geometry competitor is `x=150 mm`, `z=81 mm`, `r=6.0 mm`.

## Interpretation

Tx/Rx=52.5 improves the base margin by about `4.25e-05` relative to the
Tx/Rx=60 control and reduces the cutoff deficit from about `4.95e-05` to
`6.99e-06`. Because the acquisition offset improves the row but remains just
short of the cutoff, follow the established target0 acquisition-bracket policy
and test Tx/Rx=50 before changing mechanism or carrying weak confidence.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB and nonblank
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB and nonblank
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB and nonblank
figure validation: system_scene_geometry.png is 1768x1065 RGB and nonblank
figure notes: figures/FIGURE_NOTES.md present and reports weak confidence/below-cutoff variants
metadata validation: tx_rx_offset_mm is 52.5; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 579.3 s through the candidate sweep
```

## Next Decision

Run seed5527939710754757 target0 with 8 sources at Tx/Rx=50 mm.
