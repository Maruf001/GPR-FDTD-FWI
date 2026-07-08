# Experiment 1492: Post Offset-Transition Claim Boundary

Date: 2026-06-29

## Purpose

Refresh the local 2D near/far claim boundary after adding the five-offset
acquisition-layout transition map from runs `1489-1491`.

This run uses saved artifacts only. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1492_local_2d_state_consistent_objective_revision_post_offset_transition_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_offset_transition_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_offset_transition_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_offset_transition_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                              13
guarded claims:                      10
blocked claims:                      3
design axes ready:                   5 / 5
position generalization ready:       true
depth generalization ready:          true
spacing generalization ready:        true
source-model generalization ready:   true
acquisition generalization ready:    true
spacing truth/any/all failure:       23 / 22 / 12
source truth/any/all failure:        10 / 20 / 10
acquisition truth/any/all failure:   45 / 30 / 18
boundary ready:                      true
45 mm any far-error suppressed:      true
35 mm all-failure suppression:       true
any-failure persists through 40 mm:  true
first any far -0.8 suppression mm:   45.0
first any far -1.6 suppression mm:   45.0
broad radius promoted:               false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
figure size:                         3671x942
figure dynamic range:                255
```

## Interpretation

The near/far mechanism remains guarded local synthetic evidence after all five
planned axes have been tested. The severe all-objective failure boundary is
position-, depth-, spacing-, and acquisition-layout dependent.

The refined acquisition-layout map adds a more precise result: all-objective
far-error failures clear by 35 mm, while any-objective far-error failures
persist through 40 mm and clear at 45 mm in the tested grid.

## Decision

Use run `1492` as the current refined 2D near/far claim boundary. Keep broad
invariant radius-tolerance, physical-transfer, GPU, field-FWI, and 3D/HPC
claims blocked until measured-field evidence or a new validated compute
objective changes the decision boundary.
