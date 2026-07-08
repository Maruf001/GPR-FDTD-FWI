# Experiment 1487: Post Full Generalization Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1486` full-generalization claim-boundary artifact from
saved tables.

This uses saved artifacts only. It does not run new FDTD simulations, launch GPU
work, transfer to field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1487_local_2d_state_consistent_objective_revision_post_full_generalization_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_full_generalization_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_full_generalization_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_full_generalization_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_FULL_GENERALIZATION_CLAIM_BOUNDARY_VALIDATOR.md
```

## Result

```text
validation checks:             9
passed checks:                 9
failed checks:                 0
validation ready:              true
claims:                        12
guarded claims:                9
blocked claims:                3
design axes ready:             5 / 5
source threshold stable:       true
acquisition suppression:       true
broad radius promoted:         false
physical claim ready:          false
GPU work ready:                false
field transfer ready:          false
field FWI ready:               false
3D/HPC ready:                  false
```

## Interpretation

Run `1486` validates as the full local 2D near/far generalization claim
boundary: the mechanism is guarded local evidence, but the severe
all-objective failure boundary is constrained by geometry and acquisition
layout.

## Decision

Use run `1487` as the validator for the full five-axis claim boundary. Keep
broad-radius, physical, GPU, field-transfer, field-FWI, and 3D/HPC claims
blocked.
