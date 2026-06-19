# Field Experiment 072: Acquisition Readiness Audit

Date: 2026-06-18

## Purpose

Quantify whether the local GSSI 51600S measured dataset should be treated as a
2D QC dataset, a 3D survey, or a field-FWI/HPC workload. This is a CPU-only
audit over existing field outputs; it does not launch FDTD, FWI, GPU kernels,
3D inversion, radius recovery, or cover-depth recovery.

## Output

```text
081_gssi51600s_field_acquisition_readiness_audit
```

Key artifacts:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/081_gssi51600s_field_acquisition_readiness_audit/data/field_acquisition_readiness_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/081_gssi51600s_field_acquisition_readiness_audit/data/field_acquisition_readiness_summary.json
outputs/field_experiments/local_gssi_51600s_2026_06_09/081_gssi51600s_field_acquisition_readiness_audit/figures/field_acquisition_readiness_audit.png
```

## Result

Policy label:

```text
field_acquisition_readiness_2d_qc_not_hpc_fwi
```

Summary:

```text
survey classification:              independent_2d_line_profiles
profile count:                      4
scan spacing:                       3.333 mm
antenna frequency:                  1600 MHz
dielectric:                         2.25
nominal in-medium wavelength:       124.914 mm
samples per nominal wavelength:     37.478
nominal depth window:               499.654 mm
time-zero conservative half-width:  0.058939 ns
two-way depth equivalent:           5.890 mm
all-window spatial support:         70 / 249 columns
all-window spatial support fraction:0.281124
ready for 2D QC:                    true
ready for 3D HPC:                   false
ready for field FWI:                false
field HPC priority:                 none
```

## Interpretation

The field data are densely sampled along each line and remain useful for 2D
timing, repeatability, and visual-QC claims. They are not a 3D survey or a
field-FWI benchmark: the survey audit still lacks recoverable crossline/grid
metadata, time-zero support is relative rather than absolute, all-window spatial
support is sparse, and the long 015/013 pair remains pattern-only because one
profile lacks nominal phase-anchor picks.

Do not submit a field-data FWI or 3D HPC job from this dataset. Field-side HPC
should wait for external survey-layout metadata, calibrated target geometry, or
a new controlled acquisition.

## Validation

Focused tests:

```text
tests/test_gssi_field_acquisition_readiness_audit.py
3 passed
```

Figure validation:

```text
081 field_acquisition_readiness_audit.png: 2535x903, dynamic range=255
```
