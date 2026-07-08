# Field Experiment 107: Publication Claim Bundle After Timing Discriminant And HPC Decision

Date: 2026-06-18

## Purpose

Refresh the measured-field publication claim bundle after the two latest field
endpoints:

```text
105_gssi51600s_field_timing_discriminant_scorecard
106_gssi51600s_field_hpc_dimensionality_decision_card
```

This run reads existing field summaries only. It does not run FDTD, FWI, GPU
kernels, neural-network training, 3D inversion, or HPC jobs.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/107_gssi51600s_field_publication_claim_bundle_post_timing_discriminant_hpc
```

Key artifacts:

```text
data/field_publication_figure_rows.csv
data/field_publication_claim_boundaries.csv
data/field_publication_claim_bundle_summary.json
figures/field_publication_claim_bundle.png
figures/FIGURE_NOTES.md
```

## Result

Policy label:

```text
field_publication_claim_bundle_2d_qc_hpc_dimensionality_timing_discriminant_timing_window_timing_anchor_cue_spacing_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
```

Summary:

```text
figure rows:                         22
claim boundaries:                    21
geometry classification:             independent_2d_line_profiles
timing discriminant included:        true
timing score rows:                   4
short non-raw timing supported:      18
long short-transfer rejections:       3
HPC dimensionality included:         true
HPC geometry type:                   independent_2d_line_profiles
ready for 2D QC:                     true
ready for 3D HPC:                    false
ready for field FWI:                 false
field HPC priority:                  none
GPU priority:                        none
```

## Interpretation

The current field publication bundle now explicitly includes the row-level
timing scorecard and the 2D-only/no-HPC dimensionality decision. The allowed
field use remains measured 2D line-profile QC, timing/repeatability evidence,
and manuscript boundary figures. The bundle does not create absolute
time-zero, cover-depth, radius, field-FWI, 3D inversion, or HPC claims.

## Validation

Figure validation:

```text
field_publication_claim_bundle.png: 4250x903,
nonwhite=0.0750, dynamic range=255
```
