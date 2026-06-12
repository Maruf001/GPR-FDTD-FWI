# Experiment 521: Seed2178309 Target1 Sources=5 Tx/Rx=50 Ringdown050

## Purpose

Run 987 tests whether acquisition offset, rather than source density or
receiver interpolation, rescues seed2178309 target1.

## 987: Coordinate Optimizer Variable-Depth/Radius Seed2178309 Target1 Sources=5 Tx/Rx=50 Ringdown050

Output:

```text
outputs/experiments/987_coordinate_optimizer_variable_depth_radius_seed2178309_target1_sources5_txrx50_ringdown050_objectives
```

## Results

Run 987 is exact and accepted with low reserve:

```text
tx_rx_offset_mm: 50.0
target: 1
sources: 5
best: x=250 mm, z=100 mm, r=6.0 mm
absolute radius margin: 5.057393e-04
offset from cutoff: +5.739296e-06
confidence label: moderate
fallback warning: none
elapsed: about 369.6 s
```

Diagnostic objective rows preserve the true target1 geometry. Early_high
remains below cutoff:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.057393e-04 | above cutoff |
| highband | 6.556585e-04 | above cutoff |
| late | 7.922184e-04 | above cutoff |
| late_high | 8.611185e-04 | above cutoff |
| veryhigh | 6.040097e-04 | above cutoff |
| early_high | 4.569140e-04 | below cutoff |

## Interpretation

Tx/Rx=50 rescues the seed2178309 target1 base confidence after Tx/Rx=60,
linear receiver sampling, and source-density escalation failed. The low reserve
and early_high caveat justify a Tx/Rx=45 bracket before promoting 50 mm as the
mechanism remedy.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.241713 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate row above the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 50.0; summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]
resources: 5-source GPU checks were about 87-88% utilization
```

## Next Decision

Run a seed2178309 target1 Tx/Rx=45 bracket probe at 5 sources. That run is
underway as experiment 988.
