# GSSI 51600S Field Short-Anchor Leave-One Audit

## Purpose

Audit whether the current short-profile relative time-zero claim depends on the
timing-only short anchor or whether the two content-backed short anchors alone
provide a stable measured-field QC anchor.

This is a CPU-only field-data audit over existing local GSSI summaries. It does
not run FDTD, FWI, GPU kernels, 3D/HPC jobs, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/120_gssi51600s_field_short_anchor_leave_one_audit
```

Files:

```text
data/field_short_anchor_joined_rows.csv
data/field_short_anchor_leave_one_rows.csv
data/field_short_anchor_leave_one_summary.json
figures/field_short_anchor_leave_one_audit.png
figures/FIGURE_NOTES.md
```

## Key Result

```text
policy label:                       gssi51600s_field_short_anchor_leave_one_content_redundancy_qc_only
short anchors:                      3
content-backed short anchors:       2
timing-only short anchors:          1
content-only supported:             true
content-only half-range:            0.009823 ns
all-short half-range:               0.034381 ns
content-only tighter than all-short: true
leave-one supported cases:          1 / 3
leave-one degraded cases:           2 / 3
ready for short relative timing QC: true
ready for absolute time-zero:       false
ready for field FWI:                false
ready for 3D/HPC:                   false
gpu priority:                       none
```

Interpretation: the timing-only short anchor can be removed and the two
content-backed anchors still support a narrower relative time-zero interval.
However, removing either content-backed anchor leaves only one content-backed
anchor, so the field claim is not leave-one-content redundant. The allowed use
remains short-profile relative timing QC only.

## Validation

Focused tests:

```text
tests/test_gssi_field_short_anchor_leave_one_audit.py
tests/test_local_2d_field_manuscript_table_pack.py
```

Figure validation:

```text
field_short_anchor_leave_one_audit.png: 2535x903,
nonwhite=0.1879, dynamic range=255
```
