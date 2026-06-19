# Field Experiment 069: Event-Support Tiers and Bundle Refresh

Date: 2026-06-18

## Purpose

Convert the accumulated field QC evidence into a compact measured-event support
tier table. This is meant to make the field contribution easier to use in a
paper supplement without overstating the data as field FWI, 3D inversion,
radius recovery, or cover-depth recovery.

## Outputs

```text
072_gssi51600s_field_event_support_tiers
073_gssi51600s_field_publication_claim_bundle_post_event_support_tiers
074_gssi51600s_field_dataset_policy_synthesis_post_event_support_bundle
```

Key artifacts:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/072_gssi51600s_field_event_support_tiers/data/field_event_support_tiers.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/072_gssi51600s_field_event_support_tiers/data/field_event_support_tiers_summary.json
outputs/field_experiments/local_gssi_51600s_2026_06_09/072_gssi51600s_field_event_support_tiers/figures/field_event_support_tiers.png
outputs/field_experiments/local_gssi_51600s_2026_06_09/073_gssi51600s_field_publication_claim_bundle_post_event_support_tiers/data/field_publication_claim_boundaries.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/074_gssi51600s_field_dataset_policy_synthesis_post_event_support_bundle/data/field_dataset_policy_summary.json
```

## Result

Run 072 builds the measured-field event-support tier table:

```text
policy label:                         field_event_support_tiers_2d_qc_ready_not_fwi
tier rows:                            9
blocked rows:                         1
short content-backed anchors:         2 / 3 event pairs
short timing-only cues:               1
long pattern-supported anchors:       8 total
short band-supported bands:           4
long pattern-supported bands:         4
survey classification:                independent_2d_line_profiles
field GPU/FWI priority:               none
```

Run 073 folds that support table into the paper-facing field bundle:

```text
policy label:                         field_publication_claim_bundle_2d_qc_event_tiers_bandlimited_relaxed_ready_not_fwi
figure rows:                          10
claim boundaries:                     9
event-support tiers included:         true
ready for manuscript supplement:      true
gpu priority:                         none
```

Run 074 refreshes the dataset-level policy:

```text
policy label:                         field_2d_qc_not_3d_or_fwi
publication bundle figure rows:       10
publication bundle claim boundaries:  9
publication bundle policy:            field_publication_claim_bundle_2d_qc_event_tiers_bandlimited_relaxed_ready_not_fwi
survey classification:                independent_2d_line_profiles
```

## Interpretation

The field dataset is useful for measured-data QC and manuscript supplement
evidence:

```text
short 014/016: content-backed relative time-zero visual QC for 2 of 3 event pairs
short 014/016: one timing-only cue remains limited
long 015/013: pattern-only support across stable and repeat-limited anchors
all profiles: no recoverable 3D grid/crossline geometry
```

This strengthens the field side as a controlled QC supplement, not as a field
inversion benchmark. The blocking conditions are still explicit: missing survey
grid metadata, missing long-profile phase anchors, no validated radius labels,
and no measured-data FWI objective.

## Validation

Focused tests:

```text
tests/test_gssi_field_event_support_tiers.py
tests/test_gssi_field_publication_claim_bundle.py
tests/test_gssi_field_dataset_policy_synthesis.py
11 passed
```

Figure validation:

```text
072 field_event_support_tiers.png: 2314x1243, dynamic range=255
073 field_publication_claim_bundle.png: 2569x869, dynamic range=255
074 field_dataset_policy.png: 12259x835, dynamic range=255
```
