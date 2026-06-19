# Field Experiment 041: GSSI 51600S Content Anchor Trace Alignment Sensitivity

Date: 2026-06-17

## Purpose

CPU-only window-sensitivity check for field experiment 039. This reruns the
measured 014/016 content-anchor trace-alignment comparison across short,
nominal, and wider time windows.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/041_gssi51600s_content_anchor_trace_alignment_sensitivity
```

Artifacts:

```text
data/content_anchor_trace_alignment_sensitivity_summary.json
data/content_anchor_trace_alignment_sensitivity_windows.csv
data/content_anchor_trace_alignment_sensitivity_pairs.csv
data/figure_validation.csv
figures/content_anchor_trace_alignment_sensitivity.png
run_manifest.json
```

## Result

Policy label:

```text
content_anchor_trace_alignment_window_robust
```

Summary:

```text
windows tested:                    3
pair-window rows:                  6
improved pair-window rows:         6
minimum abs-correlation improvement: 0.3629
mean abs-correlation improvement:    0.5316
minimum corrected abs correlation:   0.9209
```

Window-level result:

| Window | Mean raw | Mean corrected | Mean improvement |
| --- | ---: | ---: | ---: |
| 0.16 / 0.24 ns | 0.5031 | 0.9542 | 0.4511 |
| 0.24 / 0.36 ns | 0.3013 | 0.9638 | 0.6625 |
| 0.32 / 0.48 ns | 0.5065 | 0.9878 | 0.4813 |

## Interpretation

The measured trace-alignment improvement from field experiment 039 is not a
single-window artifact. Both content anchors improve under every tested window,
and the corrected traces remain strongly correlated.

This remains measured-data phase/time-zero and visual-QC evidence only. It does
not support field radius, cover-depth, geometry, 3D, or FWI claims.

## Validation

Focused tests:

```text
tests/test_gssi_field_content_anchor_trace_alignment_sensitivity.py: 4 passed
```

Figure validation:

```text
content_anchor_trace_alignment_sensitivity.png: 2229x835,
nonwhite=0.3541, dynamic range=255
```
