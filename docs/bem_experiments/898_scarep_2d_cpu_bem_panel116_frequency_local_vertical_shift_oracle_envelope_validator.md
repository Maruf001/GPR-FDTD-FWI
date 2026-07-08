# BEM Experiment 898: Panel-116 Frequency-Local Vertical-Shift Oracle Envelope Validator

Date: 2026-07-01

## Purpose

Validate the saved run `897` frequency-local vertical-shift oracle envelope.

The validator checks source readiness, frequency-row and candidate-row shapes,
all-frequency oracle closure, nonconstant selected shifts, blocked downstream
claim flags, figure output, and script snapshots.

## Output

```text
outputs/bem_experiments/898_scarep_2d_cpu_bem_panel116_frequency_local_vertical_shift_oracle_envelope_validator
```

## Result

```text
validation checks:                    6
checks passed:                        6
checks failed:                        0
frequency count:                      25
high-band frequency count:             9
shift candidates:                      9
candidate rows:                      225
baseline per-frequency pass count:    23
oracle per-frequency pass count:      25
baseline high-band pass count:         7
oracle high-band pass count:           9
baseline worst frequency:             2.3125 GHz
baseline worst relative L2:           0.0020304660813911003
oracle worst frequency:               2.65625 GHz
oracle worst relative L2:             0.0008518855375610986
unique selected shifts:                4
minimum selected shift:                0.0 mm
maximum selected shift:                0.15 mm
selected shift counts:                 {"0.00": 1, "0.05": 16, "0.10": 7, "0.15": 1}
frequency-local oracle passes:         true
oracle correction promoted:            false
smooth frequency model required:       true
project FDTD comparison ready:         false
field transfer ready:                  false
real 3D validation ready:              false
gpu priority:                          none
```

## Interpretation

The oracle envelope is internally consistent and validates as a nonconstant
oracle target. It shows that the remaining 116-panel mismatch can be reduced
below target at every frequency if the vertical source/receiver shift is
allowed to vary by frequency.

This is not a correction. The selected shift changes across the band, so the
next step must be a constrained smooth model rather than free per-frequency
choice.

## Decision

Use runs `897-898` as the guarded target for a smooth frequency-aware
source/receiver model. Keep project-FDTD, field-transfer, and 3D claims
blocked.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_frequency_local_vertical_shift_oracle_envelope_validator.py
3 passed
```

Figure check:

```text
2465x865, dynamic range=255
```

