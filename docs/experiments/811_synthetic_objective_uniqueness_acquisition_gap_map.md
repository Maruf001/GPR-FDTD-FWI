# Experiment 811: Synthetic Objective-Uniqueness Acquisition Gap Map

Date: 2026-06-17

## Purpose

CPU-only actionability map for the objective-uniqueness caveats found in
experiment 809 / run 1287. This groups exact-strong rows by target,
source-count metadata, Tx/Rx-offset metadata, geometry-delta class, and
near-tie tier so the next synthetic 2D work is evidence-gated.

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1289_synthetic_objective_uniqueness_acquisition_gap_map
```

Artifacts:

```text
data/synthetic_objective_uniqueness_acquisition_gap_rows.csv
data/synthetic_objective_uniqueness_acquisition_gap_summary.json
data/figure_validation.csv
figures/synthetic_objective_uniqueness_acquisition_gap_map.png
run_manifest.json
```

## Result

Policy label:

```text
objective_uniqueness_gap_map_known_target2_x_gaps_cpu_no_gpu
```

Summary:

```text
cells:                                22
exact-strong rows:                    323
near-tie rows:                        39
known-acquisition near-tie rows:       6
archive-metadata near-tie rows:       33
target1 known-acquisition near ties:   0
target2 known-acquisition near ties:   6
known actionable x-gap cells:          3
top actionable target:                 target2
top actionable sources/TxRx:           5 sources, Tx/Rx=45 mm
top actionable near-tie rows:          2
gpu priority:                          none_now
```

Known acquisition near ties are target2 only. The x-resolution subset is
concentrated in close14-style Tx/Rx=45 mm cells:

```text
target2, 5 sources, Tx/Rx=45 mm, x delta: 2 near-tie rows
target2, 4 sources, Tx/Rx=45 mm, x delta: 1 near-tie row
target2, 7 sources, Tx/Rx=45 mm, x delta: 1 near-tie row
```

There is also a known target2 `z+radius` caveat at 5 sources and Tx/Rx=20 mm.
The target1 objective caveats are archive rows with missing source/TxRx
metadata, so they remain claim-boundary caveats rather than GPU-priority
branches.

## Interpretation

The next synthetic 2D step should still be CPU-first objective/reporting design.
If a new GPU run becomes necessary for the manuscript, this map argues for a
narrow target2 x-resolution probe after the objective scope is fixed, not a
broad sweep. The old target1 caveat is not actionable as a new acquisition run
from the current archive metadata.

## Validation

Focused tests:

```text
tests/test_synthetic_objective_uniqueness_acquisition_gap_map.py: 2 passed
```

Figure validation:

```text
synthetic_objective_uniqueness_acquisition_gap_map.png: 2569x903,
nonwhite=0.2126, dynamic range=255
```
