# BEM Experiment 583: Matched FDTD Input-Bound Exporter Real-Input Staging Receipt Acceptance Gate

Date: 2026-06-30

## Purpose

Apply a real receipt acceptance gate to the external matched-FDTD staging paths
defined by runs `580-582`.

Earlier gates validated the old in-run template locations. Runs `577-582`
moved the handoff to a fresh external staging area. This run checks those
external staged paths directly and applies row/content validation when files
are present.

This run does not run FDTD, does not run the exporter, does not write accepted
return files, and does not compare BEM and FDTD.

## Output

```text
outputs/bem_experiments/583_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate_receipt_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate_action_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate.png
scripts/
```

## Result

```text
source manifest ready:                   true
source validation ready:                 true
source sensitivity ready:                true
receipt rows:                            4
real input receipt rows:                 2
accepted return receipt rows:            2
present staged files:                    0
nonempty staged files:                   0
accepted files:                          0
accepted real input files:               0
accepted return files:                   0
accepted input rows:                     0
accepted return rows:                    0
validation errors:                       0
actions:                                 4
ready actions:                           0
exporter execution ready:                false
real BEM/FDTD comparison ready:          false
3D validation claim ready:               false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
gpu priority:                            none
```

The gate covers four externally staged files:

| File key | Role | Acceptance rule |
| --- | --- | --- |
| `fdtd_source_hash_manifest` | real input file | `returned_fdtd_source_hash` must be 64 lowercase hexadecimal characters |
| `fdtd_source_hash_manifest` | accepted return file | same row/content validation after exporter output |
| `fdtd_scattered_norm_values` | real input file | `returned_fdtd_scattered_norm` must be positive and finite |
| `fdtd_scattered_norm_values` | accepted return file | same row/content validation after exporter output |

## Interpretation

The external staging receipt gate is now executable and content-aware. It can
accept real files when they appear, but the current staging area is still empty.

This closes the gap between a manifest and an enforceable receipt check. The
project still has no accepted matched-FDTD input files, no accepted return
files, and no BEM/FDTD comparison evidence from this branch.

## Decision

Do not run the input-bound exporter or BEM/FDTD comparison until real staged
files pass this receipt gate. Keep 3D validation, GPU/HPC escalation, field
transfer, and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate.py

5 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
