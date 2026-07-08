# Experiment 1853: Experiment Archive Next ID Allocation Guard

Date: 2026-07-02

## Purpose

Use the duplicate-ID audit's recommended next safe output ID and verify that
the current allocation is unique. This guard does not rename, move, or delete
existing archive entries.

## Output

```text
outputs/experiments/1853_experiment_archive_next_id_allocation_guard
```

## Result

```text
previous next safe output ID:           1853
current numeric ID:                     1853
current output ID entries:              1
current doc ID entries:                 1
next safe output ID after current:      1854
renumbering performed now:              false
FDTD executed now:                      false
field transfer ready:                   false
3D/HPC ready:                           false
gpu priority:                           none
```

## Decision

Use `1854` as the next safe output numeric ID for subsequent experiment outputs.
Any cleanup of older collided IDs should be planned separately.

## Validation

```text
3 focused tests passed
py_compile passed
figure dynamic range=255
script snapshots: 2
```
