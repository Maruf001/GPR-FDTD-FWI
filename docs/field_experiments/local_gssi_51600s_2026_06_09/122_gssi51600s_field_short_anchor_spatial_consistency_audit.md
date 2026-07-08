# Field Experiment 122: GSSI 51600S Field Short-Anchor Spatial Consistency Audit

Date: 2026-06-18

## Purpose

Test whether the content-backed short-profile anchors support a single
profile-to-profile spatial translation after the existing timing-envelope,
supported-interval, leave-one, and time-zero ladder checks. This remains a
CPU-side field QC audit and does not launch field FWI, 3D/HPC, neural network
training, or broad GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/122_gssi51600s_field_short_anchor_spatial_consistency_audit
```

Key artifacts:

```text
data/field_short_anchor_spatial_consistency_rows.csv
data/field_short_anchor_spatial_consistency_summary.json
figures/field_short_anchor_spatial_consistency_audit.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_field_short_anchor_spatial_consistency_timing_qc_only
short anchors:                        3
content-backed anchors:               2
timing-only anchors:                  1
content anchors inside intervals:     2
content residual range:               29.997 mm
content residual half-range:          14.9985 mm
content abs residual max:             19.998 mm
content min supported-interval margin: 13.332 mm
content residual sign consistent:     false
single spatial translation supported: false
ready for short relative timing QC:   true
ready for profile spatial calibration: false
ready for absolute time-zero:         false
ready for cover-depth recovery:       false
ready for radius recovery:            false
ready for field FWI:                  false
ready for 3D HPC:                     false
gpu priority:                         none
```

Interpretation: the short content-backed anchors still support relative timing
QC, but their signed spatial residuals do not support a single calibrated
profile-to-profile spatial translation. Field use therefore remains
short-profile timing/visual QC, not absolute time-zero, cover-depth recovery,
radius recovery, field FWI, 3D, or HPC input.

## Validation

```text
tests/test_gssi_field_short_anchor_spatial_consistency_audit.py
2 passed
```

Figure validation:

```text
field_short_anchor_spatial_consistency_audit.png: 2195x835,
nonwhite=0.3272, dynamic range=255
```
