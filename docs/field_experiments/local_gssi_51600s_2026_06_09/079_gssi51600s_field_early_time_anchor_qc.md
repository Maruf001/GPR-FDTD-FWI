# Field Experiment 079: Early-Time Anchor Negative QC

Date: 2026-06-18

## Purpose

Test whether the early direct/ringdown/common-mode portion of the local GSSI
51600S traces can serve as a time-zero anchor, then move the result into the
structured field publication bundle and dataset policy pointer. This is a
CPU-only field-data audit; it does not launch FDTD, FWI, GPU kernels, 3D
inversion, radius recovery, or cover-depth recovery.

## Outputs

```text
090_gssi51600s_field_early_time_anchor_audit
091_gssi51600s_field_publication_claim_bundle_post_early_time_anchor_qc
092_gssi51600s_field_dataset_policy_synthesis_post_early_time_anchor_bundle
```

Key artifacts:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/090_gssi51600s_field_early_time_anchor_audit/data/field_early_time_anchor_audit_summary.json
outputs/field_experiments/local_gssi_51600s_2026_06_09/090_gssi51600s_field_early_time_anchor_audit/data/field_early_time_pair_lags.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/090_gssi51600s_field_early_time_anchor_audit/figures/field_early_time_anchor_audit.png
outputs/field_experiments/local_gssi_51600s_2026_06_09/091_gssi51600s_field_publication_claim_bundle_post_early_time_anchor_qc/data/field_publication_figure_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/092_gssi51600s_field_dataset_policy_synthesis_post_early_time_anchor_bundle/data/field_dataset_policy_summary.json
```

## Result

Run 090:

```text
policy label:                         field_early_time_common_mode_not_content_time_zero
primary early window:                 0.00-0.55 ns
early peak median time:               0.235756 ns
early peak time span across profiles: 0.000000 ns
short 014/016 early lag:              0.000000 ns
short 014/016 early correlation:      0.999798
content-backed short offset:          0.127701 ns
conservative half-width:              0.058939 ns
early/content delta:                  0.127701 ns
early agrees with content budget:     false
long 015/013 early lag:               0.000000 ns
long pattern offset:                  0.060000 ns
absolute time-zero ready:             false
field FWI ready:                      false
gpu priority:                         none
```

Run 091:

```text
policy label:          field_publication_claim_bundle_2d_qc_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
figure rows:           17
claim boundaries:      16
early-time included:   true
ready for manuscript:  true
gpu priority:          none
```

Run 092:

```text
policy label:                  field_2d_qc_not_3d_or_fwi
publication bundle policy:     field_publication_claim_bundle_2d_qc_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
publication figure rows:       17
publication claim boundaries:  16
early-time absolute ready:     false
field gpu/fwi priority:        none
```

## Interpretation

The early common-mode/direct-wave structure is repeatable across the profiles,
but it aligns at zero lag for the short 014/016 pair. That contradicts the
content-backed relative offset of 0.127701 ns by more than the conservative
0.058939 ns half-width. The correct use is therefore negative QC: the early
component is useful for instrument/common-mode sanity checks, but not for
absolute time-zero calibration and not as a replacement for the content-backed
short-pair timing policy.

Run 091 was the early-time paper-facing field bundle endpoint and run 092 was
the paired dataset policy refresh. They are now superseded by the cue-spacing
aware run 095 bundle and run 096 policy refresh. The field dataset remains 2D
line-profile QC only, not measured-data FWI, 3D inversion, calibrated
cover-depth, or radius recovery.

## Validation

Focused tests:

```text
tests/test_gssi_field_early_time_anchor_audit.py
tests/test_gssi_field_publication_claim_bundle.py
tests/test_gssi_field_dataset_policy_synthesis.py
17 passed
```

Figure validation:

```text
090 field_early_time_anchor_audit.png: 2909x971, dynamic range=255
091 field_publication_claim_bundle.png: 3079x903, dynamic range=255
092 field_dataset_policy.png: 12939x835, dynamic range=255
```
