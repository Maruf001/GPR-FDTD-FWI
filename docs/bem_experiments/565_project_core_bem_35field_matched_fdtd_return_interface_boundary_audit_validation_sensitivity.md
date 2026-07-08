# BEM Experiment 565: Matched-FDTD Return Interface Boundary Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Sensitivity-test the run `564` BEM/FDTD return-file interface boundary audit.

Run `564` showed that the BEM-side return files are accepted and the
matched-FDTD side still has only blank validated templates. This run checks
that the audit rejects common damaged states rather than silently promoting a
comparison.

This run does not create FDTD return files, execute commands, run a BEM/FDTD
comparison, launch GPU/HPC work, transfer to field evidence, or promote 3D
validation readiness.

## Output

```text
outputs/bem_experiments/565_project_core_bem_35field_matched_fdtd_return_interface_boundary_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_interface_boundary_audit_validation_sensitivity_cases.csv
data/project_core_bem_35field_matched_fdtd_return_interface_boundary_audit_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_interface_boundary_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source audit ready:                    true
sensitivity cases:                     8
expected pass cases:                   1
expected fail cases:                   7
actual pass cases:                     1
actual fail cases:                     7
unexpected cases:                      0
damaged cases:                         7
BEM/FDTD comparison ready:             false
3D validation ready:                   false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
sensitivity ready:                     true
```

Damaged cases rejected:

| Case | Damage |
| --- | --- |
| BEM validation ready false | BEM-side validator readiness false |
| BEM row count drift | accepted BEM row count drifts from 558 |
| FDTD template ready false | matched-FDTD template readiness false |
| FDTD blank value count drift | blank matched-FDTD value count drifts from 558 |
| FDTD file promotion | matched-FDTD return file accepted without source files |
| command execution promotion | matched-FDTD command marked executed |
| downstream promotion | premature BEM/FDTD comparison promotion |

## Interpretation

The run `564` boundary audit is sensitive to the key failure modes that matter
for the current comparison gate. It rejects damaged BEM-side validation, FDTD
template damage, premature FDTD-file acceptance, command-execution promotion,
and downstream comparison promotion.

## Decision

Use runs `564` and `565` as the guarded BEM/FDTD interface-boundary block. The
next comparison-enabling work remains producing and accepting the two real
matched-FDTD return CSV files.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_interface_boundary_audit_validation_sensitivity.py
4 passed
```

Figure check:

```text
1709x847, dynamic range=255
```
