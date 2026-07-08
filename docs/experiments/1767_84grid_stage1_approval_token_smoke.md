# Experiment 1767: 84-Grid Stage-1 Approval-Token Smoke

Date: 2026-07-01

## Purpose

Exercise stage 1 of the 84-grid staged return packet from run `1766` with an
output-local synthetic approval-token fill.

This run does not create a real external approval token, materialize
observed-by-case data, run FDTD, launch GPU work, transfer to field evidence,
or start 3D/HPC work.

## Output

```text
outputs/experiments/1767_local_2d_state_consistent_objective_revision_84grid_stage1_approval_token_smoke
```

Key artifacts:

```text
data/stage_one_synthetic_approval_token/
data/local_2d_state_consistent_objective_revision_84grid_stage1_approval_token_smoke_field_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_stage1_approval_token_smoke_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_stage1_approval_token_smoke.png
scripts/script_snapshot_manifest.json
```

## Result

```text
context fields:                      8
context values present:              8
approval fields required:            4
approval values present:             4
blank approval fields:               0
external approval token present:     false
synthetic accepted as external:      false
full external return items:          21
missing external return items:       21
materialization ready:               false
new FDTD executed:                   false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The approval-token schema can be filled locally: the four approval fields and
eight context fields are present in the output-local synthetic token.

This does not close the real approval gate. The real external approval token is
still absent, and all twenty materialization artifacts are still absent.

## Decision

Use this as stage-1 approval mechanics coverage only. Keep materialization,
FDTD execution, GPU work, field transfer, field FWI, and 3D/HPC blocked until
the real external approval token and all artifact files are present.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_stage1_approval_token_smoke.py
3 passed
```

Figure check:

```text
1672x808, dynamic range=255
```
