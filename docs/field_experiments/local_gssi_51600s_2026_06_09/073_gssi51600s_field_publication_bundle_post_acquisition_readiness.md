# Field Experiment 073: Publication Bundle After Acquisition Readiness

Date: 2026-06-18

## Purpose

Fold the field acquisition/HPC-readiness audit into the paper-facing GSSI field
bundle and refresh the dataset-level policy pointer. This is CPU-only field
reporting synthesis; it does not launch FDTD, FWI, GPU kernels, 3D inversion,
radius recovery, or cover-depth recovery.

## Outputs

```text
082_gssi51600s_field_publication_claim_bundle_post_acquisition_readiness
083_gssi51600s_field_dataset_policy_synthesis_post_acquisition_readiness
```

Key artifacts:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/082_gssi51600s_field_publication_claim_bundle_post_acquisition_readiness/data/field_publication_figure_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/082_gssi51600s_field_publication_claim_bundle_post_acquisition_readiness/data/field_publication_claim_boundaries.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/082_gssi51600s_field_publication_claim_bundle_post_acquisition_readiness/figures/field_publication_claim_bundle.png
outputs/field_experiments/local_gssi_51600s_2026_06_09/083_gssi51600s_field_dataset_policy_synthesis_post_acquisition_readiness/data/field_dataset_policy_summary.json
```

## Result

Run 082 refreshes the field publication bundle:

```text
policy label:                    field_publication_claim_bundle_2d_qc_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
figure rows:                     13
claim boundaries:                12
acquisition readiness included:  true
ready for manuscript supplement: true
gpu priority:                    none
```

Run 083 refreshes the dataset policy pointer:

```text
policy label:                    field_2d_qc_not_3d_or_fwi
publication bundle policy:       field_publication_claim_bundle_2d_qc_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
publication figure rows:         13
publication claim boundaries:    12
acquisition readiness included:  true
ready for 3D HPC:                false
ready for field FWI:             false
field HPC priority:              none
```

## Interpretation

The current paper-facing field bundle now includes the acquisition/HPC-readiness
figure and claim boundary. The field dataset remains useful as dense 2D
line-profile timing/repeatability QC and remains blocked for field FWI, 3D
inversion, radius recovery, and cover-depth claims.

## Validation

Focused tests:

```text
tests/test_gssi_field_publication_claim_bundle.py
tests/test_gssi_field_dataset_policy_synthesis.py
12 passed
```

Figure validation:

```text
082 field_publication_claim_bundle.png: 2569x869, dynamic range=255
083 field_dataset_policy.png: 12259x835, dynamic range=255
```
