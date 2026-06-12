# Experiment 526: Seed2178309 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

## Purpose

Run 992 checks whether the Tx/Rx=52.5 target1 remedy is safe for seed2178309
target0.

## 992: Coordinate Optimizer Variable-Depth/Radius Seed2178309 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/992_coordinate_optimizer_variable_depth_radius_seed2178309_target0_sources8_txrx52p5_ringdown050_objectives
```

## Results

Run 992 is exact and base-accepted:

```text
tx_rx_offset_mm: 52.5
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
absolute radius margin: 5.058533e-04
offset from cutoff: +5.853295e-06
confidence label: moderate
fallback warning: none
elapsed: about 587.7 s
```

Diagnostic rows preserve the true target0 geometry. Late and late_high remain
below cutoff.

## Interpretation

Tx/Rx=52.5 is target0-safe at the base objective, although it keeps the
late-window caveat. Continue the all-target check with target2.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.241735 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate row above the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]
resources: 8-source GPU checks were about 91-92% utilization; Python process RSS was about 456 MB during the sweep
```

## Next Decision

Run seed2178309 target2 at Tx/Rx=52.5. That run is underway as experiment 993.
