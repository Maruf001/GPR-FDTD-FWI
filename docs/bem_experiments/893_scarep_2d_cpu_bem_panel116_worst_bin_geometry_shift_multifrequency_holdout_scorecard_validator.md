# BEM Experiment 893: Panel-116 Worst-Bin Geometry-Shift Multi-Frequency Holdout Scorecard Validator

Date: 2026-07-01

## Purpose

Validate the saved run `892` multi-frequency holdout scorecard.

The validator checks source readiness, frequency-row stability, single-bin
repair without multi-frequency holdout pass, aggregate tradeoff preservation,
blocked downstream claim flags, figure output, and script snapshots.

## Output

```text
outputs/bem_experiments/893_scarep_2d_cpu_bem_panel116_worst_bin_geometry_shift_multifrequency_holdout_scorecard_validator
```

## Result

```text
validation checks:                    6
checks passed:                        6
checks failed:                        0
tested shift:                         common_z_plus_0p15mm
tested shift value:                   0.15 mm
frequency count:                      25
high-band frequency count:             9
baseline full-band relative L2:       0.0003383618947272846
shifted full-band relative L2:        0.0004561554424179171
baseline high-band relative L2:       0.0009518291083452528
shifted high-band relative L2:        0.0007586109080035837
baseline per-frequency pass count:    23
shifted per-frequency pass count:     19
baseline high-band pass count:         7
shifted high-band pass count:          5
baseline worst frequency:             2.3125 GHz
shifted worst frequency:              3.0 GHz
shifted worst relative L2:            0.0016529582704013506
original worst bin repaired:          true
high-band aggregate improves:         true
full-band aggregate improves:         false
per-frequency pass count improves:    false
multi-frequency holdout passes:       false
geometry-shift correction promoted:   false
project FDTD comparison ready:        false
field transfer ready:                 false
real 3D validation ready:             false
gpu priority:                         none
```

## Interpretation

The saved multi-frequency holdout validates as a no-promotion result. The
fixed `+0.15 mm` vertical proxy repairs the original worst bin and improves
the high-band aggregate metric, but it creates a worse upper-band failure and
reduces the number of passing frequencies.

## Decision

Use run `892` as a validated guardrail. Do not use a fixed vertical geometry
shift as a correction. The next useful branch is frequency-aware
source/receiver modeling or a boundary/source representation change.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_geometry_shift_multifrequency_holdout_scorecard_validator.py
3 passed
```

Figure check:

```text
2465x862, dynamic range=255
```

