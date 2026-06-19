# Field Experiment 121: GSSI 51600S Field Time-Zero Ladder Post Leave-One

Date: 2026-06-18

## Purpose

Promote the short-anchor leave-one/content-only audit into the measured-field
time-zero evidence ladder. This run keeps the field data scoped to local
short-profile relative timing QC and does not launch field FWI, 3D/HPC, neural
network training, or broad GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/121_gssi51600s_field_time_zero_ladder_post_leave_one
```

Key artifacts:

```text
data/field_time_zero_evidence_ladder_rows.csv
data/field_time_zero_evidence_ladder_summary.json
figures/field_time_zero_ladder_post_leave_one.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_field_time_zero_evidence_ladder_post_leave_one_short_qc_only
ladder rows:                          8
ready for short relative timing QC:   true
ready for content-only short QC:      true
ready for leave-one content claim:    false
ready for long short-transfer:        false
ready for absolute time-zero:         false
ready for field FWI:                  false
ready for 3D HPC:                     false
short relative offset:                0.127701 ns
short conservative half-width:        0.058939 ns
content-only half-range:              0.009823 ns
all-short half-range:                 0.034381 ns
leave-one supported cases:            1 / 3
leave-one degraded cases:             2 / 3
short anchors inside supported interval: 3
long pattern anchors rejecting transfer: 8
gpu priority:                         none
```

Interpretation: the timing-only short anchor can be dropped and the two
content-backed short anchors still support the short-profile relative timing
QC claim with a narrower interval. The result is not leave-one-content
redundant because removing either content-backed anchor leaves only one
content-backed anchor. Field use remains short-profile relative timing QC, not
absolute time-zero, cover-depth recovery, radius recovery, field FWI, 3D, or
HPC.

## Validation

```text
tests/test_gssi_field_time_zero_ladder_post_leave_one.py
2 passed
```

Figure validation:

```text
field_time_zero_ladder_post_leave_one.png: 2535x903,
nonwhite=0.2474, dynamic range=255
```
