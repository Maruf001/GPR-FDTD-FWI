# Field Experiment 066: GSSI 51600S Field Publication Bundle After Relaxed Anchor Audit

Date: 2026-06-18

## Purpose

CPU-only refresh of the field publication claim bundle after run 064 showed
that relaxed long-profile phase-anchor candidates remain low-SNR and should be
treated as negative time-zero evidence.

No FDTD, FWI, GPU kernels, 3D reconstruction, or field inversion was launched.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/066_gssi51600s_field_publication_claim_bundle_post_relaxed_anchor
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
field_publication_claim_bundle_2d_qc_relaxed_anchor_negative_ready_not_fwi
```

Summary:

```text
figure rows:                         8
claim boundaries:                    7
relaxed phase-anchor included:       true
relaxed low-SNR pick count:          10 / 10
geometry classification:             independent_2d_line_profiles
ready for manuscript supplement:     true
field GPU/FWI priority:              none
```

## Interpretation

Run 066 supersedes run 062 as the current paper-facing field figure bundle. It
keeps the prior 2D QC figures and adds the relaxed long-profile phase-anchor
audit as negative QC:

```text
Profile 013 relaxed candidates remain low-SNR, so the 015/013 long pair stays
pattern-only. Do not promote this dataset to absolute time-zero, cover-depth,
radius, 3D, or measured-data FWI evidence.
```

## Validation

Focused tests:

```text
tests/test_gssi_field_publication_claim_bundle.py: 5 passed
```

Figure validation:

```text
field_publication_claim_bundle.png: 2569x869,
nonwhite=0.2354, dynamic range=255
```
