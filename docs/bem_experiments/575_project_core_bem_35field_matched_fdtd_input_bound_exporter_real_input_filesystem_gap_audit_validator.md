# BEM Experiment 575: Matched-FDTD Input-Bound Exporter Real Input Filesystem Gap Audit Validator

Date: 2026-06-30

## Purpose

Validate run `574` from saved artifacts.

This run confirms that the locked real input and accepted-return paths are
absent and that exporter execution and BEM/FDTD comparison remain blocked.

## Output

```text
outputs/bem_experiments/575_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_validator.png
scripts/
```

## Result

```text
source audit ready:                    true
validation checks:                     5
failed checks:                         0
required real input files:             2
required accepted return files:        2
filesystem paths checked:              4
parent directories present:            0
files present:                         0
blocking paths:                        4
ready for exporter execution:          false
ready for real BEM/FDTD comparison:    false
ready for 3D validation claim:         false
ready for GPU/HPC:                     false
ready for field transfer:              false
ready for field FWI:                   false
```

The five checks validate source readiness, four-path shape, absent parent
directories/files, blocked actions/downstream states, and figure/script
artifacts.

## Interpretation

Run `574` is a valid filesystem-gap audit. The next BEM/FDTD handoff blocker is
not ambiguous: the locked real input and accepted-return paths are still empty.

## Decision

Do not run the input-bound exporter or any BEM/FDTD comparison until the two
real matched-FDTD input CSV files exist at the locked paths and pass the run
`571` acceptance gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_validator.py

6 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
