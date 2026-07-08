# BEM Experiment 901: Panel-116 Smooth Frequency-Aware Vertical-Shift Model Scorecard Validator

Date: 2026-07-01

## Purpose

Validate the saved run `900` smooth frequency-aware vertical-shift model
scorecard.

The validator checks source readiness, model-row shape, applied frequency-row
shape, all-frequency smooth-grid closure, the exact constrained smooth model
pattern, blocked downstream claim flags, figure output, and script snapshots.

## Output

```text
outputs/bem_experiments/901_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_model_scorecard_validator
```

## Result

```text
validation checks:                      6
checks passed:                          6
checks failed:                          0
model count:                            5
all-frequency pass model count:         3
best model:                             best_gaussian_bump
best model family:                      gaussian_bump
best model max relative L2:             0.0008518855375610986
best model worst frequency:             2.65625 GHz
best model shift MSE vs oracle:         0.0009000000000000001
best model selected shift counts:       {"0.05": 20, "0.10": 5}
smooth frequency grid model passes:     true
continuous-shift validation required:   true
smooth model correction promoted:       false
project FDTD comparison ready:          false
real 3D validation ready:               false
field transfer ready:                   false
field FWI ready:                        false
gpu priority:                           none
```

Validation checks:

| Check | Passed |
| --- | --- |
| scorecard_ready | true |
| row_shapes_stable | true |
| smooth_grid_closes_all_frequencies | true |
| constrained_smooth_model_pattern_preserved | true |
| blocked_claims_preserved | true |
| figure_and_scripts_valid | true |

## Interpretation

The run `900` smooth snapped-grid model scorecard is internally consistent.
The best model closes all saved sampled frequencies without free
per-frequency choice and keeps the downstream claim boundary blocked.

This validates the saved scorecard as a candidate source/receiver model target.
It does not validate interpolation between the saved shift values or between
sampled frequencies.

## Decision

Use runs `900-901` as the guarded input for continuous-shift validation. Do
not promote the smooth model to project-FDTD comparison, field transfer, or
3D validation until that check passes.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_model_scorecard_validator.py
4 passed
```

Figure check:

```text
2465x859, dynamic range=255
```
