# BEM Experiment 899: Panel-116 Frequency-Local Vertical-Shift Oracle Envelope Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `898` oracle-envelope validator by damaging the saved run
`897` state in controlled ways.

The sensitivity set checks envelope-readiness damage, frequency-row removal,
candidate-row removal, false oracle failure, baseline and high-band pass-count
damage, constant-shift damage, oracle-correction promotion, smooth-model
demotion, project-FDTD promotion, field promotion, real-3D promotion,
GPU-priority promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/899_scarep_2d_cpu_bem_panel116_frequency_local_vertical_shift_oracle_envelope_validation_sensitivity
```

## Result

```text
scenarios:                         16
expected passes:                    1
expected failures:                 15
observed passes:                    1
observed failures:                 15
unexpected outcomes:                0
damaged scenarios:                 15
oracle correction promoted:     false
smooth frequency model required: true
project FDTD comparison ready:  false
real 3D validation ready:       false
field transfer ready:           false
gpu priority:                   none
```

## Interpretation

The validator accepts only the exact saved oracle envelope. It rejects damaged
row counts, false correction promotion, false downstream promotion, and a
damaged constant-shift interpretation.

## Decision

Use runs `897-899` as the guarded frequency-local vertical-shift oracle target
for the next smooth frequency-aware source/receiver model.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_frequency_local_vertical_shift_oracle_envelope_validation_sensitivity.py
3 passed
```

Figure check:

```text
2789x889, dynamic range=255
```

