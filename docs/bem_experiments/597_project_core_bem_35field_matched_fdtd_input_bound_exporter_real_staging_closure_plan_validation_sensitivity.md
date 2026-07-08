# BEM Experiment 597: Matched FDTD Input-Bound Exporter Real Staging Closure Plan Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the validator from run `596`.

This run checks that the validator accepts the exact run `595` closure plan and
rejects damaged states that would falsely change the file obligations, promote
file acceptance, promote real comparison, or damage artifacts.

## Output

```text
outputs/bem_experiments/597_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan_validation_sensitivity_cases.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:         true
cases:                          13
expected pass cases:            1
expected fail cases:            12
actual pass cases:              1
actual fail cases:              12
unexpected outcomes:            0
damaged cases:                  12
real BEM/FDTD comparison ready: false
GPU/HPC ready:                  false
field transfer ready:           false
field FWI ready:                false
gpu priority:                   none
```

The damaged states cover source readiness removal, closure-group damage,
missing-file row damage, file-role damage, file-presence promotion, file
acceptance promotion, group-readiness promotion, real-comparison promotion,
GPU/HPC promotion, figure damage, and script-snapshot damage.

## Interpretation

The closure-plan validator is sensitive to the failure modes that would matter
before allowing real BEM/FDTD comparison.

## Decision

Use runs `595-597` as the current closed BEM/FDTD handoff closure block. Keep
real BEM/FDTD comparison blocked until all four staged files are accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
