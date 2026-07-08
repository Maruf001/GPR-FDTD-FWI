# Experiment 1477: Post Spacing Generalization Claim Boundary

Date: 2026-06-28

## Purpose

Refresh the local 2D claim boundary after the guarded target-position,
target-depth, and neighbor-spacing generalization blocks.

Runs `1468-1476` show that the near/far failure mechanism remains real in the
tested local synthetic setup, but the severe all-objective failure boundary
changes with aperture position, target depth, and neighbor spacing. This run
converts those results into a current claim table.

This uses saved artifacts only. It does not run new FDTD simulations, launch
GPU work, transfer to field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1477_local_2d_state_consistent_objective_revision_post_spacing_generalization_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_spacing_generalization_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_spacing_generalization_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_spacing_generalization_claim_boundary.png
scripts/script_snapshot_manifest.json
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_SPACING_GENERALIZATION_CLAIM_BOUNDARY.md
```

## Result

```text
claims:                         9
guarded claims:                 6
blocked claims:                 3
position generalization ready:  true
depth generalization ready:     true
spacing generalization ready:   true
spacing grid models:            45
spacing all-objectives truth:   23
spacing any-failure models:     22
spacing all-objective failures: 12
boundary ready:                 true
position dependent boundary:    true
depth dependent boundary:       true
spacing dependent boundary:     true
broad radius promoted:          false
physical claim ready:           false
GPU work ready:                 false
field transfer ready:           false
field FWI ready:                false
3D/HPC ready:                   false
```

## Interpretation

The near/far mechanism remains guarded as local synthetic evidence, but the
severe all-objective failure boundary is now known to depend on aperture
position, target depth, and neighbor spacing.

## Decision

Use this as the current 2D claim boundary. Keep broad-radius tolerance,
physical-transfer, GPU, field-FWI, and 3D/HPC claims blocked until additional
source, acquisition, or measured-field evidence closes those gaps.
