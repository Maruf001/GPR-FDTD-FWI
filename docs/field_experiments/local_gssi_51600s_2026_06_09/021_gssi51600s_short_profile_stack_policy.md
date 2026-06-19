# Field Experiment 021: GSSI 51600S Short-Profile Stack Policy

Date: 2026-06-17

## Purpose

CPU-only repeat-aligned stack analysis for the two short local GSSI profiles:

```text
PROJECT001C__014.DZT
PROJECT001C__016.DZT
```

Experiment 019 showed that the whole shallow-response pattern repeats best when
profile 016 is reversed and shifted by about 83 mm. This run uses that reversed
alignment to stack the shallow cue signatures and to re-pair the phase-anchor
events. It does not run FDTD, FWI, or GPU kernels.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/021_gssi51600s_short_profile_stack_policy
```

Artifacts:

```text
data/short_profile_stack_lag_scan.csv
data/short_profile_stack_signal.csv
data/short_profile_stack_anchor_candidates.csv
data/short_profile_reversed_event_pairs.csv
data/short_profile_stack_policy_summary.json
data/figure_validation.csv
figures/short_profile_stack_policy.png
run_manifest.json
```

## Result

Alignment:

```text
best orientation:             reversed
best lag:                     +83.325 mm
normalized correlation:        0.9312
alignment label:               strong_reversed_scan_preferred
```

Stable stack anchors:

| Candidate | x | Stack z | Repeat delta z | Label |
| ---: | ---: | ---: | ---: | --- |
| 1 | 396.6 mm | 10.2020 | 0.5072 | `stable_stack_anchor` |
| 2 | 703.3 mm | 10.9257 | 0.4467 | `stable_stack_anchor` |

Reversed event pairing:

| Pair | Reference event | Comparison event | x residual | Phase-time delta | Radius match |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | 014 g1 | 016 g3 | -10.0 mm | +0.1768 ns | no |
| 2 | 014 g2 | 016 g2 | -10.0 mm | +0.1081 ns | no |
| 3 | 014 g3 | 016 g1 | +20.0 mm | +0.1277 ns | no |

Summary:

```text
stable stack anchors:                         2
event pairs:                                  3
mean absolute aligned event residual:         13.332 mm
max absolute aligned event residual:          19.998 mm
median comparison-minus-reference phase time: +0.1277 ns
mean absolute phase-time delta:               0.1375 ns
radius matches:                               0 of 3
policy label:                                 repeat_stack_limited_qc
```

## Interpretation

The reversed stack strengthens the field QC result. The short profiles contain
a repeatable shallow-response structure, and reversed event pairing improves the
event-position residuals compared with the earlier order-only repeatability
view.

The result is still limited. Only two stable stack anchors pass the repeat
threshold, and none of the three paired events agree on radius. The local GSSI
data therefore remains useful for timing/repeatability QC, not field geometry,
radius, cover-depth, 3D survey, or FWI claims.

Current field policy:

```text
Use profiles 014/016 as repeat-aligned 2D line-profile QC evidence.
Use the reversed stack to support timing-anchor discussion.
Do not report field radius, cover depth, field FWI recovery, or 3D inversion
from this dataset without external survey and target metadata.
```

## Validation

The stack-policy figure was validated as nonblank:

```text
short_profile_stack_policy.png nonwhite=0.1421, dynamic range=255
```
