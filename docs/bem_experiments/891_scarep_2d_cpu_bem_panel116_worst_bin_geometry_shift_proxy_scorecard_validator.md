# BEM Experiment 891: Panel-116 Worst-Bin Geometry-Shift Proxy Scorecard Validator

Date: 2026-07-01

## Purpose

Validate the saved run `890` geometry-shift proxy scorecard.

The validator checks source readiness, candidate-grid stability, vertical
single-bin closure, the no-correction claim boundary, blocked downstream claim
flags, figure output, and script snapshots.

## Output

```text
outputs/bem_experiments/891_scarep_2d_cpu_bem_panel116_worst_bin_geometry_shift_proxy_scorecard_validator
```

## Result

```text
validation checks:                    6
checks passed:                        6
checks failed:                        0
receiver rows:                        13
candidate shifts:                     36
frequency:                            2.3125 GHz
target relative L2:                   0.001
baseline relative L2:                 0.0020304660813910734
best candidate:                       common_z_plus_0p15mm
best shift mode:                      common_z
best shift:                           0.15 mm
best candidate relative L2:           0.0002966325470015585
best reduction fraction:              0.8539091345971486
target-passing candidates:            13
vertical-shift passing candidates:    13
horizontal-shift passing candidates:   0
single-frequency geometry proxy pass: true
multi-frequency holdout required:     true
geometry-shift correction promoted:   false
project FDTD comparison ready:        false
field transfer ready:                 false
real 3D validation ready:             false
gpu priority:                         none
```

## Interpretation

The saved geometry-shift scorecard validates as a single-bin vertical proxy.
It is the current best lead for explaining the remaining worst-bin mismatch,
but it is not a promoted correction because it has not yet been tested across
multiple frequencies or holdout conditions.

## Decision

Use run `890` as a validated single-bin vertical-geometry proxy and move next
to multi-frequency holdout testing.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_geometry_shift_proxy_scorecard_validator.py
3 passed
```

Figure check:

```text
2465x860, dynamic range=255
```

