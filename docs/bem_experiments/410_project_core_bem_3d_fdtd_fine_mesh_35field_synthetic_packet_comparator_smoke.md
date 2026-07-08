# BEM Experiment 410: 35-Field Synthetic Packet Comparator Smoke

Date: 2026-06-29

## Purpose

Test whether the filled 35-field synthetic packet from run `404` can be
consumed beyond preflight: pair target and background frequency-bin rows by
receiver/frequency key and compute target-minus-background scattered rows.

This run uses deterministic synthetic values only. It does not stage real
returned FDTD files, run a real BEM/FDTD comparison, transfer to field
evidence, launch GPU work, or make a 3D validation claim.

## Output

```text
outputs/bem_experiments/410_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_packet_comparator_smoke
```

## Result

```text
consumer checks:                      10
consumer passes:                      10
consumer failures:                    0
synthetic comparator smoke ready:     true
target frequency rows:                279
background frequency rows:            279
paired keys:                          279
receivers:                            31
frequencies:                          9
scattered rows:                       279
scattered component cells:            1674
mean scattered norm:                  0.43754011371657237
max scattered norm:                   1.7743269146355192
max pair coordinate delta:            0.0 m
synthetic packet is evidence:         false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
GPU/HPC ready:                        false
```

## Interpretation

The filled packet is not only preflight-compatible; it can also be consumed by
a downstream pairing/subtraction step. The target and background files produce
279 paired scattered rows over 31 receivers and nine frequencies.

This remains a structural smoke. The computed scattered rows are derived from
synthetic placeholder values, so they are not real BEM/FDTD comparison
evidence.

## Decision

Use run `410` as a downstream-consumer smoke for the 35-field packet. Keep real
BEM/FDTD comparison, 3D validation, field transfer, field FWI, and GPU/HPC
blocked until real returned FDTD files replace the synthetic packet.

## Validation

Focused test:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_packet_comparator_smoke.py
4 passed
```

Figure validation:

```text
3653x914, dynamic range=255
```
