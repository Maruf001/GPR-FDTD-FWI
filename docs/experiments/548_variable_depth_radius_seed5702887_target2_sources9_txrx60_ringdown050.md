# Experiment 548: Seed5702887 Target2 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Run 1014 tests whether a 9-source Tx/Rx=60 source-density escalation rescues
seed5702887 target2 after the 5-source and 7-source controls both stayed weak.

## 1014: Coordinate Optimizer Variable-Depth/Radius Seed5702887 Target2 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1014_coordinate_optimizer_variable_depth_radius_seed5702887_target2_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1014 is exact but still weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 4.834373e-04
offset from cutoff: -1.656272e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 660.3 s
```

Diagnostic objective margins:

```text
base       4.834373e-04  below cutoff by 1.656272e-05
highband   6.442151e-04  above cutoff
late       7.561168e-04  above cutoff
late_high  8.692000e-04  above cutoff
veryhigh   6.712157e-04  above cutoff
early_high 4.745717e-04  below cutoff by 2.542834e-05
```

All six objective variants rank the true target2 geometry first.

## Interpretation

Nine sources recover much of the lost margin relative to the 7-source run, but
not enough to accept target2 at Tx/Rx=60. The result remains exact and
truth-ranked, with strong highband and late-window diagnostics, but base and
early_high remain below cutoff.

Do not continue blind source-density escalation at Tx/Rx=60. Switch mechanism
by combining the closest source-density row with the strongest lower-offset
acquisition point from the seed5702887 target0 bracket: 9 sources and Tx/Rx=45.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.232680 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target2 row just below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91-92%; nvidia-smi process memory was about 307 MiB
```

## Next Decision

Run seed5702887 target2 with 9 sources and Tx/Rx=45. That combined
source-density/acquisition rescue is underway as experiment 1015.
