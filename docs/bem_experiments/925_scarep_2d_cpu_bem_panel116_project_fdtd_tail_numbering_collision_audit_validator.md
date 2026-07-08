# BEM Experiment 925: Panel-116 Project-FDTD Tail Numbering Collision Audit Validator

Date: 2026-07-01

## Purpose

Validate the saved run `924` numbering-collision audit.

The validator checks the duplicated id set, numeric-only reference block,
policy rows, blocked execution/return/downstream state, figure output, and
script snapshots.

## Output

```text
outputs/bem_experiments/925_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit_validator
```

## Result

```text
validation checks:                    6
checks passed:                        6
checks failed:                        0
duplicate rows:                       8
duplicate numeric ids:                4
duplicate numeric id set:             915;920;921;924
numeric-only references allowed:      0
policy rows:                          4
project FDTD launch packet written: true
project FDTD executed:              false
project FDTD return rows present:   false
project FDTD return values present: false
project FDTD comparison completed:  false
field transfer ready:                false
real 3D validation ready:            false
gpu priority:                        none
```

Validation checks:

| Check | Passed |
| --- | --- |
| audit_identity_and_readiness | true |
| duplicate_id_set_stable | true |
| numeric_only_references_blocked | true |
| policy_rows_stable | true |
| execution_return_and_downstream_blocked | true |
| figure_and_scripts_valid | true |

## Decision

Use full artifact names or paths for ids `915`, `920`, `921`, and `924`.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit_validator.py
4 passed
```

Figure check:

```text
outputs/bem_experiments/925_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit_validator/figures/scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit_validator.png
width: 2537
height: 862
dynamic range: 255
```
