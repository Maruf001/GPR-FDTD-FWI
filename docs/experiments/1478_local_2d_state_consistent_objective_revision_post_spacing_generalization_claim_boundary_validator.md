# Experiment 1478: Post Spacing Generalization Claim Boundary Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1477` claim-boundary artifact from saved tables.

This validator checks the claim counts, spacing result counts, position/depth/
spacing boundary flags, downstream guardrails, figure validation, and script
snapshots.

This uses saved artifacts only. It does not run new FDTD simulations, launch
GPU work, transfer to field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1478_local_2d_state_consistent_objective_revision_post_spacing_generalization_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_spacing_generalization_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_spacing_generalization_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_spacing_generalization_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_SPACING_GENERALIZATION_CLAIM_BOUNDARY_VALIDATOR.md
```

## Result

```text
validation checks:              7
passed checks:                  7
failed checks:                  0
validation ready:               true
claims:                         9
guarded claims:                 6
blocked claims:                 3
spacing grid models:            45
spacing all-objectives truth:   23
spacing any-failure models:     22
spacing all-objective failures: 12
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

Run `1477` validates as the current local 2D near/far generalization claim
boundary: the mechanism is guarded local evidence, but severe all-objective
failure is not position-, depth-, or spacing-invariant.

## Decision

Use run `1478` as the validator for the post-spacing claim boundary. Keep
broad-radius, physical, GPU, field-transfer, field-FWI, and 3D/HPC claims
blocked.
