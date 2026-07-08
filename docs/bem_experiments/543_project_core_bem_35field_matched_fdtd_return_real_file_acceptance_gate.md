# BEM Experiment 543: Matched FDTD Return Real-File Acceptance Gate

Date: 2026-06-30

## Purpose

Turn the matched-FDTD return schema from runs `537-542` into a concrete
acceptance gate for future real FDTD return files.

This run does not create synthetic substitutes and does not accept any real
evidence. It defines the exact file, row, and column checks that the returned
FDTD packet must satisfy before BEM/FDTD comparison evidence can be promoted.

## Output

```text
outputs/bem_experiments/543_project_core_bem_35field_matched_fdtd_return_real_file_acceptance_gate
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_real_file_acceptance_gate_file_gate_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_file_acceptance_gate_entry_gate_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_file_acceptance_gate_column_gate_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_file_acceptance_gate_acceptance_action_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_file_acceptance_gate_summary.json
figures/project_core_bem_35field_matched_fdtd_return_real_file_acceptance_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source schema ready:                       true
source schema validation ready:            true
source schema sensitivity ready:           true
source implementation-gap ready:           true
source gap validation ready:               true
source gap sensitivity ready:              true
required real return files:                2
present real return files:                 0
nonempty real return files:                0
accepted real return files:                0
required real return entries:              558
accepted real return entries:              0
required columns:                          22
accepted columns:                          0
acceptance actions:                        4
ready acceptance actions:                  0
acceptance gate ready:                     true
real return packet accepted:               false
real BEM/FDTD comparison ready:            false
GPU priority:                              none
```

The gate requires two future real files:

| File key | Required rows | Required value field |
| --- | ---: | --- |
| `fdtd_source_hash_manifest` | 279 | `returned_fdtd_source_hash` |
| `fdtd_scattered_norm_values` | 279 | `returned_fdtd_scattered_norm` |

## Decision

The BEM side now has an explicit acceptance gate for the matched-FDTD return
packet. The current state remains non-evidence: no real FDTD return files,
rows, or columns are accepted.

The next BEM implementation task is still the real FDTD return-value exporter.
Comparison evidence, 3D validation, GPU/HPC escalation, field transfer, and
field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_real_file_acceptance_gate.py
4 passed
```

Figure check:

```text
2681x846, dynamic range=255
```
