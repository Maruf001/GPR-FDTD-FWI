# Experiment 1439: Local 2D Post Objective-Revision Claim Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1438` validator for the local 2D objective-revision claim
boundary.

This run checks whether the validator accepts the exact saved run `1437`
boundary and rejects controlled damage to row structure, summary counts,
repair-policy support, `veryhigh` failure labels, and downstream readiness
states.

This run does not execute new FDTD simulations, launch GPU work, transfer to
field data, run field FWI, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1439_local_2d_state_consistent_post_objective_revision_claim_boundary_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_post_objective_revision_claim_boundary_sensitivity_scenarios.csv
data/local_2d_state_consistent_post_objective_revision_claim_boundary_sensitivity_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_post_objective_revision_claim_boundary_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_POST_OBJECTIVE_REVISION_CLAIM_BOUNDARY_SENSITIVITY.md
scripts/run_local_2d_state_consistent_post_objective_revision_claim_boundary_sensitivity.py
scripts/test_local_2d_state_consistent_post_objective_revision_claim_boundary_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         31
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        30
observed failure scenarios:        30
unexpected outcomes:               0
sensitivity ready:                 true
claim-boundary validation ready:   true
objective revision local ready:    true
veryhigh failure count:            3
non-veryhigh failure count:        0
promote revised objective now:     false
broad radius tolerance promoted:   false
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

## Interpretation

The claim-boundary validator accepts the exact run `1437` boundary and rejects
30 damaged variants. The rejected cases cover missing rows, status drift,
promotion drift, repair-policy support drift, missing `veryhigh` failure
labels, summary count drift, false local-validation support, and false
broad/physical/GPU/field/FWI/3D readiness.

## Decision

Use runs `1437-1439` as the guarded local 2D objective-revision claim boundary.
The local objective policy is supported for this tested setup, but broad-radius
tolerance, physical-transfer, GPU, field-transfer, field-FWI, and 3D/HPC claims
remain blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_post_objective_revision_claim_boundary_sensitivity.py
5 passed
```

Figure validation:

```text
4121x887, dynamic range=255
```
