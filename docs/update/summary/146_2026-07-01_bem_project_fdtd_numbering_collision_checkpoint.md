# BEM Project-FDTD Numbering-Collision Checkpoint

Date: 2026-07-01

## Scope

This checkpoint records the post-project-FDTD packet/template numbering-collision
guard and generated-checkpoint refresh.

Numeric ids `915`, `920`, `921`, and `924` are duplicated across distinct BEM
artifacts. Numeric-only references remain blocked; use full artifact names or
paths for this tail.

## Output

```text
outputs/bem_experiments/924_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit
outputs/bem_experiments/925_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit_validator
outputs/bem_experiments/926_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit_validation_sensitivity
outputs/_generated_checkpoints/snapshot_audits/315_result_milestone_snapshot_audit_bem_project_fdtd_numbering_collision_tail_refresh
outputs/_generated_checkpoints/cross_track/316_local_bem_field_2d_checkpoint_tail_post_bem_numbering_collision_rollup
outputs/_generated_checkpoints/snapshot_audits/317_result_milestone_snapshot_audit_checkpoint_tail_post_bem_numbering_collision_rollup_refresh
```

## Result

```text
numbering audit duplicate rows:       8
duplicate numeric ids:                4
duplicate numeric id set:             915;920;921;924
validator checks passed:              6/6
sensitivity scenarios:                19
damaged scenarios rejected:           18/18
snapshot 315 milestones passed:       4/4
snapshot 315 SHA matches:             8/8
checkpoint 316 milestones ready:      43/43
checkpoint 316 promotions:            0
snapshot 317 milestones passed:       1/1
snapshot 317 SHA matches:             2/2
project FDTD executed now:            false
real BEM/FDTD comparison ready:       false
field transfer ready:                 false
ready for 3D HPC:                     false
gpu priority:                         none
```

## Decision

Use the full-name synthetic `924` smoke plus the full-name numbering-collision
`924-926` artifacts as the frozen BEM numbering-collision tail. The policy
changes citation discipline only; it does not promote FDTD execution, return
values, comparison evidence, field transfer, GPU priority, or 3D validation.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit.py
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit_validation_sensitivity.py
11 passed

tests/test_result_milestone_snapshot_audit_bem_project_fdtd_numbering_collision_tail_refresh.py
tests/test_local_bem_field_2d_checkpoint_tail_post_bem_numbering_collision_rollup.py
tests/test_result_milestone_snapshot_audit_checkpoint_tail_post_bem_numbering_collision_rollup_refresh.py
9 passed
```

Figure checks:

```text
315 snapshot audit: 1672x738, dynamic range=255
316 checkpoint rollup: 1672x738, dynamic range=255
317 rollup snapshot audit: 1276x666, dynamic range=255
```

## Marathon State

The requested 30-hour autonomous marathon is still active. This checkpoint is
not a stop condition. Continue with the next bounded BEM/field/2D evidence or
tooling branch while preserving the blocked compute and claim gates.
