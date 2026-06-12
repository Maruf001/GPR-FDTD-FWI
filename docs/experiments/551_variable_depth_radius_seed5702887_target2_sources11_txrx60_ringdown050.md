# Experiment 551: Seed5702887 Target2 Sources=11 Tx/Rx=60 Ringdown050

## Purpose

Run 1017 is the final seed5702887 target2 source-density escalation in this
branch. Previous target2 rows were exact but weak at 5, 7, and 9 sources, and
both lower and wider 9-source acquisition brackets failed to beat Tx/Rx=60.

## 1017: Coordinate Optimizer Variable-Depth/Radius Seed5702887 Target2 Sources=11 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1017_coordinate_optimizer_variable_depth_radius_seed5702887_target2_sources11_txrx60_ringdown050_objectives
```

## Results

Run 1017 is exact but still weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 11
tx_rx_offset_mm: 60.0
absolute radius margin: 4.421706e-04
offset from cutoff: -5.578294e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 847.6 s
```

Diagnostic objective margins:

```text
base       4.421706e-04  below cutoff by 5.578294e-05
highband   5.449440e-04  above cutoff
late       6.028628e-04  above cutoff
late_high  6.397626e-04  above cutoff
veryhigh   5.508058e-04  above cutoff
early_high 4.082342e-04  below cutoff by 9.176578e-05
```

All six objective variants rank the true target2 geometry first.

## Interpretation

The 11-source escalation does not rescue seed5702887 target2. It is weaker
than the 9-source Tx/Rx=60 row and comparable to the original 5-source control,
while still ranking the true geometry first. Across 5, 7, 9, and 11 sources,
and across Tx/Rx=45, 60, and 65 at 9 sources, target2 remains exact but below
the base confidence cutoff.

Stop target2 escalation for this branch. Continue with target1 so the seed can
be summarized with target0 accepted, target2 unresolved/weak, and target1
tested independently.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.214649 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target2 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=11; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 93%; nvidia-smi process memory was about 333 MiB
```

## Next Decision

Run seed5702887 target1 with 5 sources and Tx/Rx=60. That target1 control is
underway as experiment 1018.
