# Field Experiment 033: GSSI 51600S Short-Profile Content-Synthetic Policy

Date: 2026-06-17

## Purpose

CPU-only reducer that joins the short-profile repeat-content classification from
field experiment 031 with the field-to-synthetic waveform-family candidates from
field experiment 011.

This run asks whether the repeat-content event pairs also have plausible
field-to-synthetic waveform support under the already tested
`top_envelope_35pct` convention. It does not run FDTD, FWI, GPU kernels, 3D
reconstruction, or field geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/033_gssi51600s_short_profile_content_synthetic_policy
```

Artifacts:

```text
data/short_profile_content_synthetic_event_matches.csv
data/short_profile_content_synthetic_policy_summary.json
data/figure_validation.csv
figures/short_profile_content_synthetic_policy.png
run_manifest.json
```

## Inputs

```text
011_gssi51600s_field_synthetic_waveform_family_shift_epsr_probe
031_gssi51600s_short_profile_content_window_policy
```

## Result

Policy label:

```text
content_backed_field_to_synthetic_qc_supported
```

Summary:

```text
event pairs:                              3
content-backed event pairs:               2
content-backed waveform-supported pairs:  2
timing-only event pairs:                  1
timing-only waveform-supported pairs:     1
minimum absolute-correlation threshold:   0.8000
minimum content-backed pair correlation:  0.8195
minimum timing-only pair correlation:     0.8103
```

Event-level waveform support:

| Pair | Content label | Reference candidate | Comparison candidate | Pair min | Pair mean | Waveform support |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 1 | `timing_only_no_stable_content_anchor` | `PROJECT001C__014_top_envelope_35pct_g1_r6_fitted` | `PROJECT001C__016_top_envelope_35pct_g3_r5_fitted` | 0.8103 | 0.8344 | `timing_only_waveform_supported_limited` |
| 2 | `repeat_content_anchor` | `PROJECT001C__014_top_envelope_35pct_g2_r8_fitted` | `PROJECT001C__016_top_envelope_35pct_g2_r5_fitted` | 0.8195 | 0.8545 | `content_backed_waveform_supported_qc` |
| 3 | `repeat_content_anchor` | `PROJECT001C__014_top_envelope_35pct_g3_r8_fitted` | `PROJECT001C__016_top_envelope_35pct_g1_r5_fitted` | 0.8340 | 0.8588 | `content_backed_waveform_supported_qc` |

## Interpretation

The two repeat-content anchors from field experiment 031 are also supported by
the best available synthetic waveform-family candidates from field experiment
011. That makes event pairs 2 and 3 the preferred measured-data examples for
later visual field-to-synthetic comparison.

Event pair 1 also clears the waveform correlation threshold, but it remains
timing-only because it lacks a stable repeat-content anchor. It should not be
used as equal evidence in a field-data figure.

This result is useful field QC only. It does not support field radius,
cover-depth, geometry, 3D, or FWI claims.

## Validation

Focused tests:

```text
tests/test_gssi_field_short_profile_content_synthetic_policy.py: 3 passed
```

The content-synthetic policy figure was validated as nonblank:

```text
short_profile_content_synthetic_policy.png nonwhite=0.4185, dynamic range=255
```
