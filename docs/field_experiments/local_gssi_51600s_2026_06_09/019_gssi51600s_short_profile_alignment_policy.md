# Field Experiment 019: GSSI 51600S Short-Profile Alignment Policy

Date: 2026-06-17

## Purpose

CPU-only profile-level alignment check for the short local GSSI profiles:

```text
PROJECT001C__014.DZT
PROJECT001C__016.DZT
```

Experiment 018 showed that the three shallow apex positions are repeatable
after a small lateral alignment, but radius choices do not repeat. This run
asks whether the whole shallow cue pattern repeats across the two profiles, and
whether direct or reversed scan orientation is preferred.

No FDTD, FWI, or GPU command was run.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/019_gssi51600s_short_profile_alignment_policy
```

Artifacts:

```text
data/profile_alignment_lag_scan.csv
data/profile_alignment_summary.csv
data/profile_alignment_policy_summary.json
data/figure_validation.csv
figures/short_profile_alignment.png
run_manifest.json
```

## Method

The reducer re-imports the DZT profiles, applies the existing preprocessing
pipeline, and builds a lateral shallow-response signature from the 95th
percentile of the envelope-anomaly cue map over:

```text
0.45-1.25 ns
```

It then scans lags up to 120 mm for both direct and reversed comparison-profile
orientation.

## Result

Best alignment:

```text
orientation:              reversed
lag:                      +83.325 mm
normalized correlation:    0.9312
alignment label:           strong_reversed_scan_preferred
```

Direct-orientation comparison:

```text
best direct lag:           +9.999 mm
best direct correlation:    0.8675
```

The reversed orientation wins by about 0.064 correlation units.

## Interpretation

Profiles 014 and 016 repeat strongly as shallow-response patterns. The best
alignment prefers reversed orientation, which is consistent with opposite scan
direction or reversed line acquisition. This is stronger field QC evidence than
the apex-only repeatability result from experiment 018.

This does not change the field boundary:

```text
Use short profiles 014/016 as repeatable shallow-response calibration/QC data.
Do not treat the local GSSI data as a 3D survey.
Do not report field radius, cover depth, geometry, or FWI recovery without
external survey layout and target metadata.
```

## Validation

The alignment figure was validated as nonblank:

```text
short_profile_alignment.png nonwhite=0.0912, dynamic range=255
```
