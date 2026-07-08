# BEM Experiment 742: Strict Real-Producer Execution Priority Map

Date: 2026-07-01

## Purpose

Convert the strict real-producer completion worksheet from run `741` into an
execution-priority map.

This run does not execute FDTD, create real BEM/FDTD evidence, run 3D
validation, launch GPU/HPC work, transfer to field data, or run field FWI.

## Output

```text
outputs/bem_experiments/742_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_execution_priority_map
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_execution_priority_map_item_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_execution_priority_map_batch_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_execution_priority_map_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_execution_priority_map.png
scripts/script_snapshot_manifest.json
```

## Result

```text
producer files:                         2
receiver count:                         31
frequency count:                        9
receiver-frequency pairs:               279
priority batches:                       5
strict file rows required:              558
strict real-data cells required:        2232
first batch pairs:                      1
first three batches pairs:              39
first three batches real-data cells:    312
midband pairs:                          120
edgeband pairs:                         120
live files present:                     0
exact contract hashes ready:            558
strict contract hash errors:            0
real BEM/FDTD comparison ready:         false
GPU/HPC ready:                          false
field transfer ready:                   false
field FWI ready:                        false
```

Execution batches:

| Stage | Batch | Pairs | File rows | Real-data cells | Cumulative pairs |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | center pair smoke | 1 | 2 | 8 | 1 |
| 2 | center receiver frequency sweep | 8 | 16 | 64 | 9 |
| 3 | center frequency receiver sweep | 30 | 60 | 240 | 39 |
| 4 | midband receiver matrix | 120 | 240 | 960 | 159 |
| 5 | edgeband receiver matrix | 120 | 240 | 960 | 279 |

## Interpretation

The two strict producer files contain the same 279 receiver-frequency pairs.
Each pair requires two file rows and eight real-data cells: real solver status,
real solver log hash, real FDTD export flag, and returned value in each of the
two files.

The map provides a practical producer sequence. Start with one center
receiver-frequency pair, then complete the center-receiver spectral sweep, then
the center-frequency receiver sweep, then the midband matrix, then the edge
frequencies required for full strict acceptance.

## Decision

Use this map for real producer scheduling. Keep real BEM/FDTD comparison,
3D validation, GPU/HPC work, field transfer, and field FWI blocked until all
five batches are returned in both live files and strict acceptance passes.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_execution_priority_map.py
4 passed
```

Figure check:

```text
2589x916, dynamic range=255
```
