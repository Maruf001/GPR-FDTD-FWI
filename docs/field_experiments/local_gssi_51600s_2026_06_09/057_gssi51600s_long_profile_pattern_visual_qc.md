# Field Experiment 057: GSSI 51600S Long-Profile Pattern Visual QC

Date: 2026-06-17

## Purpose

CPU-only visual-QC package for the long-profile 015/013 pair using the robust
pattern-only +0.06 ns shift from field experiments 053 and 055.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/057_gssi51600s_long_profile_pattern_visual_qc
```

Artifacts:

```text
data/long_profile_pattern_visual_qc_rows.csv
data/long_profile_pattern_visual_qc_summary.json
data/figure_validation.csv
figures/long_profile_pattern_visual_qc.png
run_manifest.json
```

## Result

Policy label:

```text
long_profile_pattern_visual_qc_ready
```

Summary:

```text
pattern shift:                    +0.060000 ns
selected anchor windows:           6
supported anchor windows:          6
minimum pattern-shift gain:        0.019532
mean pattern-shift gain:           0.131072
minimum shifted abs correlation:   0.889509
mean shifted abs correlation:      0.956439
```

## Interpretation

This is a long-profile pattern-QC figure endpoint only. It supports showing the
015/013 shallow pattern after the robust +0.06 ns alignment, but it does not
turn the long pair into phase/time-zero, field inversion, 3D, radius, or
cover-depth evidence.

The reason is unchanged: profile 013 lacks phase-anchor picks.

## Validation

Focused tests:

```text
tests/test_gssi_field_long_profile_pattern_visual_qc.py: 3 passed
```

Figure validation:

```text
long_profile_pattern_visual_qc.png: 2602x2875,
nonwhite=0.5058, dynamic range=255
```
