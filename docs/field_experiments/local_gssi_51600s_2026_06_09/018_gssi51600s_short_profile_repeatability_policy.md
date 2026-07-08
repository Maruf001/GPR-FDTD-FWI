# Field Experiment 018: GSSI 51600S Short-Profile Repeatability Policy

Date: 2026-06-17

## Purpose

CPU-only repeatability reduction for the two short local GSSI profiles:

```text
PROJECT001C__014.DZT
PROJECT001C__016.DZT
```

This run asks whether the shallow events used in the accepted timing policy are
repeatable across profiles. It reads existing phase-anchor and identifiability
tables only; it does not run FDTD, FWI, or GPU kernels.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/018_gssi51600s_short_profile_repeatability_policy
```

Artifacts:

```text
data/short_profile_event_table.csv
data/short_profile_summary.csv
data/short_profile_pair_repeatability.csv
data/short_profile_spacing_repeatability.csv
data/short_profile_repeatability_policy_summary.json
data/figure_validation.csv
figures/short_profile_repeatability.png
run_manifest.json
```

## Result

The accepted phase convention was:

```text
top_envelope_35pct
```

Profile summaries:

| Profile | Events | Mean spacing | Spacing CV | Mean phase time | Mean fitted depth | Radius mode | Mean best `|corr|` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `PROJECT001C__014.DZT` | 3 | 281.6 mm | 0.0296 | 0.5108 ns | 27.1 mm | 8 mm, 2/3 | 0.8772 |
| `PROJECT001C__016.DZT` | 3 | 296.6 mm | 0.0787 | 0.6483 ns | 34.4 mm | 5 mm, 3/3 | 0.8213 |

Paired-profile repeatability:

```text
event pairs:                     3
median lateral alignment shift:  +13.3 mm
mean aligned x residual:          15.6 mm
max aligned x residual:           30.0 mm
mean adjacent-spacing delta:      31.7 mm
max adjacent-spacing delta:       46.7 mm
mean phase-time delta:             0.138 ns
radius matches:                   0 of 3
mean best |corr| across pairs:     0.8492
repeatability label: spacing_repeatable_radius_not_repeatable
```

## Interpretation

The short profiles contain a repeatable shallow reflector spacing pattern after
a small lateral alignment. That makes them useful for field QC and timing
calibration.

The result still blocks field geometry/radius claims. Radius choices do not
repeat across the two profiles, the accepted phase times differ by about
0.11-0.16 ns, and the survey-geometry audit already showed that these profiles
cannot be assembled into a reliable 3D grid.

Current field policy:

```text
Use short profiles 014/016 as repeatable shallow-reflector QC evidence.
Use top_envelope_35pct with +0.2 ns as the current timing anchor.
Do not report field radius, cover depth, geometry, FWI recovery, or 3D results
from this dataset without external survey and target metadata.
```

## Validation

The figure was validated as nonblank:

```text
short_profile_repeatability.png nonwhite=0.2677
```
