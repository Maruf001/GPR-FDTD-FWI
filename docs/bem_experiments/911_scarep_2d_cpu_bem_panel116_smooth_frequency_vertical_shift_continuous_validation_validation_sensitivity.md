# BEM Experiment 911: Panel-116 Smooth Frequency-Aware Vertical-Shift Continuous Validation Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `910` continuous-validation validator by damaging the saved
run `909` state in controlled ways.

The sensitivity set checks readiness damage, frequency-row removal,
above-target continuous rows, pass-count damage, high-band pass-count damage,
worst-frequency damage, off-grid demotion, excessive snapped/continuous
difference, project-FDTD candidate demotion, false project-FDTD completion,
correction promotion, downstream promotion, figure damage, and script-snapshot
damage.

## Output

```text
outputs/bem_experiments/911_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_continuous_validation_validation_sensitivity
```

## Result

```text
source validator ready:              true
scenarios:                           17
expected passes:                      1
expected failures:                   16
observed passes:                      1
observed failures:                   16
unexpected outcomes:                  0
damaged scenarios:                   16
project FDTD comparison candidate:   true
project FDTD comparison completed:  false
smooth correction promoted:         false
field transfer ready:               false
real 3D validation ready:           false
gpu priority:                       none
```

Scenario results:

| Scenario | Expected pass | Observed pass | Unexpected |
| --- | --- | --- | --- |
| exact_continuous_validation | true | true | false |
| continuous_not_ready | false | false | false |
| frequency_row_removed | false | false | false |
| continuous_fail | false | false | false |
| pass_count_changed | false | false | false |
| high_pass_count_changed | false | false | false |
| worst_frequency_changed | false | false | false |
| off_grid_demoted | false | false | false |
| snapped_delta_too_large | false | false | false |
| project_candidate_demoted | false | false | false |
| project_fdtd_completed | false | false | false |
| correction_promoted | false | false | false |
| field_promoted | false | false | false |
| three_d_promoted | false | false | false |
| gpu_promoted | false | false | false |
| figure_damage | false | false | false |
| snapshot_damage | false | false | false |

## Interpretation

The run `910` validator accepts only the exact saved continuous-validation
state. It rejects damaged continuous rows, false project-FDTD completion,
false correction promotion, downstream promotion, damaged figures, and damaged
script snapshots.

## Decision

Use runs `909-911` as the guarded BEM-side candidate packet for a
project-FDTD comparison design. This packet does not complete project-FDTD
comparison, field transfer, or real 3D validation.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_continuous_validation_validation_sensitivity.py
3 passed
```

Figure check:

```text
2861x890, dynamic range=255
```
