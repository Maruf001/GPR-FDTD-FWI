# BEM Experiment 922: Panel-116 Project-FDTD Packet/Template Reconciliation Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `921` reconciliation validator by damaging the saved run
`920` packet/template relationship in controlled ways.

The sensitivity set mutates reconciliation readiness, packet/template
readiness, packet frequency counts, schema counts, template row counts,
duplicated-run-id resolution, reconciliation rows, launch-packet state,
execution flags, return rows, return values, comparison flags, downstream
promotion, figure metadata, and script snapshots.

## Output

```text
outputs/bem_experiments/922_scarep_2d_cpu_bem_panel116_project_fdtd_packet_template_reconciliation_audit_validation_sensitivity
```

## Result

```text
source validator ready:               true
scenarios:                            22
expected passes:                       1
expected failures:                    21
observed passes:                       1
observed failures:                    21
unexpected outcomes:                   0
damaged scenarios:                    21
damaged scenarios rejected:           21
project FDTD launch packet written: true
project FDTD execution authorized:  false
project FDTD return rows present:   false
project FDTD return values present: false
project FDTD comparison completed:  false
field transfer ready:                false
real 3D validation ready:            false
gpu priority:                        none
```

## Interpretation

The reconciliation validator accepts only the exact combined packet/template
state. It rejects damaged counts, damaged reconciliation rows, unresolved
duplicated-run-id state, false return values, false comparison completion, and
downstream promotion.

## Decision

Use runs `920-922` as the guarded packet/template reconciliation block.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_packet_template_reconciliation_audit_validation_sensitivity.py
3 passed
```

Figure check:

```text
3293x888, dynamic range=255
```
