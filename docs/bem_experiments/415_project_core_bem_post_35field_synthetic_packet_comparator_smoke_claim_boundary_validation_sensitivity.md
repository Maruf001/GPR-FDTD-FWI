# BEM Experiment 415: Post 35-Field Synthetic Packet Comparator-Smoke Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `414` validator with damaged variants of the run `413`
claim boundary.

## Output

```text
outputs/bem_experiments/415_project_core_bem_post_35field_synthetic_packet_comparator_smoke_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                            15
expected pass:                        1
observed pass:                        1
expected failures:                    14
observed failures:                    14
unexpected outcomes:                  0
sensitivity ready:                    true
accepts exact run 413:                true
rejects damaged variants:             true
claims:                               21
guarded claims:                       18
blocked claims:                       3
paired keys:                          279
scattered component cells:            1674
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
GPU/HPC ready:                        false
```

Damaged variants fail for source-label drift, claim-count drift, consumer-claim
support drift, consumer-claim evidence drift, consumer-count drift, paired-key
drift, receiver-count drift, scattered-cell drift, coordinate drift, false
evidence promotion, blocked-support drift, downstream promotion, figure drift,
and script-snapshot drift.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_synthetic_packet_comparator_smoke_claim_boundary.py
tests/test_project_core_bem_post_35field_synthetic_packet_comparator_smoke_claim_boundary_validator.py
tests/test_project_core_bem_post_35field_synthetic_packet_comparator_smoke_claim_boundary_validation_sensitivity.py
6 passed
```

Figure validation:

```text
3581x877, dynamic range=255
```
