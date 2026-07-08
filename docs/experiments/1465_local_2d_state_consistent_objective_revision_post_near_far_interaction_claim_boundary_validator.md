# Experiment 1465: Post Near/Far Interaction Claim Boundary Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1464` post near/far interaction claim boundary from
artifacts.

This run uses saved artifacts only. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1465_local_2d_state_consistent_objective_revision_post_near_far_interaction_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_near_far_interaction_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_near_far_interaction_claim_boundary_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_post_near_far_interaction_claim_boundary_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_NEAR_FAR_INTERACTION_CLAIM_BOUNDARY_VALIDATOR.md
scripts/run_local_2d_state_consistent_objective_revision_post_near_far_interaction_claim_boundary_validator.py
scripts/test_local_2d_state_consistent_objective_revision_post_near_far_interaction_claim_boundary_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:              7
passed checks:                  7
failed checks:                  0
validation ready:               true
claims:                         6
guarded local claims:           3
blocked claims:                 3
local mechanism evidence ready: true
broad radius promoted:          false
physical claim ready:           false
GPU work ready:                 false
field transfer ready:           false
field FWI ready:                false
3D/HPC ready:                   false
```

Validated checks:

| Check | Result |
| --- | --- |
| source policy and counts | pass |
| guarded local claims ready | pass |
| blocked claims not ready | pass |
| source guards ready | pass |
| downstream states blocked | pass |
| figure validation present | pass |
| script snapshots present | pass |

## Interpretation

The saved claim boundary validates: three local mechanism claims are guarded
and three broader claims remain blocked.

## Decision

Use run `1465` as the validator for the post near/far interaction claim
boundary. Promote only local mechanism evidence.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_near_far_interaction_claim_boundary_validator.py
3 passed
```

Figure validation:

```text
3329x895, dynamic range=255
```
