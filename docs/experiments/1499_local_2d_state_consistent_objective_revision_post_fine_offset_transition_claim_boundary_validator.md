# Experiment 1499: Post Fine Offset-Transition Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1498` fine-refined local 2D near/far claim boundary
from artifacts.

Run `1498` integrated the guarded fine transition from runs `1495-1497` into
the local 2D claim boundary. This run checks that the saved boundary preserves
the expected claim counts, fine-transition metrics, blocked downstream states,
figure validation, and script snapshots.

This is an artifact-only validation run. It does not run new FDTD simulations,
launch GPU work, transfer claims to field evidence, run field FWI, or start
3D/HPC work.

## Output

```text
outputs/experiments/1499_local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:             8
passed checks:                 8
failed checks:                 0
validation ready:              true
claims:                        14
guarded claims:                11
blocked claims:                3
fine grid models:              90
fine any-failure models:       32
fine all-failure models:       12
40-44 mm far-error persists:   true
45 mm far-error suppressed:    true
broad radius promoted:         false
physical claim ready:          false
GPU work ready:                false
field transfer ready:          false
field FWI ready:               false
3D/HPC ready:                  false
figure size:                   3581x928
figure dynamic range:          255
```

## Interpretation

The fine-refined claim boundary validates from saved artifacts. The current
local 2D boundary has 14 claims: 11 guarded local/design observations and
three blocked downstream claims.

The new fine acquisition-layout claim remains stable: far-error any-objective
failures persist through 44 mm and first clear at 45 mm in the tested
40-45 mm sweep. All-objective far-error failures remain absent throughout that
fine sweep.

The validator intentionally preserves the no-go decision for broad-radius
promotion, physical transfer, GPU escalation, field FWI, and 3D/HPC work.

## Decision

Use run `1499` as the validator for the fine-refined local 2D near/far claim
boundary. A sensitivity hardening run remains required before treating this
validator as a guarded validation block.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary_validator.py
4 passed
```
