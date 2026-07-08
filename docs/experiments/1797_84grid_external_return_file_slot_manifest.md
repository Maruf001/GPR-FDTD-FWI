# Experiment 1797: 84-Grid External Return File-Slot Manifest

Date: 2026-07-01

## Purpose

Convert the run `1794` external-return dependency audit into a per-file
checklist for the 84-grid observed-by-case materialization return.

Runs `1794-1796` split the blocker into one approval dependency and ten paired
cache/result artifact jobs. This run turns that split into one row per required
external file.

## Output

```text
outputs/experiments/1797_local_2d_state_consistent_objective_revision_84grid_external_return_file_slot_manifest
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_file_slot_manifest_file_slot_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_file_slot_manifest_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_file_slot_manifest.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source dependency audit ready:             true
source validator ready:                    true
source sensitivity ready:                  true
file slots:                                21
stages:                                    5
approval-token slots:                      1
cache-array slots:                         10
result-JSON slots:                         10
paired artifact slots:                     20
artifact jobs:                             10
producer files present:                    0
core preflight-passed slots:               0
paired artifact jobs ready:                0
preflight-passed slots:                    0
ready slots:                               0
materialization input accepted:            false
ready for materialization:                 false
observed-by-case materialized:             false
new FDTD executed:                         false
field transfer ready:                      false
field FWI ready:                           false
3D/HPC ready:                              false
gpu priority:                              none
```

## Interpretation

The 84-grid external return now has a concrete file-level checklist:

| Slot class | Count | Requirement |
| --- | ---: | --- |
| Approval JSON | 1 | Must be provided before artifact intake |
| Cache-array NPZ | 10 | Must be paired with its matching result JSON |
| Result JSON | 10 | Must be paired with its matching cache-array NPZ |

The ten artifact jobs are not independently useful unless both files in each
pair pass preflight. No producer files are currently present, so no
materialization or new FDTD execution is authorized.

## Decision

Use this manifest as the file-level external-return checklist. Keep
observed-by-case materialization, new FDTD execution, field transfer, field FWI,
and 3D/HPC blocked until the approval token and all ten cache/result pairs pass
preflight.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_file_slot_manifest.py

3 passed
```

Figure check:

```text
2968x918, dynamic range=255
```
