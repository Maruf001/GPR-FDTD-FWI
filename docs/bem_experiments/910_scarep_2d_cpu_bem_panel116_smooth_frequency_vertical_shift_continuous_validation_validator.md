# BEM Experiment 910: Panel-116 Smooth Frequency-Aware Vertical-Shift Continuous Validation Validator

Date: 2026-07-01

## Purpose

Validate the saved run `909` continuous off-grid vertical-shift validation.

The validator checks source readiness, frequency-row shape, off-grid
continuous model closure, consistency between snapped and continuous results,
blocked downstream claim flags, figure output, and script snapshots.

## Output

```text
outputs/bem_experiments/910_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_continuous_validation_validator
```

## Result

```text
validation checks:                       6
checks passed:                           6
checks failed:                           0
model:                                   best_gaussian_bump
model family:                            gaussian_bump
frequency count:                         25
high-band frequency count:                9
continuous pass count:                   25
snapped pass count:                      25
high-band continuous pass count:          9
continuous worst frequency:              2.65625 GHz
continuous worst relative L2:            0.0008519458802336965
continuous shift min:                    0.05000000000000001 mm
continuous shift max:                    0.09970745639274738 mm
max absolute continuous/snapped delta:   0.00008112758940537559
BEM continuous shift validation passes:  true
project FDTD comparison candidate:       true
project FDTD comparison completed:       false
smooth correction promoted:              false
field transfer ready:                    false
real 3D validation ready:                false
gpu priority:                            none
```

Validation checks:

| Check | Passed |
| --- | --- |
| continuous_validation_ready | true |
| frequency_rows_stable | true |
| continuous_off_grid_model_passes | true |
| snapped_continuous_consistency | true |
| blocked_claims_preserved | true |
| figure_and_scripts_valid | true |

## Interpretation

The run `909` continuous-shift validation is internally consistent. The
off-grid smooth source/receiver shift model passes all tested frequencies and
keeps the downstream claim boundary blocked.

## Decision

Use runs `909-910` as the guarded BEM-side candidate for a project-FDTD
comparison design. Do not treat this as a completed project-FDTD comparison,
field transfer, or 3D validation.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_continuous_validation_validator.py
4 passed
```

Figure check:

```text
2465x860, dynamic range=255
```
