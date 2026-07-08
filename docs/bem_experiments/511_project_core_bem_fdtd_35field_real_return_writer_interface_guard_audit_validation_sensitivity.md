# BEM Experiment 511: BEM/FDTD 35-Field Real-Return Writer Interface Guard Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `510` validator for the run `509` guarded return-file
writer-interface audit.

Run `510` validated that the writer interface checks the saved contract but
does not produce accepted evidence. This run verifies that the validator rejects
missing audit rows, hidden evidence writes, blocker drift, downstream
promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/511_project_core_bem_fdtd_35field_real_return_writer_interface_guard_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_fdtd_35field_real_return_writer_interface_guard_audit_validation_sensitivity_rows.csv
data/project_core_bem_fdtd_35field_real_return_writer_interface_guard_audit_validation_sensitivity_summary.json
figures/project_core_bem_fdtd_35field_real_return_writer_interface_guard_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     9
expected pass scenarios:                   1
expected failure scenarios:                8
unexpected scenarios:                      0
writer-interface validation sensitivity:   true
exact source artifacts pass:               true
evidence promotion rejected:               true
real return production ready:              false
real BEM/FDTD comparison ready:            false
3D validation ready:                       false
GPU/HPC ready:                             false
field FWI ready:                           false
GPU priority:                              none
```

The exact run `509` artifacts pass. Damaged variants fail as expected for audit
case-count drift, a missing contract-key row, accepted-file promotion, hidden
evidence readiness, blocker-count drift, downstream comparison promotion,
figure damage, and script-snapshot damage.

## Decision

Use runs `509-511` as the guarded return-file writer-interface block. The
writer interface is useful for contract checks, but real return production still
requires BEM/FDTD exporters and a later real-write implementation with real
values and provenance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fdtd_35field_real_return_files_writer.py
tests/test_project_core_bem_fdtd_35field_real_return_writer_interface_guard_audit.py
tests/test_project_core_bem_fdtd_35field_real_return_writer_interface_guard_audit_validator.py
tests/test_project_core_bem_fdtd_35field_real_return_writer_interface_guard_audit_validation_sensitivity.py
15 passed
```

Figure check:

```text
2393x857, dynamic range=255
```
