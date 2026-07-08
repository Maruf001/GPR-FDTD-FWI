# BEM Experiment 414: Post 35-Field Synthetic Packet Comparator-Smoke Claim-Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `413` claim boundary from artifacts.

## Output

```text
outputs/bem_experiments/414_project_core_bem_post_35field_synthetic_packet_comparator_smoke_claim_boundary_validator
```

## Result

```text
validation checks:                    7
passed checks:                        7
failed checks:                        0
validation ready:                     true
claims:                               21
guarded claims:                       18
blocked claims:                       3
paired keys:                          279
receivers:                            31
frequencies:                          9
scattered rows:                       279
scattered component cells:            1674
synthetic packet is evidence:         false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
GPU/HPC ready:                        false
```

The validator confirms claim counts, the new synthetic downstream-consumer
claim row, consumer metrics, blocked claim rows, blocked downstream states,
figure validation, and script snapshots.

## Validation

Focused test:

```text
tests/test_project_core_bem_post_35field_synthetic_packet_comparator_smoke_claim_boundary_validator.py
2 passed
```

Figure validation:

```text
3617x893, dynamic range=255
```
