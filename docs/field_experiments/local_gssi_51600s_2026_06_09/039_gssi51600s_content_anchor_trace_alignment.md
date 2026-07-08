# Field Experiment 039: GSSI 51600S Content Anchor Trace Alignment

Date: 2026-06-17

## Purpose

CPU-only measured-trace check for the two content-backed short-profile anchors
accepted in field experiments 037 and 038. This run extracts real
`PROJECT001C__014.DZT` and `PROJECT001C__016.DZT` traces at the supported
content anchors and compares field-to-field waveform agreement before and
after applying the relative time-zero transfer.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/039_gssi51600s_content_anchor_trace_alignment
```

Artifacts:

```text
data/content_anchor_trace_alignment_rows.csv
data/content_anchor_trace_alignment_summary.json
data/figure_validation.csv
figures/content_anchor_trace_alignment.png
run_manifest.json
```

## Result

Policy label:

```text
content_anchor_field_trace_alignment_improves_after_time_zero
```

Summary:

```text
supported content anchor pairs: 2
improved field-trace pairs:    2
mean raw abs correlation:      0.3013
mean corrected abs correlation:0.9638
mean improvement:              0.6625
max corrected timing residual: 0.01965 ns
```

Pair-level result:

| Pair | Raw abs corr | Corrected abs corr | Improvement |
| ---: | ---: | ---: | ---: |
| 2 | 0.3538 | 0.9395 | 0.5856 |
| 3 | 0.2488 | 0.9881 | 0.7393 |

## Interpretation

This is the strongest measured-data support so far for the short-profile
relative time-zero anchor: the same accepted content events become much more
similar in measured field traces after the relative transfer is applied.

The result remains measured-data timing and visual-QC evidence only. It does
not support field radius, cover-depth, geometry, 3D, or FWI claims.

## Validation

Focused tests:

```text
tests/test_gssi_field_content_anchor_trace_alignment.py: 3 passed
```

Figure validation:

```text
content_anchor_trace_alignment.png: 2263x1447,
nonwhite=0.0802, dynamic range=255
```
