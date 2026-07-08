# BEM Experiment 457: Post-Serialization Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `456` validator against controlled damage to the run `455`
claim boundary.

## Output

```text
outputs/bem_experiments/457_project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary_validation_sensitivity.png
```

## Result

```text
sensitivity scenarios:                  32
expected pass scenarios:                 1
observed pass scenarios:                 1
expected failure scenarios:              31
observed failure scenarios:              31
unexpected outcomes:                     0
validation sensitivity ready:            true
validator accepts exact run 455:         true
validator rejects damaged variants:      true
real BEM/FDTD comparison ready:          false
3D validation ready:                     false
GPU/HPC ready:                           false
field FWI ready:                         false
```

The damaged variants cover claim-count drift, serialization-readiness drift,
reference/tolerance drift, serialization metric drift, serialization-claim
drift, downstream promotion, figure drift, and missing script snapshots. The
exact run `455` passes and all damaged variants fail as expected.

## Decision

Use runs `455-457` as the current guarded BEM post-serialization
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x885, dynamic range=255
```
