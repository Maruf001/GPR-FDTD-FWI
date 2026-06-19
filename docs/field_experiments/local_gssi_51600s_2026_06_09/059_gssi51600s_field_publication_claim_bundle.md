# Field Experiment 059: GSSI 51600S Field Publication Claim Bundle

Date: 2026-06-17

## Purpose

CPU-only field publication bundle that converts the current local GSSI 51600S
field QC endpoints into structured figure rows and claim boundaries.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/059_gssi51600s_field_publication_claim_bundle
```

Artifacts:

```text
data/field_publication_figure_rows.csv
data/field_publication_claim_boundaries.csv
data/field_publication_claim_bundle_summary.json
data/figure_validation.csv
figures/field_publication_claim_bundle.png
run_manifest.json
```

## Result

Policy label:

```text
field_publication_claim_bundle_2d_qc_ready_not_fwi
```

Summary:

```text
figure rows:                         5
claim boundaries:                    5
geometry classification:             independent_2d_line_profiles
long holdout policy:                 long_profile_pattern_holdout_qc_all_candidate_anchors_supported
ready for manuscript field supplement: true
gpu priority:                        none
```

Included figure rows:

```text
survey_geometry_boundary
short_content_waveform_qc
short_supported_stack_intervals
long_pattern_visual_qc
long_pattern_holdout_qc
```

## Interpretation

Use this bundle for measured field-data QC figures only. It supports 2D
line-profile geometry boundaries, short-profile relative timing/repeatability
QC, and long-profile pattern-only QC. It does not create 3D, field inversion,
radius, cover-depth, absolute time-zero, or measured-data FWI claims.

## Validation

Focused tests:

```text
tests/test_gssi_field_publication_claim_bundle.py: 3 passed
```

Figure validation:

```text
field_publication_claim_bundle.png: 2195x835,
nonwhite=0.2559, dynamic range=255
```
