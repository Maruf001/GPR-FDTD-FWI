# Field Experiment 123: GSSI 51600S Field Inversion Readiness Synthesis

Date: 2026-06-18

## Purpose

Consolidate the current measured-field evidence into explicit readiness gates
for short-profile QC, apparent-depth scale QC, profile spatial calibration,
cover-depth/radius recovery, field FWI, and 3D/HPC. This is a CPU-only
synthesis over saved field summaries and does not launch FDTD, FWI, GPU
kernels, 3D/HPC jobs, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/123_gssi51600s_field_inversion_readiness_synthesis_post_spatial_consistency
```

Key artifacts:

```text
data/field_inversion_readiness_synthesis_rows.csv
data/field_inversion_readiness_synthesis_summary.json
figures/field_inversion_readiness_synthesis.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                       gssi51600s_field_inversion_readiness_synthesis_short_qc_only
readiness gates:                    8
supported gates:                    2
blocked gates:                      6
supported gate keys:                short_relative_timing_qc;apparent_depth_scale_qc
blocked gate keys:                  long_profile_transfer;profile_spatial_calibration;cover_depth_recovery;radius_recovery;field_fwi;field_3d_hpc
ready for short relative timing QC: true
ready for apparent-depth scale QC:  true
ready for long-profile transfer:    false
ready for profile spatial calibration: false
ready for cover-depth recovery:     false
ready for radius recovery:          false
ready for field FWI:                false
ready for 3D/HPC:                   false
field geometry type:                independent_2d_line_profiles
is 3D survey:                       false
spatial residual range:             29.997 mm
apparent-depth max span:            149.916 mm
apparent-depth sensitivity factor:  2.18x
hyperbola near-top epsr span:       4.085
hyperbola near-top time-zero span:  0.300 ns
gpu priority:                       none
```

Interpretation: the local GSSI field data can support short-profile
timing/visual QC and apparent-depth scale checks. Heavy field work remains
blocked because the archive lacks external survey layout, absolute timing/depth
controls, calibrated dielectric/target geometry, profile spatial calibration,
and cover-depth/radius validation.

## Validation

```text
tests/test_gssi_field_inversion_readiness_synthesis.py
2 passed
```

Figure validation:

```text
field_inversion_readiness_synthesis.png: 2263x886,
nonwhite=0.1187, dynamic range=255
```
