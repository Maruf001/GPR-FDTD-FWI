# Experiment 729: Seed498454012769264 Target2 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Escalate the seed498454012769264 target2 branch to 9 sources after the
5-source control was a practical near-zero acceptance and the 7-source bracket
fell below the moderate cutoff.

## 1192: Coordinate Optimizer Variable-Depth/Radius Seed498454012769264 Target2 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1192_coordinate_optimizer_variable_depth_radius_seed498454012769264_target2_sources9_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed498454012769264:1.1,-50.0,1.1,0.10,498454012769264,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed498454012769264 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed498454012769264_target2_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1192 selected the exact geometry and cleared the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 5.422296e-04
offset from cutoff: 4.222962e-05
relative margin: 3.422647e-02
confidence label: moderate
fallback warning: none
best misfit: 1.584241e-02
next radius misfit: 1.638464e-02
elapsed: 657.2 s
```

Diagnostic objective margins:

```text
base       5.422296e-04  above cutoff
highband   7.088243e-04  above cutoff
late       8.263690e-04  above cutoff
late_high  9.507334e-04  above cutoff
veryhigh   7.827900e-04  above cutoff
early_high 5.173297e-04  above cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
base objective distinct-radius competitor is `r=8.75 mm` at `z=121 mm`, which
is also the closest changed-geometry competitor.

## Interpretation

The 9-source escalation rescues the target2 branch. It moves the base margin
from a practical near-zero 5-source result and a weak 7-source bracket to a
moderate result with all diagnostic objectives above cutoff. No further
target2 rescue is justified for this seed; continue to target1.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3353 and sampled_unique_colors=73
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1678 and sampled_unique_colors=82
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0618 and sampled_unique_colors=157
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6261 and sampled_unique_colors=118
figure notes: figures/FIGURE_NOTES.md present, reports one moderate row and no objective variants below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 657.2 s through the candidate sweep
```

## Next Decision

Continue seed498454012769264 with target1 at the standard 5-source Tx/Rx=60
control.
