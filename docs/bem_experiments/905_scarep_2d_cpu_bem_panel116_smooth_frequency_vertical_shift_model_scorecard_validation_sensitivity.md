# BEM Experiment 905: Panel-116 Smooth Frequency-Aware Vertical-Shift Model Scorecard Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `901` smooth-model validator by damaging the saved run
`900` scorecard in controlled ways.

The sensitivity set checks scorecard-readiness damage, model-row removal,
applied-row removal, false all-model pass claims, best-model swaps,
above-target best-model errors, selected-shift damage, missing
continuous-shift validation requirements, correction promotion, downstream
promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/905_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_model_scorecard_validation_sensitivity
```

## Result

```text
source validator ready:                 true
scenarios:                              17
expected passes:                         1
expected failures:                      16
observed passes:                         1
observed failures:                      16
unexpected outcomes:                     0
damaged scenarios:                      16
smooth model correction promoted:     false
continuous-shift validation required: true
project FDTD comparison ready:        false
real 3D validation ready:             false
field transfer ready:                 false
gpu priority:                         none
```

Scenario results:

| Scenario | Expected pass | Observed pass | Unexpected |
| --- | --- | --- | --- |
| exact_scorecard | true | true | false |
| scorecard_not_ready | false | false | false |
| model_row_removed | false | false | false |
| applied_row_removed | false | false | false |
| false_all_models_pass | false | false | false |
| best_model_swapped | false | false | false |
| best_relative_l2_above_target | false | false | false |
| best_shift_counts_changed | false | false | false |
| best_unique_shift_damaged | false | false | false |
| continuous_validation_not_required | false | false | false |
| correction_promoted | false | false | false |
| project_fdtd_promoted | false | false | false |
| field_promoted | false | false | false |
| three_d_promoted | false | false | false |
| gpu_promoted | false | false | false |
| figure_damage | false | false | false |
| snapshot_damage | false | false | false |

## Interpretation

The run `901` validator accepts only the exact saved smooth-model scorecard. It
rejects damaged rows, false model-pattern changes, false correction promotion,
downstream promotion, damaged figures, and damaged script snapshots.

## Decision

Use runs `900-901` and `905` as the guarded smooth-model setup for
continuous-shift validation. The current scorecard passes on the sampled
shifted grid, but it still cannot be promoted as a correction until
interpolation between the saved grid values is checked.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_model_scorecard_validation_sensitivity.py
3 passed
```

Figure check:

```text
2861x889, dynamic range=255
```
