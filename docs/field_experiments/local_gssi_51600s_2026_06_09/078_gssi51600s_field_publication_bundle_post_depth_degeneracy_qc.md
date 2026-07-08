# Field Experiment 078: Publication Bundle After Depth/Degeneracy QC

Date: 2026-06-18

## Purpose

Move the apparent-depth QC, apparent-depth sensitivity, and hyperbola/time-zero
degeneracy guardrails into the structured GSSI field publication bundle, then
refresh the dataset-level policy pointer. This is CPU-only reporting synthesis;
it does not launch FDTD, FWI, GPU kernels, 3D inversion, radius recovery, or
cover-depth recovery.

Superseded endpoint note: field experiment 079 / runs 090-092 add the
early-time common-mode negative-control audit. Run 091 is now the current
paper-facing field bundle, and run 092 is the current dataset policy pointer.

## Outputs

```text
088_gssi51600s_field_publication_claim_bundle_post_depth_degeneracy_qc
089_gssi51600s_field_dataset_policy_synthesis_post_depth_degeneracy_publication_bundle
```

Key artifacts:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/088_gssi51600s_field_publication_claim_bundle_post_depth_degeneracy_qc/data/field_publication_figure_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/088_gssi51600s_field_publication_claim_bundle_post_depth_degeneracy_qc/data/field_publication_claim_boundaries.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/088_gssi51600s_field_publication_claim_bundle_post_depth_degeneracy_qc/figures/field_publication_claim_bundle.png
outputs/field_experiments/local_gssi_51600s_2026_06_09/089_gssi51600s_field_dataset_policy_synthesis_post_depth_degeneracy_publication_bundle/data/field_dataset_policy_summary.json
```

## Result

Run 088 refreshes the field publication bundle:

```text
policy label:                  field_publication_claim_bundle_2d_qc_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
figure rows:                   16
claim boundaries:              15
apparent-depth QC included:    true
apparent-depth sensitivity:    true
hyperbola/time-zero degen:     true
ready for manuscript supplement true
gpu priority:                  none
```

Run 089 refreshes the dataset policy pointer:

```text
policy label:                  field_2d_qc_not_3d_or_fwi
publication bundle policy:     field_publication_claim_bundle_2d_qc_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
publication figure rows:       16
publication claim boundaries:  15
field apparent-depth policy:   field_apparent_depth_qc_relative_scale_not_cover_depth
field hyperbola/degen policy:  field_hyperbola_timezero_degeneracy_not_calibrated_inversion
```

## Interpretation

The current paper-facing field bundle is now run 088. Runs 084-086 are no
longer loose candidate figures; they are structured supplemental guardrails
inside the field publication bundle. Their claim boundaries remain negative:
relative apparent-depth scale QC is allowed, but calibrated cover-depth,
radius, 3D, and measured-data FWI recovery remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_publication_claim_bundle.py
tests/test_gssi_field_dataset_policy_synthesis.py
13 passed
```

Figure validation:

```text
088 field_publication_claim_bundle.png: 3079x903, dynamic range=255
089 field_dataset_policy.png: 12939x835, dynamic range=255
```
