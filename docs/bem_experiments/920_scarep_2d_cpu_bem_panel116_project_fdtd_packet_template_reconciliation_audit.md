# BEM Experiment 920: Panel-116 Project-FDTD Packet/Template Reconciliation Audit

Date: 2026-07-01

## Purpose

Reconcile the panel-116 project-FDTD launch/return packet with the separate
row-level return packet template.

The stream currently has two run-`915` artifacts with distinct names:

```text
outputs/bem_experiments/915_scarep_2d_cpu_bem_panel116_continuous_shift_project_fdtd_launch_return_packet
outputs/bem_experiments/915_scarep_2d_cpu_bem_panel116_project_fdtd_return_packet_template
```

This audit makes their relationship explicit and keeps both artifacts
non-evidence.

## Output

```text
outputs/bem_experiments/920_scarep_2d_cpu_bem_panel116_project_fdtd_packet_template_reconciliation_audit
```

## Result

```text
packet ready:                           true
template ready:                         true
reconciliation checks:                   6
passed reconciliation checks:            6
failed reconciliation checks:            0
packet frequency slots:                 25
packet high-band frequency slots:        9
packet return schema columns:           15
template receivers:                     13
template frequencies:                   25
template rows:                         325
template blank value columns:            6
template blank value cells:           1950
receiver rows per frequency min:        13
receiver rows per frequency max:        13
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

## Interpretation

The launch/return packet and row-level return template are complementary. The
packet defines handoff metadata, packet files, frequency slots, and the required
return schema. The template expands those frequency slots into 325 fillable
receiver-frequency rows.

The duplicated numeric run id is an audit risk, but the distinct run names and
paths keep the artifacts separable.

## Decision

Use the launch/return packet for packet-level handoff and the row template for
receiver-frequency fillable rows. Real-return intake remains required before
comparison claims.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_packet_template_reconciliation_audit.py
4 passed
```

Figure check:

```text
3365x888, dynamic range=255
```
