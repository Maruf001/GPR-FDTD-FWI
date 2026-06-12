# Experiment 522: Seed2178309 Target1 Sources=5 Tx/Rx=45 Ringdown050

## Purpose

Run 988 brackets the lower side of the Tx/Rx offset rescue after Tx/Rx=50
accepted seed2178309 target1.

## 988: Coordinate Optimizer Variable-Depth/Radius Seed2178309 Target1 Sources=5 Tx/Rx=45 Ringdown050

Output:

```text
outputs/experiments/988_coordinate_optimizer_variable_depth_radius_seed2178309_target1_sources5_txrx45_ringdown050_objectives
```

## Results

Run 988 is exact but weak:

```text
tx_rx_offset_mm: 45.0
target: 1
sources: 5
best: x=250 mm, z=100 mm, r=6.0 mm
absolute radius margin: 4.759223e-04
offset from cutoff: -2.407768e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: about 371.3 s
```

Diagnostic rows preserve the true target1 geometry; base and early_high are
below cutoff.

## Interpretation

Tx/Rx=45 does not preserve the Tx/Rx=50 rescue. Continue with Tx/Rx=55 to
bracket the accepted offset band.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.228190 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak row below the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 45.0; summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]
resources: 5-source GPU checks were about 87-88% utilization
```

## Next Decision

Run a seed2178309 target1 Tx/Rx=55 upper-bracket probe at 5 sources. That run
is underway as experiment 989.
