# Field Experiment 109: Support Refresh After Timing Discriminant/HPC

Date: 2026-06-18

## Purpose

Refresh the measured-field event-support table after the latest timing
discriminant scorecard and 2D-only/no-HPC dimensionality decision. This keeps
the field evidence useful for manuscript support tables while preserving the
boundary that the local GSSI data are 2D line-profile QC evidence, not field
FWI, 3D inversion, radius recovery, or cover-depth recovery.

This is a synthesis over existing field outputs. It does not run FDTD, FWI,
GPU kernels, neural-network training, 3D inversion, or HPC jobs.

## Outputs

Use these refreshed endpoints:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/110_gssi51600s_field_event_support_tiers_post_timing_discriminant_hpc
outputs/field_experiments/local_gssi_51600s_2026_06_09/111_gssi51600s_field_publication_claim_bundle_post_event_support_timing_discriminant_hpc
outputs/field_experiments/local_gssi_51600s_2026_06_09/112_gssi51600s_field_dataset_policy_synthesis_post_event_support_timing_discriminant_hpc_bundle
```

Run `109_gssi51600s_field_event_support_tiers_post_timing_discriminant_hpc`
was superseded by run `110` because the table figure labels were too cramped.
The numeric table contents were unchanged; use run `110` as the clean endpoint.

## Result

Refreshed event-support table:

```text
policy label:                         field_event_support_tiers_timing_discriminant_hpc_2d_qc_ready_not_fwi
tier rows:                            11
blocked rows:                          1
short content-backed anchors:          2 / 3 event pairs
short timing-only cues:                1
long pattern-supported anchors:        8 total
short band-supported bands:            4
long pattern-supported bands:          4
timing score rows:                     4
short non-raw timing supported:       18
long short-transfer rejections:        3
HPC geometry type:                    independent_2d_line_profiles
HPC ready for 3D/FWI:                 false / false
field GPU/FWI priority:               none
```

Publication and policy refresh:

```text
publication bundle rows:              22 figures / 21 claim boundaries
publication event-support rows:       11
dataset policy:                       field_2d_qc_not_3d_or_fwi
publication bundle ready:             true
ready for 2D QC:                      true
ready for 3D/HPC/FWI:                 false
```

## Interpretation

The refreshed field table now carries the current timing-discriminant and
HPC-dimensionality evidence directly. The short pair remains the only
content-backed relative timing/QC anchor. The long pair remains pattern-only.
The field dataset remains useful for measured-data QC and supplement figures,
not as a measured inversion benchmark.

The publication bundle now points its event-support figure row at run `110`,
so downstream manuscript handoff does not accidentally cite the older run `072`
event-support table.

## Validation

Focused tests:

```text
tests/test_gssi_field_event_support_tiers.py
tests/test_gssi_field_publication_claim_bundle.py
tests/test_gssi_field_dataset_policy_synthesis.py
20 passed
```

Figure validation:

```text
110 field_event_support_tiers.png: 2314x1481, nonwhite=0.4497, dynamic range=255
111 field_publication_claim_bundle.png: 4250x903, nonwhite=0.0754, dynamic range=255
112 field_dataset_policy.png: 12939x835, nonwhite=0.2572, dynamic range=255
```
