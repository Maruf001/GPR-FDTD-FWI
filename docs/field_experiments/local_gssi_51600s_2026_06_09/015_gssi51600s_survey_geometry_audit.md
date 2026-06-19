# Field Experiment 015: GSSI 51600S Survey-Geometry Audit

Date: 2026-06-17

## Purpose

CPU-only audit of whether the local GSSI 51600S field dataset can be treated as
a 3D survey/grid, or only as separate 2D line-profile evidence. This run reads
the experiment 001 DZT inventory and the raw `.DZX` sidecars.

No FDTD, FWI, or GPU command was run for this experiment.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/015_gssi51600s_survey_geometry_audit
```

Artifacts:

```text
data/survey_geometry_audit.csv
data/survey_geometry_audit_summary.json
data/figure_validation.csv
figures/survey_geometry_audit.png
run_manifest.json
```

## Result

Classification:

```text
independent_2d_line_profiles
```

The dataset has four imported DZT channel records:

| File | Traces | Trace-derived length | DZX waypoint endpoint distance | Waypoint/trace length ratio |
| --- | ---: | ---: | ---: | ---: |
| `PROJECT001C__013.DZT` | 807 | 2.686398 m | 0.003332 m | 0.00124 |
| `PROJECT001C__014.DZT` | 274 | 0.909909 m | 0.003332 m | 0.00366 |
| `PROJECT001C__015.DZT` | 814 | 2.709729 m | 0.003332 m | 0.00123 |
| `PROJECT001C__016.DZT` | 274 | 0.909909 m | 0.003332 m | 0.00366 |

Audit flags:

```text
profile count:                    4
trace-derived total length:        7.215945 m
DZG/GPS/grid position file:        absent
reliable DZX waypoint lengths:     no
recoverable crossline spacing:     no
```

## Interpretation

The local GSSI dataset is useful for profile-level QC, timing calibration, and
2D field-to-synthetic waveform checks. It is not currently a usable 3D survey
geometry. The `.DZX` files contain a `gridId`, but the waypoint endpoint
distances do not encode the trace-derived profile lengths, and there is no
`.DZG`/GPS/grid-position file to recover profile spacing, orientation, or
crossline order.

Current field policy:

```text
Treat this dataset as separate 2D line-profile calibration/QC evidence.
Do not use it as a 3D survey or measured-data FWI benchmark without external
survey-layout metadata.
```

## Validation

The survey-geometry audit figure was validated as nonblank:

```text
survey_geometry_audit.png nonwhite=0.1691
```
