# Experiment 1570: Post Command-Replay Claim Boundary

Date: 2026-06-29

## Purpose

Fold the executed aggregate CPU replay from runs `1567-1569` into the current
local 2D claim boundary.

This run confirms that the saved follow-up probe can be replayed as one
aggregate CPU command. It does not create a per-objective command interface,
promote a physical acquisition claim, launch GPU work, transfer to field data,
run field FWI, or run 3D/HPC work.

## Output

```text
outputs/experiments/1570_local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary.png
```

## Result

```text
claims:                            25
guarded claims:                    22
blocked claims:                    3
base claims:                       24
base guarded claims:               21
base blocked claims:               3
aggregate replay executed:         true
replay audit ready:                true
replay sensitivity ready:          true
per-objective CLI available:       false
grid models:                       20
objective rows:                    120
candidate rows:                    480
any-failure models:                20
all-objective-failure models:      0
local generalization boundary:     true
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The claim boundary now has one additional guarded row for the executed
aggregate replay. The replay confirms reproducibility of the saved follow-up
probe but does not justify broader physical, GPU, field, or 3D claims.

## Decision

Use this as the current 2D claim boundary after the command replay block. Keep
physical, GPU, field-transfer, field-FWI, and 3D/HPC claims blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary.py
4 passed as part of the 12-test focused set
```

Figure check:

```text
3941x906, dynamic range=255
```
