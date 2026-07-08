# BEM Project-FDTD Citation-Map Checkpoint

Date: 2026-07-01

## Scope

This checkpoint records the full-artifact citation-map branch for duplicated
project-FDTD BEM ids, plus the generated-checkpoint refresh that freezes it.

## Output

```text
outputs/bem_experiments/927_scarep_2d_cpu_bem_panel116_project_fdtd_tail_full_artifact_citation_map
outputs/bem_experiments/928_scarep_2d_cpu_bem_panel116_project_fdtd_tail_full_artifact_citation_map_validator
outputs/bem_experiments/929_scarep_2d_cpu_bem_panel116_project_fdtd_tail_full_artifact_citation_map_validation_sensitivity
outputs/_generated_checkpoints/snapshot_audits/318_result_milestone_snapshot_audit_bem_project_fdtd_citation_map_tail_refresh
outputs/_generated_checkpoints/cross_track/319_local_bem_field_2d_checkpoint_tail_post_bem_citation_map_rollup
outputs/_generated_checkpoints/snapshot_audits/320_result_milestone_snapshot_audit_checkpoint_tail_post_bem_citation_map_rollup_refresh
```

## Result

```text
citation rows:                       16
duplicate numeric ids:                4
duplicate numeric id set:             915;920;921;924
full-name required rows:             16
numeric-only references allowed:      0
validator checks passed:              6/6
sensitivity scenarios:                22
damaged scenarios rejected:           21/21
snapshot 318 milestones passed:       3/3
snapshot 318 SHA matches:             6/6
checkpoint 319 milestones ready:      44/44
checkpoint 319 promotions:            0
snapshot 320 milestones passed:       1/1
snapshot 320 SHA matches:             2/2
project FDTD executed now:            false
real BEM/FDTD comparison ready:       false
field transfer ready:                 false
ready for 3D HPC:                     false
gpu priority:                         none
```

## Decision

Use runs `927-929` as the guarded citation-map block for duplicated ids `915`,
`920`, `921`, and `924`. Use runs `318-320` as the generated-checkpoint freeze
for that block. Numeric-only citations remain blocked, and no FDTD execution,
return-value, comparison, field-transfer, GPU, or 3D claim is promoted.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_tail_full_artifact_citation_map.py
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_tail_full_artifact_citation_map_validator.py
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_tail_full_artifact_citation_map_validation_sensitivity.py
11 passed

tests/test_result_milestone_snapshot_audit_bem_project_fdtd_citation_map_tail_refresh.py
tests/test_local_bem_field_2d_checkpoint_tail_post_bem_citation_map_rollup.py
tests/test_result_milestone_snapshot_audit_checkpoint_tail_post_bem_citation_map_rollup_refresh.py
9 passed
```

Figure checks:

```text
927 citation map: 2500x858, dynamic range=255
928 validator: 2537x858, dynamic range=255
929 sensitivity: 3257x891, dynamic range=255
318 snapshot audit: 1672x738, dynamic range=255
319 checkpoint rollup: 1672x738, dynamic range=255
320 rollup snapshot audit: 1276x666, dynamic range=255
```

## Marathon State

The requested 30-hour autonomous marathon is still active. This checkpoint is
not a stop condition. Continue with the next bounded BEM/field/2D evidence,
report, or tooling branch while preserving blocked compute and claim gates.
