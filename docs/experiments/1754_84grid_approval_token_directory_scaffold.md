# Experiment 1754: 84-Grid Approval-Token Directory Scaffold

Date: 2026-06-30

## Purpose

Create or verify the external drop directory required by the 84-grid approval
token branch.

Runs `1751-1753` showed that materialization was blocked by three concrete
items: the external approval-token directory, the real approval fields, and the
external approval-token file. This run resolves only the directory part of that
blocker.

This is CPU-only filesystem preparation and readiness auditing. It does not
create the approval token, fill real approval fields, materialize the 84-grid
case packet, run FDTD, launch GPU work, transfer to field evidence, or promote
3D/HPC work.

## Output

```text
outputs/experiments/1754_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold_scaffold_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source rescan ready:                 true
source validation ready:             true
source sensitivity ready:            true
scaffold paths:                      1
parent directory present after:      1
external approval token present:     0
external approval token nonempty:    0
external approval token accepted:    0
real approval fields missing:        4
complete actions:                    1
materialization ready:               false
new FDTD executed:                   false
GPU work ready:                      false
field transfer ready:                false
3D/HPC ready:                        false
```

The external drop directory is now present:

```text
outputs/experiments/_external_2d_returns/84grid_observed_by_case_pending
```

No approval-token file is present in that directory.

## Interpretation

The directory blocker is closed, but the approval blocker is not closed. The
branch still needs four real approval fields and one real approval-token file
before any materialization can start.

## Decision

Use the scaffolded directory only as the drop location for the real approval
token. Keep materialization, FDTD execution, GPU work, field transfer, and
3D/HPC blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold.py
3 passed
```

Figure check:

```text
2536x850, dynamic range=255
```
