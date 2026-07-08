# BEM Experiment 455: Post-Serialization Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded reference-coefficient serialization round-trip block from runs
`452-454` into the BEM claim boundary.

## Output

```text
outputs/bem_experiments/455_project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary_summary.json
figures/project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary.png
```

## Result

```text
claims:                                  28
guarded claims:                          25
blocked claims:                          3
serialization round-trip ready:          true
serialization validation ready:          true
serialization sensitivity ready:         true
reference coefficient:                   0.01907878402833891
relative tolerance:                      1e-12
serialization scenarios:                 12
passing serialization scenarios:         9
failing serialization scenarios:         3
safe scorecard scenarios:                9
preferred scorecard scenarios:           4
preferred scenarios passing:             4
minimum safe scorecard digits:           13
recommended storage digits:              17
sensitivity scenarios:                   34
sensitivity expected failures:           33
sensitivity unexpected outcomes:         0
real BEM/FDTD comparison ready:          false
3D validation ready:                     false
GPU/HPC ready:                           false
field FWI ready:                         false
```

The new guarded claim records that future real-return scorecards should store
the reference coefficient with full numeric precision or 17 significant digits,
while 13 significant digits remains the minimum tolerance-preserving floor.

## Decision

Use this as the current BEM claim boundary after the serialization round-trip
block. This updates the scorecard-storage contract only; real BEM/FDTD
comparison and downstream escalation remain blocked until real returned values
and hashes exist.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_reference_coefficient_serialization_roundtrip_claim_boundary.py
4 passed
```

Figure check:

```text
3941x899, dynamic range=255
```
