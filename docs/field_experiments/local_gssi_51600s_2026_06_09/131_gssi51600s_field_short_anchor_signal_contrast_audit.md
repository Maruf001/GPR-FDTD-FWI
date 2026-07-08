# Field Experiment 131: GSSI 51600S Field Short-Anchor Signal-Contrast Audit

Date: 2026-06-18

## Purpose

Check whether the two content-backed short-anchor event windows have enough
local signal contrast to support the field morphology-QC claim from runs
`124-129`.

This was a CPU field-QC audit. It reloaded the two relevant DZT profiles,
applied the existing background-removal preprocessing, and compared each
aligned event window with a local pre-event baseline. It did not run FDTD,
FWI, GPU kernels, 3D/HPC jobs, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/131_gssi51600s_field_short_anchor_signal_contrast_audit
```

Key artifacts:

```text
data/field_short_anchor_signal_contrast_rows.csv
data/field_short_anchor_signal_contrast_summary.json
figures/field_short_anchor_signal_contrast_audit.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_field_short_anchor_signal_contrast_qc_only
content pairs:                         2
side windows:                          4
signal-contrast supported windows:     4 / 4
min event/pre-event RMS ratio:         4.129473194969804
min event/pre-event RMS dB:           12.317893027750134
min peak/pre-event-p95 ratio:         12.398728731716746
signal contrast QC ready:              true
signed morphology QC ready:            true
timing-margin QC ready:                true
absolute amplitude calibration ready:  false
field FWI ready:                       false
3D/HPC ready:                          false
gpu priority:                          none
```

Interpretation: the content-backed short-anchor event windows are not
low-contrast artifacts; all four reference/aligned-comparison windows clear the
local pre-event contrast gate. This strengthens the field morphology-QC
supplement claim. It is not absolute amplitude calibration, radius/geometry
seeding, cover-depth recovery, field FWI, 3D/HPC, or heavy field-work evidence.

## Validation

```text
tests/test_gssi_field_short_anchor_signal_contrast_audit.py
3 passed
```

Figure validation:

```text
field_short_anchor_signal_contrast_audit.png: 2263x835,
nonwhite=0.2221, dynamic range=255
```
