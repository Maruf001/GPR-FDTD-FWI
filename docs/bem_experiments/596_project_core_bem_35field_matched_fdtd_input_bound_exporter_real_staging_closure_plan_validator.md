# BEM Experiment 596: Matched FDTD Input-Bound Exporter Real Staging Closure Plan Validator

Date: 2026-06-30

## Purpose

Validate the real external staging closure plan from run `595`.

Run `595` reduced the real BEM/FDTD handoff blocker to two real matched-FDTD
input CSVs, two accepted return CSVs, and gate reruns. This run verifies that
the plan has the expected file shape, zero accepted files, blocked downstream
states, and valid artifacts.

## Output

```text
outputs/bem_experiments/596_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan_validator.png
scripts/
```

## Result

```text
checks:                         5
passed checks:                  5
failed checks:                  0
staged files required:          4
real input files required:      2
accepted return files required: 2
present files:                  0
accepted files:                 0
closure groups:                 4
ready groups:                   0
real BEM/FDTD comparison ready: false
GPU/HPC ready:                  false
field transfer ready:           false
field FWI ready:                false
gpu priority:                   none
```

## Interpretation

The closure plan is valid and remains a blocker reducer, not evidence for real
BEM/FDTD agreement.

## Decision

Use run `596` as the validator for run `595`. Keep real BEM/FDTD comparison
blocked until all four staged files are present and accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan_validator.py

3 passed
```

Figure validation:

```text
2285x841, dynamic range=255
```
