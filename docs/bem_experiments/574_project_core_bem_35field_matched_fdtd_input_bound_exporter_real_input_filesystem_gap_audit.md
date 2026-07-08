# BEM Experiment 574: Matched-FDTD Input-Bound Exporter Real Input Filesystem Gap Audit

Date: 2026-06-30

## Purpose

Audit the filesystem state for the real matched-FDTD input and accepted-return
paths defined by run `571`.

This is a read-only audit. It does not create directories, copy files, execute
the exporter, or run a BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/574_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_filesystem_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_action_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit.png
scripts/
```

## Result

```text
source gate ready:                    true
required real input files:            2
required accepted return files:       2
filesystem paths checked:             4
parent directories present:           0
paths present:                        0
files present:                        0
nonempty files:                       0
real input files present:             0
accepted return files present:        0
blocking paths:                       4
ready for exporter execution:         false
ready for real BEM/FDTD comparison:   false
ready for 3D validation claim:        false
ready for GPU/HPC:                    false
ready for field transfer:             false
ready for field FWI:                  false
```

The four locked paths are the two real input CSV files and the two accepted
return CSV files. All four are blocked by missing parent directories and missing
files.

## Interpretation

The BEM/FDTD handoff is not waiting on analysis code at this point. It is
waiting on real matched-FDTD CSV inputs at the locked paths, followed by
exporter execution that writes accepted return CSVs.

## Decision

Do not run the exporter or BEM/FDTD comparison until the two real input CSV
files exist and pass the run `571` acceptance gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate_validator.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate_validation_sensitivity.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_filesystem_gap_audit.py

13 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
