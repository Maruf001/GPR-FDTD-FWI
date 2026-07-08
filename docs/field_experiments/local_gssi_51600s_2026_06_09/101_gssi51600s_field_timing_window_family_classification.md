# Field Experiment 101: Timing-Window Family Classification

Date: 2026-06-18

## Purpose

Classify the measured-field timing evidence by window family without running
field FWI, 3D inversion, or new GPU simulations. The goal is to keep three
timing anchors separate:

- early/direct/ringdown windows as common-mode negative controls
- short-profile content windows as relative timing support
- long-profile windows as pattern-only evidence that should not inherit the
  short-pair correction

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/101_gssi51600s_field_timing_window_family_classification
```

Key artifacts:

```text
data/field_timing_window_family_rows.csv
data/field_timing_window_family_classification_summary.json
figures/field_timing_window_family_classification.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         field_timing_window_family_classification_ready_not_absolute
strict early near-zero lags:          6/6
short non-raw supported windows:      18/18
raw/no-correction supported windows:  0/3
long windows rejecting short transfer: 3/3
absolute time-zero ready:             false
field FWI ready:                      false
gpu priority:                         none
```

## Interpretation

This strengthens the field timing boundary. The early window family behaves as
a near-zero common-mode control; the short content-window family supports the
relative correction; and the long profile rejects transferring that short-pair
correction. The result is manuscript-useful timing scope evidence, not an
absolute time-zero calibration or inversion input.
