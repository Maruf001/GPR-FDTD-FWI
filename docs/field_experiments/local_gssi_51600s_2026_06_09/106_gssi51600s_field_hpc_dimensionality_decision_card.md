# Field Experiment 106: HPC Dimensionality Decision Card

Date: 2026-06-18

## Purpose

Consolidate the current local GSSI field-data decision boundary into one
CPU-only card:

- whether the dataset is a 2D or 3D survey
- whether it should be submitted as an HPC/field-FWI workload
- which field claims remain allowed after the timing-discriminant scorecard

This run reads existing summaries. It does not run FDTD, FWI, 3D inversion,
GPU kernels, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/106_gssi51600s_field_hpc_dimensionality_decision_card
```

Key artifacts:

```text
data/field_hpc_dimensionality_decision_rows.csv
data/field_hpc_dimensionality_decision_summary.json
figures/field_hpc_dimensionality_decision_card.png
figures/FIGURE_NOTES.md
```

## Result

Policy label:

```text
gssi51600s_field_hpc_dimensionality_decision_2d_only_no_hpc
```

Summary:

```text
field geometry type:              independent_2d_line_profiles
is 3D survey:                     false
ready for 2D QC:                  true
ready for 3D HPC:                 false
ready for field FWI:              false
ready for absolute time-zero:     false
ready for cover-depth recovery:   false
ready for radius recovery:        false
profile count:                    4
total trace-derived length:       7.215945 m
scan spacing:                     3.333 mm
samples per wavelength:           37.478
relative time-zero depth equiv.:  5.890 mm
short nominal offset:             0.127701 ns
long/short offset separation:     0.067701 ns
all-window support fraction:      0.281124
field HPC priority:               none
```

Decision rows:

| Gate | Decision | Status |
| --- | --- | --- |
| survey dimensionality | `2d_line_profiles_only` | `blocks_3d_hpc` |
| alongline sampling | `supports_2d_qc` | `ready_for_2d_qc` |
| timing anchor scope | `relative_not_absolute` | `blocks_absolute_time_zero` |
| spatial support scope | `supported_intervals_only` | `scope_limited` |
| claim viability | `2d_field_qc_only` | `ready_scoped_not_inversion` |
| field HPC/FWI gate | `do_not_submit_field_hpc_job` | `blocked` |

## Interpretation

The local GSSI 51600S dataset should be treated as four independent 2D line
profiles. It is useful for dense along-line timing, repeatability, and
supported-interval visual QC. It is not a 3D survey, field-FWI benchmark,
radius-recovery dataset, or cover-depth-recovery dataset in the current archive
state.

Field-side HPC should wait for external survey-layout metadata, calibrated
target geometry, and absolute timing/depth controls, or for a new controlled
field acquisition. The current field work should remain local CPU-side 2D QC
and manuscript boundary evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_hpc_dimensionality_decision_card.py
2 passed
```

Figure validation:

```text
field_hpc_dimensionality_decision_card.png: 2484x869,
nonwhite=0.1867, dynamic range=255
```
