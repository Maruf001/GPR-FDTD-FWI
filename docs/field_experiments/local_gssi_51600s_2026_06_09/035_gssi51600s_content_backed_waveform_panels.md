# Field Experiment 035: GSSI 51600S Content-Backed Waveform Panels

Date: 2026-06-17

## Purpose

Publication-oriented visual QC reducer for the two repeat-content short-profile
events accepted in field experiments 031 and 033. This run re-simulates only
the four selected field-to-synthetic snippets:

```text
pair 2 reference/comparison
pair 3 reference/comparison
```

It excludes the timing-only pair 1 and does not run field FWI, geometry
inversion, 3D reconstruction, or a broad synthetic sweep.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/035_gssi51600s_content_backed_waveform_panels
```

Artifacts:

```text
data/content_backed_waveform_panel_rows.csv
data/content_backed_waveform_panel_summary.json
data/figure_validation.csv
figures/content_backed_waveform_panels.png
run_manifest.json
```

## Inputs

```text
011_gssi51600s_field_synthetic_waveform_family_shift_epsr_probe
033_gssi51600s_short_profile_content_synthetic_policy
```

## Result

Policy label:

```text
content_backed_waveform_visual_qc
```

Summary:

```text
panel count:                 4
valid panel count:           4
content-backed pair count:   2
minimum absolute correlation: 0.8195
mean absolute correlation:    0.8566
```

Panel candidates:

| Pair | Side | Candidate | Radius | Epsr | Absolute correlation |
| ---: | --- | --- | ---: | ---: | ---: |
| 2 | comparison | `PROJECT001C__016_top_envelope_35pct_g2_r5_fitted` | 5.0 mm | 12.4395 | 0.8195 |
| 2 | reference | `PROJECT001C__014_top_envelope_35pct_g2_r8_fitted` | 8.0 mm | 9.9585 | 0.8895 |
| 3 | comparison | `PROJECT001C__016_top_envelope_35pct_g1_r5_fitted` | 5.0 mm | 12.4395 | 0.8340 |
| 3 | reference | `PROJECT001C__014_top_envelope_35pct_g3_r8_fitted` | 8.0 mm | 9.9585 | 0.8836 |

## Interpretation

This is now the preferred measured-data figure candidate for the local GSSI
short-profile bridge: it shows only repeat-content-backed events and their
best existing field-to-synthetic waveform snippets.

The result remains visual QC only. It does not support field radius,
cover-depth, geometry, 3D, or FWI claims.

## Validation

Focused tests:

```text
tests/test_gssi_field_content_backed_waveform_panels.py: 3 passed
```

The panel figure was validated as nonblank:

```text
content_backed_waveform_panels.png nonwhite=0.0716, dynamic range=255
```
