# Experiment 523: Seed2178309 Target1 Sources=5 Tx/Rx=55 Ringdown050

## Purpose

Run 989 brackets the upper side of the seed2178309 target1 Tx/Rx offset rescue.

## 989: Coordinate Optimizer Variable-Depth/Radius Seed2178309 Target1 Sources=5 Tx/Rx=55 Ringdown050

Output:

```text
outputs/experiments/989_coordinate_optimizer_variable_depth_radius_seed2178309_target1_sources5_txrx55_ringdown050_objectives
```

## Results

Run 989 is exact and accepted:

```text
tx_rx_offset_mm: 55.0
target: 1
sources: 5
best: x=250 mm, z=100 mm, r=6.0 mm
absolute radius margin: 5.098189e-04
offset from cutoff: +9.818895e-06
confidence label: moderate
fallback warning: none
elapsed: about 361.2 s
```

Diagnostic rows preserve the true target1 geometry; early_high remains below
cutoff.

## Interpretation

Tx/Rx=55 is accepted and slightly stronger than Tx/Rx=50. Because Tx/Rx=60 is
weak, run Tx/Rx=57.5 to refine the upper edge of the accepted offset band.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.243516 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate row above the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 55.0; summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]
resources: 5-source GPU checks were about 88% utilization
```

## Next Decision

Run a seed2178309 target1 Tx/Rx=57.5 upper-edge probe at 5 sources. That run is
underway as experiment 990.
