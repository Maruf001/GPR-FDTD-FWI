# BEM Experiment 517: FDTD 35-Field Real-Return Exporter Interface Guard Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `516` validator for the run `515` guarded FDTD exporter
interface audit.

Run `516` validated that the FDTD exporter interface checks the saved contract
but does not produce accepted evidence. This run verifies that the validator
rejects missing audit rows, fake real-export output, accepted-file promotion,
hidden evidence flags, blocker drift, downstream promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/bem_experiments/517_project_core_bem_fdtd_35field_real_return_exporter_interface_guard_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_fdtd_35field_real_return_exporter_interface_guard_audit_validation_sensitivity_rows.csv
data/project_core_bem_fdtd_35field_real_return_exporter_interface_guard_audit_validation_sensitivity_summary.json
figures/project_core_bem_fdtd_35field_real_return_exporter_interface_guard_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                         10
expected pass scenarios:                       1
expected failure scenarios:                    9
unexpected scenarios:                          0
FDTD exporter validation sensitivity ready:    true
exact source artifacts pass:                   true
real export promotion rejected:                true
accepted-file promotion rejected:              true
real return production ready:                  false
real BEM/FDTD comparison ready:                false
3D validation ready:                           false
GPU/HPC ready:                                 false
field FWI ready:                               false
GPU priority:                                  none
```

The exact run `515` artifacts pass. Damaged variants fail as expected for audit
case-count drift, a missing FDTD contract-key row, fake real export, accepted
file promotion, hidden evidence readiness, blocker-count drift, downstream
comparison promotion, figure damage, and script-snapshot damage.

## Decision

Use runs `515-517` as the guarded FDTD real-return exporter-interface block.
The BEM branch now has guarded interfaces for the FDTD exporter, the Bempp
exporter, and the return-file writer, but real return production still requires
real returned values and a later evidence-producing writer path.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fdtd_35field_real_return_exporter.py
tests/test_project_core_bem_fdtd_35field_real_return_exporter_interface_guard_audit.py
tests/test_project_core_bem_fdtd_35field_real_return_exporter_interface_guard_audit_validator.py
tests/test_project_core_bem_fdtd_35field_real_return_exporter_interface_guard_audit_validation_sensitivity.py
16 passed
```

Figure check:

```text
2393x860, dynamic range=255
```
