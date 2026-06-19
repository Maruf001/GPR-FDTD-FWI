# Field Experiment 126: GSSI 51600S Short-Anchor Signed-Morphology Audit

Date: 2026-06-18

## Purpose

Audit whether the content-backed short-anchor waveform evidence remains
same-polarity after relative timing correction. This follows run `124`
waveform-coherence QC and run `125` radius-degeneracy analysis.

This was a CPU saved-artifact audit. It read runs `039`, `124`, and `125`
only. It did not run DZT preprocessing, FDTD, FWI, GPU kernels, field
inversion, 3D/HPC jobs, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/126_gssi51600s_field_short_anchor_signed_morphology_audit
```

Key artifacts:

```text
data/field_short_anchor_signed_morphology_rows.csv
data/field_short_anchor_signed_morphology_gates.csv
data/field_short_anchor_signed_morphology_summary.json
figures/field_short_anchor_signed_morphology_audit.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_field_short_anchor_signed_morphology_qc_only
content-backed pairs:                 2
signed morphology supported pairs:    2 / 2
corrected same-polarity pairs:        2 / 2
raw same-polarity pairs:              2 / 2
min corrected signed correlation:     0.939469
mean corrected signed correlation:    0.963803
min raw signed correlation:           0.248836
min event-local abs correlation:      0.988138
min abs correlation improvement:      0.585637
max corrected timing residual:        0.019646 ns
max corrected trace residual RMS:     0.347941
weak radius sides:                    4
selected radius mismatch pairs:       2
common-radius near-tie pairs:         2
signed morphology QC ready:           true
absolute amplitude calibration ready: false
radius seed ready:                    false
geometry seed ready:                  false
field FWI ready:                      false
3D/HPC ready:                         false
gpu priority:                         none
```

Interpretation: the content-backed short anchors keep same-polarity,
high-correlation waveform morphology after the relative timing correction. This
strengthens the positive field supplement claim from absolute waveform
resemblance to signed morphology QC.

The boundary remains strict: the traces are robust-normalized, radius remains
weak and near-tied, and spatial/depth controls remain unavailable. Do not use
this as amplitude calibration, radius/geometry seeding, cover-depth recovery,
field FWI, 3D/HPC, or heavy field-work evidence.

## Validation

```text
tests/test_gssi_field_short_anchor_signed_morphology_audit.py
3 passed
```

Figure validation:

```text
field_short_anchor_signed_morphology_audit.png: 2263x835,
nonwhite=0.2619, dynamic range=255
```
