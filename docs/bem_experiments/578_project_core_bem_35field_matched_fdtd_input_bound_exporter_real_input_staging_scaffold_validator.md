# BEM Experiment 578: Matched FDTD Input-Bound Exporter Real-Input Staging Scaffold Validator

Date: 2026-06-30

## Purpose

Validate the run `577` input-bound matched-FDTD staging scaffold from saved
artifacts.

This run checks that the source gap block is ready, both staging directories
exist, all four required staged files are still missing, all actions and
downstream states remain blocked, and the figure and script snapshots exist.

## Output

```text
outputs/bem_experiments/578_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_validator_checks.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_validator.png
scripts/
```

## Result

```text
validation checks:                        5
passed checks:                            5
blocking failures:                        0
required directories:                     2
required staged files:                    4
required real input files:                2
required accepted return files:           2
missing files:                            4
staging actions:                          4
exporter execution ready:                 false
real BEM/FDTD comparison ready:           false
3D validation claim ready:                false
GPU/HPC ready:                            false
field transfer ready:                     false
field FWI ready:                          false
gpu priority:                             none
```

The five validation checks all pass:

```text
source_chain_ready
staging_directories_present
required_files_still_missing
actions_and_downstream_states_blocked
figure_and_script_snapshots_present
```

## Interpretation

The input-bound staging scaffold is valid and intentionally empty. It is now
safe to treat run `577` as the current BEM handoff drop-location checkpoint, but
not as evidence that any real matched-FDTD files exist.

## Decision

Use run `578` as the artifact guard for the input-bound matched-FDTD staging
scaffold. Do not run the exporter, BEM/FDTD comparison, 3D validation, GPU/HPC,
field transfer, or field FWI until real staged input files exist and pass the
acceptance gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_validator.py

6 passed
```

Figure validation:

```text
2285x841, dynamic range=255
```
