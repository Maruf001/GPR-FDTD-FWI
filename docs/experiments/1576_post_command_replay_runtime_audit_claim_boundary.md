# Experiment 1576: Post Command-Replay Runtime-Audit Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded run `1573-1575` runtime-audit result into the current local
2D claim boundary.

## Output

```text
outputs/experiments/1576_local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary.png
```

## Result

```text
claims:                            26
guarded claims:                    23
blocked claims:                    3
aggregate replay executed:         true
runtime audit ready:               true
runtime sensitivity ready:         true
grid models:                       20
objective rows:                    120
candidate rows:                    480
any-failure models:                20
all-objective-failure models:      0
elapsed seconds:                   782.566
elapsed minutes:                   13.0428
seconds per grid model:            39.1283
seconds per objective row:         6.52138
seconds per candidate row:         1.63035
grid models per minute:            1.53342
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The new guarded claim records the aggregate replay runtime cost. It does not
promote physical, GPU, field-transfer, field-FWI, or 3D/HPC readiness.

## Decision

Use this as the current 2D claim boundary after the runtime-audit block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary.py
4 passed as part of the 12-test focused set
```

Figure check:

```text
3941x906, dynamic range=255
```
