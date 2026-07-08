# Experiment 1435: Local 2D Objective Revision Holdout Audit

Date: 2026-06-28

## Purpose

Check the run `1434` candidate objective-revision policies against the saved
run `1428` expanded-window radius bracket.

This run uses saved result tables only. It does not execute new FDTD
simulations, launch GPU work, transfer to field data, run field FWI, or promote
3D/HPC work.

## Output

```text
outputs/experiments/1435_local_2d_state_consistent_objective_revision_holdout_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_holdout_objective_rows.csv
data/local_2d_state_consistent_objective_revision_holdout_policy_rows.csv
data/local_2d_state_consistent_objective_revision_holdout_design_rows.csv
data/local_2d_state_consistent_objective_revision_holdout_audit_summary.json
figures/local_2d_state_consistent_objective_revision_holdout_audit.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_HOLDOUT_AUDIT.md
scripts/run_local_2d_state_consistent_objective_revision_holdout_audit.py
scripts/test_local_2d_state_consistent_objective_revision_holdout_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
holdout perturbations:              10
objective selection rows:           60
objectives per case:                6
veryhigh failure count:             2
non-veryhigh failure count:         0
policies recovering all holdouts:   drop_veryhigh_all_remaining;majority_vote_all_objectives
drop-veryhigh holdout supported:    true
majority-vote holdout supported:    true
saved holdout support ready:        true
prospective validation required:    true
promote revised objective now:      false
broad radius tolerance promoted:    false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The saved expanded-window bracket supports both drop-`veryhigh` and
majority-vote candidate policies across all ten holdout perturbations,
including the deeper far-radius failure, but this remains saved-data support
rather than a prospective validation.

## Decision

Use run `1435` to justify a prospective objective-revision validation sweep. Do
not promote the revised objective, broad-radius tolerance, physical transfer,
GPU work, field transfer, field FWI, or 3D/HPC from saved holdout evidence
alone.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_holdout_audit.py
4 passed
```

Figure validation:

```text
3258x902, dynamic range=255
```
