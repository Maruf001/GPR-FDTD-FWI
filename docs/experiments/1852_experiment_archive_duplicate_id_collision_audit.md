# Experiment 1852: Experiment Archive Duplicate ID Collision Audit

Date: 2026-07-02

## Purpose

Scan the numbered experiment output folders and experiment documentation files
for duplicate numeric IDs. This is a non-destructive audit: it does not rename,
move, or delete existing artifacts.

## Output

```text
outputs/experiments/1852_experiment_archive_duplicate_id_collision_audit
```

## Result

```text
output duplicate IDs:                  1
doc duplicate IDs:                     5
recent tail collisions:                1
manual resolution required IDs:        1
renumbering performed now:             false
FDTD executed now:                     false
field transfer ready:                  false
3D/HPC ready:                          false
gpu priority:                          none
```

The current output-archive collision is numeric ID `1848`.

## Decision

Do not reuse collided IDs. Use the next safe numeric output ID for new
experiment outputs and plan any renumbering separately.

## Validation

```text
3 focused tests passed
py_compile passed
figure dynamic range=255
script snapshots: 2
```
