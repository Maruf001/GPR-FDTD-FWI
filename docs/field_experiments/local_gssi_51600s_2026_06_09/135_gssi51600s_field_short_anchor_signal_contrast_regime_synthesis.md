# Field Experiment 135: Short-Anchor Signal-Contrast Regime Synthesis

Date: 2026-06-18

## Purpose

Summarize the run `132` signal-contrast sensitivity table by regime. This
separates the defensible broad-event-window morphology claim from the blocked
strict window-invariant/amplitude-calibration claim.

This is CPU-only field synthesis. It does not run FDTD, FWI, GPU kernels,
3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/135_gssi51600s_field_short_anchor_signal_contrast_regime_synthesis
```

Key artifacts:

```text
data/field_short_anchor_signal_contrast_regime_summary.json
data/field_short_anchor_signal_contrast_regime_event_rows.csv
data/field_short_anchor_signal_contrast_regime_aperture_rows.csv
data/field_short_anchor_signal_contrast_regime_noise_rows.csv
data/field_short_anchor_signal_contrast_regime_gates.csv
figures/field_short_anchor_signal_contrast_regime_synthesis.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_field_short_anchor_signal_contrast_regime_synthesis_qc_only
sensitivity combos:                   27
all-supported combos:                 13
all-supported combo fraction:          0.481481481
broad event combos supported:          9 / 9
broad event min RMS ratio:             5.051403727
broad event min peak/p95 ratio:        11.312450857
default event all-supported fraction:  4 / 9
tight event all-supported fraction:    0 / 9
broad event contrast regime ready:     true
strict window-invariant contrast:      false
absolute amplitude calibration ready:  false
field FWI ready:                       false
3D/HPC ready:                          false
gpu priority:                          none
```

## Interpretation

Run `135` strengthens the field supplement without overclaiming. The broad
event window is robust across all tested aperture and pre-event baseline
settings, with minimum event/pre-event RMS ratio 5.05x. Tight windows fail
completely and default windows are mixed, so the field claim must remain a
broad-window morphology-contrast regime rather than strict window-invariant
contrast or amplitude calibration.

This keeps cover-depth/radius recovery, field FWI, 3D/HPC, and heavy field
work blocked.

## Validation

```text
tests/test_gssi_field_short_anchor_signal_contrast_regime_synthesis.py
2 passed
```

Figure validation:

```text
field_short_anchor_signal_contrast_regime_synthesis.png: 2433x818,
nonwhite=0.2778, dynamic range=255
```
