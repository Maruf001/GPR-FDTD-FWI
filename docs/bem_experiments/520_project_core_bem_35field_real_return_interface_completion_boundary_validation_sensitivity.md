# BEM Experiment 520: 35-Field Real-Return Interface Completion Boundary Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `519` validator for the run `518` real-return interface
completion boundary.

Run `519` validated that guarded contract checks exist while real values and
accepted evidence remain absent. This run verifies that the validator rejects
fake real-value readiness, fake accepted-evidence readiness, count drift,
implementation-action drift, downstream promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/bem_experiments/520_project_core_bem_35field_real_return_interface_completion_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_real_return_interface_completion_boundary_validation_sensitivity_rows.csv
data/project_core_bem_35field_real_return_interface_completion_boundary_validation_sensitivity_summary.json
figures/project_core_bem_35field_real_return_interface_completion_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                         11
expected pass scenarios:                       1
expected failure scenarios:                    10
unexpected scenarios:                          0
interface-boundary sensitivity ready:          true
exact source artifacts pass:                   true
real-value promotion rejected:                 true
accepted-evidence promotion rejected:          true
real return production ready:                  false
real BEM/FDTD comparison ready:                false
3D validation ready:                           false
GPU/HPC ready:                                 false
field FWI ready:                               false
GPU priority:                                  none
```

The exact run `518` artifacts pass. Damaged variants fail as expected for
guarded-interface count drift, fake real-value readiness, fake accepted-evidence
readiness, required-count drift, action-order damage, early evidence permission,
blocker-count drift, downstream comparison promotion, figure damage, and
script-snapshot damage.

## Decision

Use runs `518-520` as the guarded 35-field real-return interface-completion
boundary block. All contract-check interfaces are now guarded, but no real
return values or accepted evidence files exist.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_real_return_interface_completion_boundary.py
tests/test_project_core_bem_35field_real_return_interface_completion_boundary_validator.py
tests/test_project_core_bem_35field_real_return_interface_completion_boundary_validation_sensitivity.py
12 passed
```

Figure check:

```text
2537x868, dynamic range=255
```
