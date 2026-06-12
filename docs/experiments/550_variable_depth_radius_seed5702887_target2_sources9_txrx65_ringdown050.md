# Experiment 550: Seed5702887 Target2 Sources=9 Tx/Rx=65 Ringdown050

## Purpose

Run 1016 tests the wider-aperture side of the seed5702887 target2 acquisition
bracket. Tx/Rx=45 was worse than Tx/Rx=60, so this run asks whether target2
instead wants a larger Tx/Rx offset at the same 9-source density.

## 1016: Coordinate Optimizer Variable-Depth/Radius Seed5702887 Target2 Sources=9 Tx/Rx=65 Ringdown050

Output:

```text
outputs/experiments/1016_coordinate_optimizer_variable_depth_radius_seed5702887_target2_sources9_txrx65_ringdown050_objectives
```

## Results

Run 1016 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 9
tx_rx_offset_mm: 65.0
absolute radius margin: 4.749441e-04
offset from cutoff: -2.505586e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 659.4 s
```

Diagnostic objective margins:

```text
base       4.749441e-04  below cutoff by 2.505586e-05
highband   6.176548e-04  above cutoff
late       7.138868e-04  above cutoff
late_high  8.242603e-04  above cutoff
veryhigh   6.387243e-04  above cutoff
early_high 4.666352e-04  below cutoff by 3.333648e-05
```

All six objective variants rank the true target2 geometry first.

## Interpretation

Tx/Rx=65 does not rescue seed5702887 target2. It is better than Tx/Rx=45 but
still worse than the 9-source Tx/Rx=60 row. The acquisition bracket therefore
does not identify a better offset among 45, 60, and 65 mm.

Return to the best tested aperture, Tx/Rx=60, and run one 11-source escalation.
This is no longer blind source-density escalation: lower and wider acquisition
brackets were both tested and failed to beat Tx/Rx=60.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.229074 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target2 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 65.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91-92%; nvidia-smi process memory was about 307 MiB
```

## Next Decision

Run seed5702887 target2 with 11 sources and Tx/Rx=60. That escalation is
underway as experiment 1017.
