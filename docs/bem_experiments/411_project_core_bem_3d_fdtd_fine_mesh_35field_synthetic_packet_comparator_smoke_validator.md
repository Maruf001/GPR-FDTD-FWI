# BEM Experiment 411: 35-Field Synthetic Packet Comparator-Smoke Validator

Date: 2026-06-29

## Purpose

Validate the saved run `410` comparator smoke from artifacts.

## Output

```text
outputs/bem_experiments/411_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_packet_comparator_smoke_validator
```

## Result

```text
validation checks:                    8
passed checks:                        8
failed checks:                        0
validation ready:                     true
paired keys:                          279
receivers:                            31
frequencies:                          9
scattered rows:                       279
scattered component cells:            1674
mean scattered norm:                  0.43754011371657237
max scattered norm:                   1.7743269146355192
synthetic packet is evidence:         false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
GPU/HPC ready:                        false
```

The validator confirms source identity, consumer counts, pair-grid counts,
scattered norms, pair coordinate agreement, all consumer checks, blocked
downstream states, figure validation, and script snapshots.

## Validation

Focused test:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_packet_comparator_smoke_validator.py
2 passed
```

Figure validation:

```text
3545x894, dynamic range=255
```
