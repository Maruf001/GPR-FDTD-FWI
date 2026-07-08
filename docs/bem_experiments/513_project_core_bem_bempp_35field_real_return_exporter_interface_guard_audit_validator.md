# BEM Experiment 513: Bempp 35-Field Real-Return Exporter Interface Guard Audit Validator

Date: 2026-06-30

## Purpose

Validate run `512`, the guarded Bempp-side exporter-interface audit for the
35-field real-return files.

Run `512` added a Bempp exporter interface that checks the saved return-file
contract but refuses evidence-producing export. This validator confirms that
the saved audit rows preserve that boundary.

## Output

```text
outputs/bem_experiments/513_project_core_bem_bempp_35field_real_return_exporter_interface_guard_audit_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_35field_real_return_exporter_interface_guard_audit_validator_checks.csv
data/project_core_bem_bempp_35field_real_return_exporter_interface_guard_audit_validator_summary.json
figures/project_core_bem_bempp_35field_real_return_exporter_interface_guard_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation checks passed:                  5
blocking failures:                         0
Bempp exporter-interface validation ready: true
audit cases:                               5
Bempp return-file keys:                    2
remaining real-return blockers:            3
real Bempp export enabled:                 false
real return values exported:               false
accepted return file written:              false
real return production ready:              false
real BEM/FDTD comparison ready:            false
3D validation ready:                       false
GPU/HPC ready:                             false
field FWI ready:                           false
GPU priority:                              none
```

The validator confirms that both Bempp return-file keys remain
contract-checkable, FDTD-side keys are rejected, unknown keys are rejected, real
Bempp export requests are refused, no evidence is written, and all downstream
states remain blocked.

## Decision

Use run `513` as the artifact guard for run `512`. The BEM branch now has a
guarded Bempp exporter interface and a guarded writer interface, but still
needs real Bempp values, the FDTD exporter, and a later evidence-producing
writer path before real return production can proceed.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_35field_real_return_exporter.py
tests/test_project_core_bem_bempp_35field_real_return_exporter_interface_guard_audit.py
tests/test_project_core_bem_bempp_35field_real_return_exporter_interface_guard_audit_validator.py
13 passed
```

Figure check:

```text
2177x832, dynamic range=255
```
