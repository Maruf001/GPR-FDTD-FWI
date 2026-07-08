# BEM Experiment 926: Panel-116 Project-FDTD Tail Numbering Collision Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `925` numbering-collision validator by damaging the saved
run `924` collision policy in controlled ways.

The sensitivity set mutates audit readiness, duplicate id counts, duplicate id
sets, duplicate rows, numeric-only reference policy, policy rows, launch state,
execution flags, return rows, return values, comparison flags, downstream
promotion, figure metadata, and script snapshots.

## Output

```text
outputs/bem_experiments/926_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit_validation_sensitivity
```

## Result

```text
source validator ready:               true
scenarios:                            19
expected passes:                       1
expected failures:                    18
observed passes:                       1
observed failures:                    18
unexpected outcomes:                   0
damaged scenarios:                    18
damaged scenarios rejected:           18
project FDTD launch packet written: true
project FDTD execution authorized:  false
project FDTD return rows present:   false
project FDTD return values present: false
project FDTD comparison completed:  false
field transfer ready:                false
real 3D validation ready:            false
gpu priority:                        none
```

## Decision

Use runs `924-926` as the guarded numbering-collision policy block.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit_validation_sensitivity.py
3 passed
```

Figure check:

```text
outputs/bem_experiments/926_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit_validation_sensitivity/figures/scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit_validation_sensitivity.png
width: 3185
height: 885
dynamic range: 255
```
