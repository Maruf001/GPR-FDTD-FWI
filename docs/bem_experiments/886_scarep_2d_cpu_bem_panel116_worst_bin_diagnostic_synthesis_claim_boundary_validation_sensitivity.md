# BEM Experiment 886: Panel-116 Worst-Bin Diagnostic Synthesis Claim Boundary Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `885` validator by damaging the saved run `884` state in
controlled ways.

The sensitivity set checks synthesis-readiness damage, row removal, false
physical target repair, false best-candidate demotion, lower-bound failure,
source/receiver model demotion, correction promotion, hard per-frequency
promotion, project-FDTD promotion, field promotion, real-3D promotion,
GPU-priority promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/886_scarep_2d_cpu_bem_panel116_worst_bin_diagnostic_synthesis_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                         15
expected passes:                    1
expected failures:                 14
observed passes:                    1
observed failures:                 14
unexpected outcomes:                0
damaged scenarios:                 14
correction promoted:            false
hard per-frequency ready:       false
project FDTD comparison ready:  false
real 3D validation ready:       false
field transfer ready:           false
gpu priority:                   none
```

## Interpretation

The validator accepts only the exact saved diagnostic synthesis. All damaged
states and all premature downstream promotions are rejected.

## Decision

Use runs `884-886` as the guarded diagnostic synthesis claim boundary for the
remaining 116-panel worst high-band frequency bin.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_diagnostic_synthesis_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
2645x875, dynamic range=255
```

