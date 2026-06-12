# Experiment 543: Seed5702887 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

## Purpose

Run 1009 tests the first acquisition-offset rescue for seed5702887 target0.
Run 1008 was exact but weak at 8 sources and Tx/Rx=60, so this run keeps the
source count fixed and reduces Tx/Rx to 52.5 mm.

## 1009: Coordinate Optimizer Variable-Depth/Radius Seed5702887 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1009_coordinate_optimizer_variable_depth_radius_seed5702887_target0_sources8_txrx52p5_ringdown050_objectives
```

## Results

Run 1009 is exact and marginally base-accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 52.5
absolute radius margin: 5.002552e-04
offset from cutoff: +2.551861e-07
confidence label: moderate
fallback warning: none
elapsed: 576.0 s
```

Diagnostic objective margins:

```text
base       5.002552e-04  above cutoff by 2.551861e-07
highband   6.406452e-04  above cutoff
late       4.033034e-04  below cutoff by 9.669664e-05
late_high  3.997451e-04  below cutoff by 1.002549e-04
veryhigh   6.035753e-04  above cutoff
early_high 5.266328e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

Tx/Rx=52.5 improves the seed5702887 target0 base margin from weak to barely
accepted, but the reserve is too small to treat as a robust policy by itself.
Late and late_high remain below cutoff by about 1.0e-04, so this is a
truth-preserving, caveated rescue rather than a clean one.

Before increasing source density, bracket the acquisition remedy at Tx/Rx=50.
If the lower offset strengthens base confidence, it may provide a better
8-source policy; if it fails, the next decision should compare Tx/Rx=55 versus
source-density escalation.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.239903 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one marginal moderate target0 row at the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91%; nvidia-smi process memory was about 294 MiB
```

## Next Decision

Run seed5702887 target0 with 8 sources and Tx/Rx=50. That acquisition bracket
is underway as experiment 1010.
