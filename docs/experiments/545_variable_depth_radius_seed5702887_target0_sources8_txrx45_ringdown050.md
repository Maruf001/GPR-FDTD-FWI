# Experiment 545: Seed5702887 Target0 Sources=8 Tx/Rx=45 Ringdown050

## Purpose

Run 1011 checks the lower edge of the seed5702887 target0 acquisition bracket.
The target0 sequence was weak at Tx/Rx=60, marginal at 52.5, and accepted at
50, so this run tests whether 45 mm gives enough reserve to stop the target0
rescue branch and continue with target2.

## 1011: Coordinate Optimizer Variable-Depth/Radius Seed5702887 Target0 Sources=8 Tx/Rx=45 Ringdown050

Output:

```text
outputs/experiments/1011_coordinate_optimizer_variable_depth_radius_seed5702887_target0_sources8_txrx45_ringdown050_objectives
```

## Results

Run 1011 is exact and base-accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 45.0
absolute radius margin: 5.313755e-04
offset from cutoff: +3.137755e-05
confidence label: moderate
fallback warning: none
elapsed: 574.3 s
```

Diagnostic objective margins:

```text
base       5.313755e-04  above cutoff
highband   6.961627e-04  above cutoff
late       4.892123e-04  below cutoff by 1.078771e-05
late_high  4.925306e-04  below cutoff by 7.469444e-06
veryhigh   7.087326e-04  above cutoff
early_high 5.545879e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

Tx/Rx=45 is the strongest tested 8-source target0 policy point for
seed5702887. It improves the base margin by about 2.09e-05 over Tx/Rx=50, by
about 3.11e-05 over Tx/Rx=52.5, and by about 6.19e-05 over Tx/Rx=60. The
late-window objectives remain just below cutoff, but their deficits are now
small compared with the earlier 50, 52.5, and 60 mm offsets.

Stop the target0 acquisition sweep here for this branch. The result is not a
fully clean diagnostic row, but it is a defensible base-accepted target0 policy
with small late-window caveats. Continue seed5702887 with target2 at the
standard 5-source Tx/Rx=60 control.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.253426 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target0 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 45.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91%; nvidia-smi process memory was about 294 MiB
```

## Next Decision

Run seed5702887 target2 with 5 sources and Tx/Rx=60. That target2 control is
underway as experiment 1012.
