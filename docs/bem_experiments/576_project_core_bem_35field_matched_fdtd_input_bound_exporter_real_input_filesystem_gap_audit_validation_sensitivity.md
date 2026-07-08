# BEM Experiment 576: Matched-FDTD Input-Bound Exporter Real Input Filesystem Gap Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `575` validator with controlled damage to the run `574`
filesystem-gap artifacts.

This run checks that the validator fails when path shape, directory/file
presence, blocking counts, downstream readiness, action readiness, figure paths,
or script snapshots are damaged.

## Output

```text
outputs/bem_experiments/576_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_validation_sensitivity_cases.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:              true
sensitivity cases:                   10
expected pass cases:                 1
expected fail cases:                 9
actual pass cases:                   1
actual fail cases:                   9
unexpected cases:                    0
damaged cases:                       9
ready for exporter execution:        false
ready for real BEM/FDTD comparison:  false
ready for 3D validation claim:       false
ready for GPU/HPC:                  false
ready for field transfer:            false
ready for field FWI:                 false
```

The exact source state passes. Damaged states fail for:

```text
source readiness removal
filesystem path removal
parent-directory promotion
file-presence promotion
blocking-count drift
BEM/FDTD comparison promotion
action-readiness promotion
missing figure
missing script snapshots
```

## Interpretation

The filesystem-gap validator is sensitive to the intended failure modes. It
does not allow missing or damaged handoff paths to become exporter-ready or
comparison-ready evidence.

## Decision

Keep exporter execution and BEM/FDTD comparison blocked until the locked real
input CSV files exist and pass the run `571` acceptance gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_validation_sensitivity.py

3 passed
```

Filesystem-gap slice:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_validator.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_validation_sensitivity.py

9 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
