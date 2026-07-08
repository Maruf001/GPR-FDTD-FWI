# BEM Experiment 577: Matched FDTD Input-Bound Exporter Real-Input Staging Scaffold

Date: 2026-06-30

## Purpose

Create an empty external staging scaffold for the real matched-FDTD input and
return CSV files required by runs `571-576`.

This run creates only staging directories. It does not create real input files,
does not create accepted return files, does not edit the locked historical run
`568` output folder, and does not promote exporter execution, BEM/FDTD
comparison, 3D validation, GPU/HPC, field transfer, or field FWI readiness.

## Output

```text
outputs/bem_experiments/577_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold
```

Staging root:

```text
outputs/bem_experiments/_external_fdtd_inputs/project_core_bem_35field_matched_fdtd_input_bound_exporter_pending
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_directory_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_staged_file_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_action_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold.png
scripts/
```

## Result

```text
source gap ready:                         true
source validation ready:                  true
source sensitivity ready:                 true
required directories:                     2
present directories:                      2
required staged files:                    4
required real input files:                2
required accepted return files:           2
present files:                            0
nonempty files:                           0
missing files:                            4
accepted files:                           0
unexpected files:                         0
staging actions:                          4
ready staging actions:                    0
exporter execution ready:                 false
real BEM/FDTD comparison ready:           false
3D validation claim ready:                false
GPU/HPC ready:                            false
field transfer ready:                     false
field FWI ready:                          false
gpu priority:                             none
```

The empty staging directories are:

```text
outputs/bem_experiments/_external_fdtd_inputs/project_core_bem_35field_matched_fdtd_input_bound_exporter_pending/real_fdtd_input_files
outputs/bem_experiments/_external_fdtd_inputs/project_core_bem_35field_matched_fdtd_input_bound_exporter_pending/real_fdtd_return_files
```

The four missing staged files are:

```text
real_fdtd_input_files/fdtd_source_hash_manifest_real_input.csv
real_fdtd_input_files/fdtd_scattered_norm_values_real_input.csv
real_fdtd_return_files/fdtd_source_hash_manifest_real_return.csv
real_fdtd_return_files/fdtd_scattered_norm_values_real_return.csv
```

## Interpretation

The BEM/FDTD matched handoff now has a clean external drop location. The current
state is still a scaffold only: no real matched-FDTD input files exist, no
accepted return files exist, and no comparison evidence exists.

## Decision

Use this staging scaffold as the current BEM handoff checkpoint. Do not run the
input-bound exporter, BEM/FDTD comparison, 3D validation, GPU/HPC, field
transfer, or field FWI until the staged real input files exist and pass the
acceptance gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_validator.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_validation_sensitivity.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold.py

12 passed
```

Figure validation:

```text
2465x845, dynamic range=255
```
