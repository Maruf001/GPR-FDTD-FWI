# BEM Experiment 456: Post-Serialization Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `455` post-serialization BEM claim boundary from disk.

## Output

```text
outputs/bem_experiments/456_project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary_validator_checks.csv
data/project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary_validator_summary.json
figures/project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary_validator.png
```

## Result

```text
validation checks:                       5
validation checks passed:                5
blocking failures:                       0
claim-boundary validation ready:         true
claims:                                  28
guarded claims:                          25
blocked claims:                          3
serialization round-trip ready:          true
serialization validation ready:          true
serialization sensitivity ready:         true
minimum safe scorecard digits:           13
recommended storage digits:              17
real BEM/FDTD comparison ready:          false
3D validation ready:                     false
GPU/HPC ready:                           false
field FWI ready:                         false
```

The validator confirms the saved run `455` claim counts, serialization claim,
serialization metrics, downstream blocked states, figure, and script snapshots.

## Decision

Use this validator as the artifact guard for run `455`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary_validator.py
5 passed
```

Figure check:

```text
2645x839, dynamic range=255
```
