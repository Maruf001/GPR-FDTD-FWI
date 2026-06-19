# Field Experiment 132: GSSI 51600S Field Short-Anchor Signal-Contrast Sensitivity

Date: 2026-06-18

## Purpose

Test whether the run `131` signal-contrast result is robust to reasonable
aperture, event-window, and pre-event baseline choices.

This was a CPU field-QC sensitivity audit. It reloaded the same two
content-backed DZT profiles and swept 27 local contrast settings. It did not
run FDTD, FWI, GPU kernels, 3D/HPC jobs, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/132_gssi51600s_field_short_anchor_signal_contrast_sensitivity
```

Key artifacts:

```text
data/field_short_anchor_signal_contrast_sensitivity_combos.csv
data/field_short_anchor_signal_contrast_sensitivity_windows.csv
data/field_short_anchor_signal_contrast_sensitivity_summary.json
figures/field_short_anchor_signal_contrast_sensitivity.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_field_short_anchor_signal_contrast_sensitivity_qc_only
sensitivity combinations:             27
all-supported combinations:           13 / 27
default combination supported:        true
default min event/pre-event RMS:       4.129473194969804
default min peak/pre-event-p95:       12.398728731716746
worst RMS combination:                a10mm_tight_near
worst supported side windows:          2 / 4
worst min event/pre-event RMS:         1.0542762100138983
window-invariant contrast ready:       false
absolute amplitude calibration ready:  false
field FWI ready:                       false
3D/HPC ready:                          false
gpu priority:                          none
```

Interpretation: the default signal-contrast gate from run `131` is supported,
but the claim is not window-invariant. Tight event windows, especially with
near pre-event baselines, fail for some side windows. Use the result as
default-window field morphology-QC guardrail only, not as absolute amplitude
calibration, strict contrast invariance, radius/geometry/depth recovery, field
FWI, 3D/HPC, or heavy field-work evidence.

## Validation

```text
tests/test_gssi_field_short_anchor_signal_contrast_sensitivity.py
2 passed
```

Figure validation:

```text
field_short_anchor_signal_contrast_sensitivity.png: 2603x835,
nonwhite=0.4619, dynamic range=255
```
