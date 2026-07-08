# Field Experiment 043: GSSI 51600S Corrected Profile Stack

Date: 2026-06-17

## Purpose

CPU-only B-scan-level check of the short-profile relative time-zero correction.
This run uses the existing 014/016 spatial alignment from field experiment 021
and the applied relative time-zero transfer from field experiment 025.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/043_gssi51600s_corrected_profile_stack
```

Artifacts:

```text
data/corrected_profile_stack_column_agreement.csv
data/corrected_profile_stack_summary.json
data/figure_validation.csv
figures/corrected_profile_stack.png
run_manifest.json
```

## Result

Policy label:

```text
corrected_profile_stack_time_zero_supported
```

Summary:

```text
profile pair:                         PROJECT001C__014 / PROJECT001C__016
spatial alignment:                    reversed, lag=83.325 mm
applied relative time-zero offset:    0.127701 ns
window:                               0.45-1.25 ns
raw matrix abs correlation:           0.535682
corrected matrix abs correlation:     0.812268
matrix abs correlation improvement:   0.276586
raw matrix residual RMS:              0.982203
corrected matrix residual RMS:        0.625209
finite profile columns:               249
improved profile columns:             161
improved column fraction:             0.646586
mean column abs-correlation gain:     0.144253
```

## Interpretation

The relative time-zero correction improves the aligned 014/016 B-scan window,
not only the two individual content-anchor traces. This strengthens the field
timing/repeatability QC chain.

The result is still not field inversion evidence. It does not establish
absolute time zero, survey geometry, cover depth, radius, 3D structure, or
measured-data FWI validity.

## Validation

Focused tests:

```text
tests/test_gssi_field_corrected_profile_stack.py: 3 passed
```

Figure validation:

```text
corrected_profile_stack.png: 2261x1481,
nonwhite=0.4308, dynamic range=255
```
