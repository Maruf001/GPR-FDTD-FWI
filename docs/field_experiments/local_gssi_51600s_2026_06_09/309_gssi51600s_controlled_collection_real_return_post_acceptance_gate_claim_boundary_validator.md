# Field Experiment 309: Real-Return Post Acceptance Gate Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `308` field post-acceptance claim boundary from
artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/309_gssi51600s_controlled_collection_real_return_post_acceptance_gate_claim_boundary_validator
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
claims:                             12
guarded claims:                     8
blocked claims:                     4
missing packet items:               57
missing measured DZT files:         9
missing metadata requirements:      32
missing checksum rows:              9
missing acceptance results:         7
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
GPU priority:                       none
```

## Decision

Use run `309` as the validator for the run `308` field post-acceptance claim
boundary.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_post_acceptance_gate_claim_boundary_validator.py
3 passed
```

Figure validation:

```text
3689x929, dynamic range=255
```
