# BEM Experiment 900: Panel-116 Smooth Frequency-Aware Vertical-Shift Model Scorecard

Date: 2026-07-01

## Purpose

Test whether the run `897` frequency-local vertical-shift oracle can be
approximated by constrained smooth source/receiver models instead of free
per-frequency choices.

This run does not rerun the BEM solver. It scores smooth snapped-grid models
against the saved run `897` candidate table, after run `898` validated that
oracle table and run `899` sensitivity-hardened the validator. It does not
run project FDTD, field processing, 3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/900_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_model_scorecard
```

## Result

```text
source oracle ready:                    true
source oracle validation ready:         true
source oracle sensitivity ready:        true
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

Model scorecard:

| Model | Pass count | Max relative L2 | Selected shifts |
| --- | ---: | ---: | --- |
| polynomial_degree_0 | 24 | 0.001367588871846657 | {"0.05": 25} |
| polynomial_degree_1 | 24 | 0.001367588871846657 | {"0.05": 21, "0.10": 4} |
| polynomial_degree_2 | 25 | 0.0009089020571223779 | {"0.05": 16, "0.10": 9} |
| polynomial_degree_3 | 25 | 0.0009089020571223779 | {"0.05": 15, "0.10": 10} |
| best_gaussian_bump | 25 | 0.0008518855375610986 | {"0.05": 20, "0.10": 5} |

## Interpretation

A constrained smooth frequency-aware source/receiver model can pass every
sampled frequency on the saved shifted grid. The best model uses only two
vertical shifts, `0.05 mm` and `0.10 mm`, and reaches the same worst-frequency
relative L2 as the run `897` oracle envelope.

This is a stronger result than the free oracle because it removes most of the
per-frequency freedom, but it is still a snapped-grid scorecard. It does not
prove that the correction works between sampled shifts or between sampled
frequencies.

## Decision

Use this as the current candidate source/receiver model. Do not promote it to
project-FDTD comparison, field transfer, or 3D validation until a continuous
shift validation checks interpolation between the saved grid values.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_model_scorecard.py
3 passed
```

Figure check:

```text
2716x870, dynamic range=255
```
