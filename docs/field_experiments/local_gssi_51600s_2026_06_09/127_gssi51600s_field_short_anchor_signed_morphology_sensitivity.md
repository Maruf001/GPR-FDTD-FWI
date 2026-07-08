# Field Experiment 127: GSSI 51600S Signed-Morphology Threshold Sensitivity

Date: 2026-06-18

## Purpose

Sweep signed-morphology thresholds for the two content-backed short anchors
from run `126`. This checks whether the field supplement morphology claim has
threshold margin, without promoting field inversion or radius/geometry claims.

This was a CPU saved-artifact audit. It read run `126` only. It did not run
DZT preprocessing, FDTD, FWI, GPU kernels, field inversion, 3D/HPC jobs, or
neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/127_gssi51600s_field_short_anchor_signed_morphology_sensitivity
```

Key artifacts:

```text
data/field_short_anchor_signed_morphology_sensitivity_rows.csv
data/field_short_anchor_signed_morphology_sensitivity_gates.csv
data/field_short_anchor_signed_morphology_sensitivity_summary.json
figures/field_short_anchor_signed_morphology_sensitivity.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_field_short_anchor_signed_morphology_threshold_sensitivity_qc_only
content-backed pairs:                 2
threshold combinations:               320
all-pair supported combinations:      36
all-pair supported fraction:          0.1125
default thresholds supported:         true
moderate tightening supported:        true
strict correlation supported:         false
strict all-threshold claim supported: false
corrected signed-correlation limit:   0.939469
event-local abs-correlation limit:    0.988138
correlation-improvement limit:        0.585637
timing-cap limit:                     0.019646 ns
field FWI ready:                      false
3D/HPC ready:                         false
gpu priority:                         none
```

Interpretation: the signed short-anchor morphology is not a one-point artifact:
it survives the default thresholds and a moderate tightening envelope. The
margin is finite, however. Strict correlation, stricter improvement, and tighter
timing-cap requirements fail, so the result should stay a field supplement
threshold-margin statement.

The boundary remains unchanged: this is not amplitude calibration,
radius/geometry seeding, cover-depth recovery, field FWI, 3D/HPC, or heavy
field-work evidence.

## Validation

```text
tests/test_gssi_field_short_anchor_signed_morphology_sensitivity.py
3 passed
```

Figure validation:

```text
field_short_anchor_signed_morphology_sensitivity.png: 2263x835,
nonwhite=0.2158, dynamic range=255
```
