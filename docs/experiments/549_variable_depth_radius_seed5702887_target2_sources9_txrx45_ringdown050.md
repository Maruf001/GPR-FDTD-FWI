# Experiment 549: Seed5702887 Target2 Sources=9 Tx/Rx=45 Ringdown050

## Purpose

Run 1015 tests whether combining 9 sources with the lower Tx/Rx=45 acquisition
point can rescue seed5702887 target2. Tx/Rx=45 was the strongest target0
acquisition point, while target2 at 9 sources and Tx/Rx=60 was close but still
weak.

## 1015: Coordinate Optimizer Variable-Depth/Radius Seed5702887 Target2 Sources=9 Tx/Rx=45 Ringdown050

Output:

```text
outputs/experiments/1015_coordinate_optimizer_variable_depth_radius_seed5702887_target2_sources9_txrx45_ringdown050_objectives
```

## Results

Run 1015 is exact but much weaker than the Tx/Rx=60 9-source row:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 9
tx_rx_offset_mm: 45.0
absolute radius margin: 3.766762e-04
offset from cutoff: -1.233238e-04
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 659.7 s
```

Diagnostic objective margins:

```text
base       3.766762e-04  below cutoff by 1.233238e-04
highband   4.982323e-04  below cutoff by 1.767675e-06
late       6.202923e-04  above cutoff
late_high  6.754092e-04  above cutoff
veryhigh   5.494191e-04  above cutoff
early_high 3.224508e-04  below cutoff by 1.775492e-04
```

All six objective variants rank the true target2 geometry first.

## Interpretation

The lower Tx/Rx=45 acquisition point does not transfer from target0 to target2.
It degrades base confidence from 4.834e-04 at Tx/Rx=60 to 3.767e-04, and it
also pushes highband fractionally below cutoff. Target2 therefore should not
use the target0 low-offset policy.

Bracket the acquisition mechanism in the opposite direction with 9 sources and
Tx/Rx=65. That tests whether the deeper target2 needs wider aperture rather
than lower offset.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.187604 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target2 row far below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 45.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91-92%; nvidia-smi process memory was about 307 MiB
```

## Next Decision

Run seed5702887 target2 with 9 sources and Tx/Rx=65. That wider-aperture
bracket is underway as experiment 1016.
