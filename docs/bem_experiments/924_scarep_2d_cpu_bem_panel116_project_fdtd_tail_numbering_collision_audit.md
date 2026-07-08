# BEM Experiment 924: Panel-116 Project-FDTD Tail Numbering Collision Audit

Date: 2026-07-01

## Purpose

Audit duplicated numeric BEM run ids in the project-FDTD packet/template tail.

This run exists because several artifacts now share numeric ids while retaining
distinct full names and paths. Numeric-only references are unsafe for this
tail.

## Output

```text
outputs/bem_experiments/924_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit
```

## Result

```text
duplicate rows:                       8
duplicate numeric ids:                4
duplicate numeric id set:             915;920;921;924
output duplicate id rows:             4
doc duplicate id rows:                4
duplicate artifact references:       16
numeric-only references allowed:      0
policy rows:                          4
passed policy rows:                   4
failed policy rows:                   0
project FDTD launch packet written: true
project FDTD executed:              false
project FDTD return rows present:   false
project FDTD return values present: false
project FDTD comparison completed:  false
field transfer ready:                false
real 3D validation ready:            false
gpu priority:                        none
```

Duplicated numeric ids:

```text
915, 920, 921, 924
```

## Interpretation

Numeric-only citations are ambiguous for ids `915`, `920`, `921`, and `924`.
References in this tail must include the full artifact name or path.

This audit changes reference policy only. It does not promote FDTD execution,
return values, BEM/FDTD comparison, field transfer, GPU priority, or 3D
validation.

## Decision

Do not cite ids `915`, `920`, `921`, or `924` without full artifact names or
paths in this tail.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit.py
4 passed
```

Figure check:

```text
outputs/bem_experiments/924_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit/figures/scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit.png
width: 2410
height: 808
dynamic range: 255
```
