# Experiment 1486: Post Full Generalization Claim Boundary

Date: 2026-06-29

## Purpose

Refresh the local 2D claim boundary after all five near/far generalization axes
have been executed and sensitivity checked:

```text
target position
target depth
neighbor spacing
source timing
Tx/Rx acquisition layout
```

This uses saved artifacts only. It does not run new FDTD simulations, launch GPU
work, transfer to field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1486_local_2d_state_consistent_objective_revision_post_full_generalization_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_full_generalization_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_full_generalization_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_full_generalization_claim_boundary.png
scripts/script_snapshot_manifest.json
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_FULL_GENERALIZATION_CLAIM_BOUNDARY.md
```

## Result

```text
claims:                              12
guarded claims:                      9
blocked claims:                      3
design axes ready:                   5 / 5
position generalization ready:       true
depth generalization ready:          true
spacing generalization ready:        true
source-model generalization ready:   true
acquisition generalization ready:    true
spacing truth/any/all failure:       23 / 22 / 12
source truth/any/all failure:        10 / 20 / 10
acquisition truth/any/all failure:   18 / 12 / 8
boundary ready:                      true
source far-error threshold stable:   true
45 mm far-error failures suppressed: true
broad radius promoted:               false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The near/far mechanism remains guarded as local synthetic evidence after all
five planned axes have been tested. The severe all-objective failure boundary is
position-, depth-, spacing-, and acquisition-layout dependent. Source timing
does not remove the far-error onset in this matched test, but it does soften
the far-error-free all-objective detail.

## Decision

Use this as the current full 2D near/far claim boundary. Keep broad invariant
radius-tolerance, physical-transfer, GPU, field-FWI, and 3D/HPC claims blocked
until measured-field evidence or a new validated compute objective changes the
decision boundary.
