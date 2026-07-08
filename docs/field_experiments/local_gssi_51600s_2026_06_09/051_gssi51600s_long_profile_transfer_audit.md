# Field Experiment 051: GSSI 51600S Long-Profile Transfer Audit

Date: 2026-06-17

## Purpose

CPU-only audit of whether the 014/016 short-profile relative time-zero
correction transfers to the long-profile 015/013 pair.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/051_gssi51600s_long_profile_transfer_audit
```

Artifacts:

```text
data/long_profile_transfer_column_agreement.csv
data/long_profile_transfer_anchor_windows.csv
data/long_profile_transfer_audit_summary.json
data/figure_validation.csv
figures/long_profile_transfer_audit.png
run_manifest.json
```

## Result

Policy label:

```text
long_profile_short_correction_transfer_not_supported
```

Summary:

```text
raw matrix abs corr:             0.763452
corrected matrix abs corr:       0.732421
matrix abs-corr change:         -0.031031
finite columns:                  683
improved columns:                369
stable anchor windows:           6
improved stable anchor windows:  0
min corrected anchor abs corr:   0.539009
```

## Interpretation

The short-profile relative time-zero correction should not be generalized to
the 015/013 long pair. It slightly reduces whole-window agreement and improves
none of the six stable long-profile anchor windows.

This strengthens the field boundary: the 014/016 correction is useful for the
short-pair visual-QC story, while 015/013 remains long-profile pattern-only
evidence because profile 013 lacks phase-anchor picks.

## Validation

Focused tests:

```text
tests/test_gssi_field_long_profile_transfer_audit.py: 4 passed
```

Figure validation:

```text
long_profile_transfer_audit.png: 2397x1447,
nonwhite=0.5461, dynamic range=255
```
