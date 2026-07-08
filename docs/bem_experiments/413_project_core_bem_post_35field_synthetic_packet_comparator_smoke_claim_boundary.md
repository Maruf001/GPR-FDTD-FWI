# BEM Experiment 413: Post 35-Field Synthetic Packet Comparator-Smoke Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded synthetic downstream-consumer result from runs `410-412` into
the current BEM claim boundary.

This run does not stage real returned FDTD files, run a real BEM/FDTD
comparison, transfer to field evidence, launch GPU work, or make a 3D
validation claim.

## Output

```text
outputs/bem_experiments/413_project_core_bem_post_35field_synthetic_packet_comparator_smoke_claim_boundary
```

## Result

```text
claims:                               21
guarded claims:                       18
blocked claims:                       3
synthetic comparator sensitivity:     true
synthetic comparator smoke ready:     true
consumer checks:                      10
consumer passes:                      10
consumer failures:                    0
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

## Interpretation

The BEM claim boundary now includes the downstream-consumer smoke: a filled
35-field synthetic packet can be paired by receiver/frequency and subtracted
into scattered rows.

This is still not real BEM/FDTD comparison evidence. It proves that the
downstream consumer can read the packet shape, not that the synthetic values
match a physical FDTD return.

## Decision

Use run `413` as the current BEM claim boundary after the synthetic
comparator-smoke block. Real comparison remains blocked until real returned
FDTD target/background files replace the synthetic packet.

## Validation

Focused test:

```text
tests/test_project_core_bem_post_35field_synthetic_packet_comparator_smoke_claim_boundary.py
2 passed
```

Figure validation:

```text
3941x891, dynamic range=255
```
