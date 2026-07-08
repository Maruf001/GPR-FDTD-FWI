# Experiment 1464: Post Near/Far Interaction Claim Boundary

Date: 2026-06-28

## Purpose

Refresh the local 2D claim boundary after the guarded near/far radius-error
interaction block.

This run uses saved artifacts only. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1464_local_2d_state_consistent_objective_revision_post_near_far_interaction_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_near_far_interaction_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_near_far_interaction_claim_boundary_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_post_near_far_interaction_claim_boundary.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_NEAR_FAR_INTERACTION_CLAIM_BOUNDARY.md
scripts/run_local_2d_state_consistent_objective_revision_post_near_far_interaction_claim_boundary.py
scripts/test_local_2d_state_consistent_objective_revision_post_near_far_interaction_claim_boundary.py
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                         6
guarded local claims:           3
blocked claims:                 3
threshold guard ready:          true
interaction guard ready:        true
local mechanism evidence ready: true
broad radius promoted:          false
physical claim ready:           false
GPU work ready:                 false
field transfer ready:           false
field FWI ready:                false
3D/HPC ready:                   false
```

Guarded local claims:

| Claim | Supporting runs | Evidence |
| --- | --- | --- |
| near-neighbor radius-error threshold is a local mechanism | 1458-1460 | At far -1.6 mm, near +0.0 mm passes, +0.5/+1.0 mm partially fail, and +1.5/+1.9 mm all-objective fail. |
| far-neighbor error shifts partial-failure boundary | 1461-1463 | First partial failure moves from near +1.5 mm with no far error to near +0.5 mm with far -0.8 or -1.6 mm. |
| all-objective wrong-lock boundary is near dominated in the tested grid | 1461-1463 | First all-objective failure stays at near +1.5 mm across far +0.0, -0.8, and -1.6 mm. |

Blocked claims:

| Claim | Reason |
| --- | --- |
| broad radius tolerance policy | Needs independent geometries, seeds, and acquisition settings. |
| physical or field transfer | Needs measured field packet and transfer validation. |
| GPU, field FWI, or 3D/HPC escalation | Needs a new validated design objective or accepted field data. |

## Interpretation

The near/far interaction block supports a guarded local mechanism claim:
far-neighbor radius error shifts partial failures earlier, while all-objective
wrong-lock failure remains near-neighbor dominated in the tested grid.

## Decision

Promote only the local mechanism evidence. Keep broad-radius tolerance,
physical transfer, GPU work, field transfer/FWI, and 3D/HPC claims blocked
until independent designs or accepted field data exist.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_near_far_interaction_claim_boundary.py
3 passed
```

Figure validation:

```text
3437x909, dynamic range=255
```
