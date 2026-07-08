# Experiment 1768: 84-Grid Stage-1 Live Approval Contract

Date: 2026-07-01

## Purpose

Define the exact live approval-token file that must replace the stage-1
synthetic approval smoke from run `1767`.

This run does not create a real external approval token, materialize
observed-by-case data, run FDTD, launch GPU work, transfer to field evidence,
or start 3D/HPC work.

## Output

```text
outputs/experiments/1768_local_2d_state_consistent_objective_revision_84grid_stage1_live_approval_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_stage1_live_approval_contract_contract_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_stage1_live_approval_contract_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_stage1_live_approval_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
contract rows:                      1
required approval fields:           4
context fields:                     8
live parent directory present:      1
live approval token present:        0
accepted external approvals:        0
full external return items:         21
missing external return items:      21
materialization ready:              false
new FDTD executed:                  false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

Expected live approval token:

```text
outputs/experiments/_external_2d_returns/84grid_observed_by_case_pending/APPROVED_1691_OBSERVED_BY_CASE_EXECUTION.json
```

Required approval fields:

```text
approval_id
approval_created_at_utc
approved_by
approval_reason
```

## Interpretation

The first 2D return-stage replacement is now exact: one external JSON token
with four real approval fields. The parent directory exists, but the live
approval token is not present yet.

## Decision

Use this as the live approval-token contract. Keep materialization, FDTD
execution, GPU work, field transfer, field FWI, and 3D/HPC blocked until the
real token and all artifact files are present.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_stage1_live_approval_contract.py
3 passed
```

Figure check:

```text
1816x826, dynamic range=255
```
