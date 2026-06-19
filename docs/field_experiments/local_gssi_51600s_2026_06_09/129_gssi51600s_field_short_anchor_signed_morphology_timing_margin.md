# Field Experiment 129: GSSI 51600S Field Short-Anchor Signed-Morphology Timing Margin

Date: 2026-06-18

## Purpose

Compare the signed short-anchor morphology timing residuals with the current
field time-zero uncertainty ladder. This asks whether the positive signed
morphology result from run `126` survives plausible extra timing uncertainty.

This was a CPU saved-artifact audit. It read runs `121`, `126`, and `127` only.
It did not run DZT preprocessing, FDTD, FWI, GPU kernels, 3D/HPC jobs, or
neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/129_gssi51600s_field_short_anchor_signed_morphology_timing_margin
```

Key artifacts:

```text
data/field_short_anchor_signed_morphology_timing_margin_rows.csv
data/field_short_anchor_signed_morphology_timing_margin_summary.json
figures/field_short_anchor_signed_morphology_timing_margin.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_field_short_anchor_signed_morphology_timing_margin_qc_only
content pairs:                         2
signed morphology supported pairs:      2
default timing cap:                    0.05 ns
moderate timing cap:                   0.02 ns
max corrected timing residual:         0.01964636542239684 ns
min default timing slack:              0.030353634577603164 ns
min moderate timing slack:             0.0003536345776031617 ns
content-only time-zero half-range:     0.00982318271119842 ns
conservative short half-width:         0.058939096267190516 ns
default slack covers content pairs:    2 / 2
default slack covers conservative:      0 / 2
moderate slack covers content pairs:    1 / 2
content-only morphology timing QC:     true
conservative timing morphology claim:  false
absolute time-zero ready:              false
field FWI ready:                       false
3D/HPC ready:                          false
gpu priority:                          none
```

Interpretation: the signed morphology result has enough slack under the default
0.05 ns timing cap to cover the content-only short-profile timing half-range,
but it does not cover the conservative all-short timing half-width. Use this as
content-only timing-margin support for field morphology QC, not as absolute
time-zero, conservative timing, field FWI, 3D/HPC, radius/geometry recovery, or
heavy field-work evidence.

## Validation

```text
tests/test_gssi_field_short_anchor_signed_morphology_timing_margin.py
2 passed
```

Figure validation:

```text
field_short_anchor_signed_morphology_timing_margin.png: 2263x835,
nonwhite=0.1811, dynamic range=255
```
