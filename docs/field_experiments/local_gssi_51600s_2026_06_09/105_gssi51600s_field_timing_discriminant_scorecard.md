# Field Experiment 105: Timing Discriminant Scorecard

Date: 2026-06-18

## Purpose

Build a row-level scorecard from existing measured-field timing evidence:

- early/common-mode lag rows
- short-pair time-zero perturbation windows
- long-profile shift-sensitivity windows
- timing-window family classification

This is CPU-only analysis over existing outputs. It does not run FDTD, FWI, 3D,
or GPU kernels.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/105_gssi51600s_field_timing_discriminant_scorecard
```

Key artifacts:

```text
data/field_timing_discriminant_scorecard_rows.csv
data/field_timing_discriminant_scorecard_summary.json
figures/field_timing_discriminant_scorecard.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         field_timing_discriminant_scorecard_ready_not_absolute
score rows:                           4
strict early near-zero windows:       6/6
early minimum uniqueness margin:      3.017058e-05
short non-raw supported windows:      18/18
raw/no-correction supported windows:  0/3
short nominal relative offset:        0.127701 ns
short minimum matrix improvement:     0.125152
long windows rejecting short transfer: 3/3
long best offset median:              0.060000 ns
long/short offset separation:         0.067701 ns
field FWI ready:                      false
gpu priority:                         none
```

## Interpretation

This scorecard strengthens the timing-claim boundary. Early windows behave as a
common-mode timing control, but one early row has a low best-vs-second
correlation margin, so it should not be upgraded to absolute time-zero. Short
non-raw timing windows robustly support the relative correction. Raw/no
correction is rejected. Long windows keep a stable pattern-only offset and
reject transferring the short-pair correction.

The result is useful timing discipline for manuscript wording. It does not
create absolute time-zero, field FWI, 3D, radius, or cover-depth claims.
