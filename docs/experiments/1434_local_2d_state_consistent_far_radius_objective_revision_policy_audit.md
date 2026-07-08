# Experiment 1434: Local 2D Far-Radius Objective Revision Policy Audit

Date: 2026-06-28

## Purpose

Audit candidate objective-revision policies for the run `1430` far-radius
`veryhigh` failures.

This run uses saved result tables only. It does not execute new FDTD
simulations, launch GPU work, transfer to field data, run field FWI, or promote
3D/HPC work.

## Output

```text
outputs/experiments/1434_local_2d_state_consistent_far_radius_objective_revision_policy_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_far_radius_objective_selection_rows.csv
data/local_2d_state_consistent_far_radius_objective_revision_policy_rows.csv
data/local_2d_state_consistent_far_radius_objective_revision_design_rows.csv
data/local_2d_state_consistent_far_radius_objective_revision_policy_audit_summary.json
figures/local_2d_state_consistent_far_radius_objective_revision_policy_audit.png
docs/LOCAL_2D_STATE_CONSISTENT_FAR_RADIUS_OBJECTIVE_REVISION_POLICY_AUDIT.md
scripts/run_local_2d_state_consistent_far_radius_objective_revision_policy_audit.py
scripts/test_local_2d_state_consistent_far_radius_objective_revision_policy_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
failed far-radius cases:              5
objective selection rows:             30
objectives per case:                  6
veryhigh failure count:               5
non-veryhigh failure count:           0
candidate policies:                   4
policy rows:                          20
policies recovering all failed cases: drop_veryhigh_all_remaining;majority_vote_all_objectives
objective revision candidate ready:   true
independent validation required:      true
promote revised objective now:        false
broad radius tolerance promoted:      false
physical claim ready:                 false
GPU work ready:                       false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
```

The far-radius failures are isolated to `veryhigh`. Dropping `veryhigh` or
using a majority vote recovers truth on the saved failed cases, but this is a
candidate repair that still needs independent validation.

## Decision

Use run `1434` to define the next 2D objective-revision branch: validate
drop-`veryhigh` and majority-vote policies on an independent
perturbation/objective sweep before promoting any revised objective.

Broad radius, physical, GPU, field-transfer, field-FWI, and 3D/HPC claims remain
blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_far_radius_objective_revision_policy_audit.py
5 passed
```

Figure validation:

```text
3222x878, dynamic range=255
```
