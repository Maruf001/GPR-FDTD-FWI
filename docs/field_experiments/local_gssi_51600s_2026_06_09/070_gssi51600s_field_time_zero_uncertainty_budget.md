# Field Experiment 070: Relative Time-Zero Uncertainty Budget

Date: 2026-06-18

## Purpose

Synthesize the accumulated short-profile timing evidence into a manuscript-ready
relative time-zero uncertainty budget for the local GSSI 51600S field data. This
is a field-QC artifact for the 014/016 short pair only; it is not an absolute
time-zero calibration, measured-data FWI objective, 3D inversion input, radius
estimate, or cover-depth estimate.

## Outputs

```text
075_gssi51600s_field_time_zero_uncertainty_budget
076_gssi51600s_field_publication_claim_bundle_post_time_zero_budget
077_gssi51600s_field_dataset_policy_synthesis_post_time_zero_budget
```

Key artifacts:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/075_gssi51600s_field_time_zero_uncertainty_budget/data/field_time_zero_uncertainty_budget_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/075_gssi51600s_field_time_zero_uncertainty_budget/data/field_time_zero_uncertainty_budget_summary.json
outputs/field_experiments/local_gssi_51600s_2026_06_09/075_gssi51600s_field_time_zero_uncertainty_budget/figures/field_time_zero_uncertainty_budget.png
outputs/field_experiments/local_gssi_51600s_2026_06_09/076_gssi51600s_field_publication_claim_bundle_post_time_zero_budget/data/field_publication_claim_boundaries.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/077_gssi51600s_field_dataset_policy_synthesis_post_time_zero_budget/data/field_dataset_policy_summary.json
```

## Result

Run 075 builds the relative uncertainty budget:

```text
policy label:                         field_time_zero_uncertainty_budget_short_pair_relative_qc_not_absolute
budget rows:                          13
relative anchor offset:               0.127701 ns
bootstrap observed median offset:     0.117878 ns
bootstrap CI:                         0.108055 to 0.147348 ns
bootstrap CI width:                   0.039293 ns
conservative half-width:              0.058939 ns
leave-one-out max abs residual:       0.058939 ns
content anchor support:               2 / 3 event pairs
max content-anchor residual:          0.009823 ns
trace-window support:                 6 / 6
spatial all-window support fraction:  0.281124
short supported bands:                low, mid_low, mid_high, broad
absolute time-zero ready:             false
field FWI ready:                      false
field GPU/FWI priority:               none
```

Run 076 folds that budget into the paper-facing field bundle:

```text
policy label:                         field_publication_claim_bundle_2d_qc_time_zero_event_tiers_bandlimited_relaxed_ready_not_fwi
figure rows:                          11
claim boundaries:                     10
time-zero uncertainty included:        true
time-zero conservative half-width:     0.058939 ns
ready for manuscript supplement:      true
gpu priority:                         none
```

Run 077 refreshes the dataset-level policy:

```text
policy label:                         field_2d_qc_not_3d_or_fwi
publication bundle figure rows:       11
publication bundle claim boundaries:  10
publication time-zero budget:         true
publication budget half-width:        0.058939 ns
publication absolute time-zero ready: false
survey classification:                independent_2d_line_profiles
```

## Interpretation

The short 014/016 field pair now has an explicit relative timing uncertainty
budget suitable for manuscript QC language. The supported estimate is bounded by
phase-convention and bootstrap evidence, then stress-tested against content
anchors, trace alignment, B-scan stack windows, spatial support, event-support
tiers, and band-limited repeatability.

The limiting condition did not change: this is relative measured-field QC, not a
new inversion target. The field dataset still lacks recoverable 3D grid/crossline
metadata, validated field radius labels, absolute time-zero calibration, and a
measured-data FWI objective.

## Validation

Focused tests:

```text
tests/test_gssi_field_time_zero_uncertainty_budget.py
tests/test_gssi_field_publication_claim_bundle.py
tests/test_gssi_field_dataset_policy_synthesis.py
12 passed
```

Figure validation:

```text
075 field_time_zero_uncertainty_budget.png: 2654x1379, dynamic range=255
076 field_publication_claim_bundle.png: 2569x869, dynamic range=255
077 field_dataset_policy.png: 12259x835, dynamic range=255
```
