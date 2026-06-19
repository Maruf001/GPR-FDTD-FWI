# Field Experiment 103: Dataset Policy After Timing-Window Bundle

Date: 2026-06-18

## Purpose

Refresh the dataset-level field policy so the current endpoint reads the
timing-window-aware publication bundle from experiment 102.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/103_gssi51600s_field_dataset_policy_synthesis_post_timing_window_family_bundle
```

Key artifacts:

```text
data/field_dataset_policy_evidence.csv
data/field_dataset_policy_summary.json
figures/field_dataset_policy.png
```

## Result

```text
policy label:                              field_2d_qc_not_3d_or_fwi
publication bundle figures:               20
publication bundle claim boundaries:       19
strict early near-zero timing windows:     6/6
short non-raw supported timing windows:    18/18
long windows rejecting short transfer:     3/3
publication bundle GPU priority:           none
```

## Interpretation

The field dataset remains a 2D line-profile QC and timing/repeatability
supplement. The refreshed policy explicitly keeps short relative timing, early
common-mode timing, and long pattern-only timing separate.
