# Experiment 544: Seed5702887 Target0 Sources=8 Tx/Rx=50 Ringdown050

## Purpose

Run 1010 brackets the seed5702887 target0 acquisition rescue on the lower side
of Tx/Rx=52.5. Run 1009 was exact and base-accepted at Tx/Rx=52.5, but only by
2.55e-07, so this run tests whether a 50 mm offset gives useful reserve.

## 1010: Coordinate Optimizer Variable-Depth/Radius Seed5702887 Target0 Sources=8 Tx/Rx=50 Ringdown050

Output:

```text
outputs/experiments/1010_coordinate_optimizer_variable_depth_radius_seed5702887_target0_sources8_txrx50_ringdown050_objectives
```

## Results

Run 1010 is exact and base-accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 50.0
absolute radius margin: 5.105064e-04
offset from cutoff: +1.050636e-05
confidence label: moderate
fallback warning: none
elapsed: 571.3 s
```

Diagnostic objective margins:

```text
base       5.105064e-04  above cutoff
highband   6.563274e-04  above cutoff
late       4.222659e-04  below cutoff by 7.773414e-05
late_high  4.179401e-04  below cutoff by 8.205987e-05
veryhigh   6.292094e-04  above cutoff
early_high 5.356677e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

Tx/Rx=50 is the strongest seed5702887 target0 8-source offset tested so far.
It improves the base margin by about 1.03e-05 over Tx/Rx=52.5 and by about
4.10e-05 over Tx/Rx=60. The late-window diagnostics remain below cutoff, but
their deficits are smaller than in the 52.5 and 60 mm runs.

Because the base margin is accepted but still low, run one lower-edge Tx/Rx=45
bracket before declaring the 8-source target0 policy. This checks whether the
lower-offset trend continues or whether 50 mm is the practical local optimum.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.244411 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target0 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 50.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91%; nvidia-smi process memory was about 294 MiB
```

## Next Decision

Run seed5702887 target0 with 8 sources and Tx/Rx=45. That lower-edge bracket
is underway as experiment 1011.
