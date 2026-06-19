# Field Experiment 037: GSSI 51600S Content Time-Zero Anchor Policy

Date: 2026-06-17

## Purpose

CPU-only synthesis of the accepted short-profile repeat-content evidence from
field experiments 031, 033, and 035. This run quantifies whether the
content-backed events are stable enough to serve as measured-data time-zero and
visual-QC anchors.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/037_gssi51600s_content_time_zero_anchor_policy
```

Artifacts:

```text
data/short_profile_content_time_zero_anchor_rows.csv
data/short_profile_content_time_zero_anchor_summary.json
data/figure_validation.csv
figures/short_profile_content_time_zero_anchor_policy.png
run_manifest.json
```

## Result

Policy label:

```text
short_profile_content_time_zero_anchor_supported_for_visual_qc
```

Summary:

```text
event pairs:                         3
content-backed event pairs:          2
supported content anchor pairs:      2
timing-only event pairs:             1
max content timing residual:         0.009823 ns
max all-event timing residual:       0.058939 ns
minimum content-pair abs correlation: 0.819494
max content panel residual RMS:      0.629150
```

Pair decisions:

| Pair | Decision | Residual to bootstrap median | Min abs correlation |
| ---: | --- | ---: | ---: |
| 1 | `timing_only_no_content_anchor` | 0.058939 ns | 0.810335 |
| 2 | `content_time_zero_anchor_supported` | 0.009823 ns | 0.819494 |
| 3 | `content_time_zero_anchor_supported` | 0.009823 ns | 0.833996 |

## Interpretation

The two repeat-content short-profile pairs are now explicitly quantified as
measured-data time-zero and visual-QC anchors. The timing-only pair remains
excluded from content-backed anchor evidence even though it has waveform
support.

This supports measured-data QC figures and timing discussion only. It does not
support field radius, cover-depth, geometry, 3D, or FWI claims.

## Validation

Focused tests:

```text
tests/test_gssi_field_content_time_zero_anchor_policy.py: 3 passed
```

Figure validation:

```text
short_profile_content_time_zero_anchor_policy.png: 2195x835,
nonwhite=0.3205, dynamic range=255
```
