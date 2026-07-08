# BEM Experiment 537: Matched FDTD Return Real-Export Schema Contract

Date: 2026-06-30

## Purpose

Define the acceptance schema for future real matched-FDTD return exports.

Runs `534-536` showed that the guarded real-export path correctly refuses both
matched FDTD return-file keys. This run turns the next implementation step into
a concrete schema:

```text
What files, row keys, and columns must exist before matched FDTD return values
can be accepted for BEM/FDTD comparison?
```

This is a CPU-only contract run. It does not execute FDTD, BEM solves, FWI, GPU
kernels, field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/bem_experiments/537_project_core_bem_35field_matched_fdtd_return_real_export_schema_contract
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_return_file_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_return_column_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_return_key_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_action_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_summary.json
figures/project_core_bem_35field_matched_fdtd_return_real_export_schema_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source gap audit ready:                    true
source validator ready:                    true
source sensitivity ready:                  true
future FDTD return files:                  2
required FDTD return rows:                 558
required return columns:                   22
real return files present now:             0
real FDTD values present now:              0
return-file schemas accepted now:          0
row schemas accepted now:                  0
template/synthetic outputs allowed:        0
implementation actions:                    4
ready implementation actions:              0
schema contract ready:                     true
accepted evidence ready:                   false
real BEM/FDTD comparison ready:            false
3D validation claim ready:                 false
GPU/HPC ready:                             false
field transfer ready:                      false
field FWI ready:                           false
GPU priority:                              none
```

The two future return files are:

| File key | Future filename | Rows | Required value field |
| --- | --- | ---: | --- |
| `fdtd_source_hash_manifest` | `fdtd_source_hash_manifest_real_return.csv` | 279 | `returned_fdtd_source_hash` |
| `fdtd_scattered_norm_values` | `fdtd_scattered_norm_values_real_return.csv` | 279 | `returned_fdtd_scattered_norm` |

Each file has the same 10 common columns plus one file-specific value column.
The 558 row keys are inherited from the matched BEM/FDTD handoff, so any future
FDTD return must align to the same receiver-frequency rows before comparison.

## Decision

Use this schema before accepting matched FDTD return files or writing accepted
BEM/FDTD comparison evidence. The next BEM task is a validator for this schema
contract, followed by a sensitivity run, then a bounded real-export
implementation.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_real_export_schema_contract.py
3 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
