# BEM Experiment 546: Matched FDTD Return Real-File Staging Scaffold

Date: 2026-06-30

## Purpose

Create the empty staging directory for the two real matched-FDTD return CSV
files required by runs `543-545`.

This run creates only the directory scaffold. It does not create return files,
does not create synthetic substitutes, and does not promote comparison,
GPU/HPC, field-transfer, or field-FWI readiness.

## Output

```text
outputs/bem_experiments/546_project_core_bem_35field_matched_fdtd_return_real_file_staging_scaffold
```

Staging root:

```text
outputs/bem_experiments/_external_fdtd_returns/project_core_bem_35field_matched_fdtd_return_pending
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_real_file_staging_scaffold_directory_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_file_staging_scaffold_staged_file_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_file_staging_scaffold_action_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_file_staging_scaffold_summary.json
figures/project_core_bem_35field_matched_fdtd_return_real_file_staging_scaffold.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source gate ready:                         true
source validation ready:                   true
source sensitivity ready:                  true
required directories:                      1
present directories:                       1
required files:                            2
present files:                             0
nonempty files:                            0
missing files:                             2
accepted files:                            0
unexpected files:                          0
staging actions:                           3
ready staging actions:                     0
staging scaffold ready:                    true
real return packet accepted:               false
real BEM/FDTD comparison ready:            false
GPU priority:                              none
```

The two missing files are:

```text
fdtd_source_hash_manifest_real_return.csv
fdtd_scattered_norm_values_real_return.csv
```

## Decision

The BEM return-file drop location now exists. The branch remains blocked until
both real matched-FDTD return CSV files are copied into that directory and pass
the run `543` acceptance gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_real_file_staging_scaffold.py
3 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
