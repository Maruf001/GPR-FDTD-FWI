# BEM Experiment 921: Panel-116 Project-FDTD Packet/Template Reconciliation Audit Validator

Date: 2026-07-01

## Purpose

Validate the saved run `920` packet/template reconciliation audit.

The validator checks reconciliation readiness, packet/template counts,
reconciliation rows, duplicated-run-id handling, blocked execution/return
states, figure output, and script snapshots.

## Output

```text
outputs/bem_experiments/921_scarep_2d_cpu_bem_panel116_project_fdtd_packet_template_reconciliation_audit_validator
```

## Result

```text
validation checks:                       6
checks passed:                           6
checks failed:                           0
packet frequency slots:                 25
packet return schema columns:           15
template receivers:                     13
template frequencies:                   25
template rows:                         325
duplicate run id present:              true
duplicate id resolved by names:        true
combined handoff ready:                true
project FDTD launch packet written:    true
project FDTD executed:                 false
project FDTD return rows present:      false
project FDTD return values present:    false
project FDTD comparison completed:     false
field transfer ready:                  false
real 3D validation ready:              false
gpu priority:                          none
```

Validation checks:

| Check | Passed |
| --- | --- |
| reconciliation_identity_and_readiness | true |
| packet_and_template_counts_stable | true |
| reconciliation_rows_stable | true |
| duplicate_run_id_boundary_explicit | true |
| execution_return_and_downstream_blocked | true |
| figure_and_scripts_valid | true |

## Interpretation

The packet/template reconciliation validates as a combined non-evidence handoff
boundary.

## Decision

Use run `920` as the current packet/template relationship audit.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_packet_template_reconciliation_audit_validator.py
4 passed
```

Figure check:

```text
3311x893, dynamic range=255
```
