# BEM Experiment 883: Panel-116 Worst-Bin Pair-Component Oracle Scorecard Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `882` pair-component oracle validator by damaging the saved
run `881` state in controlled ways.

The sensitivity set checks source readiness damage, row removal, false
antisymmetric pass rows, antisymmetric demotion below target, false energy
budget claims, all-pair lower-bound failure, correction promotion, hard
per-frequency promotion, project-FDTD promotion, field/3D promotion,
GPU-priority promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/883_scarep_2d_cpu_bem_panel116_worst_bin_pair_component_oracle_scorecard_validation_sensitivity
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

## Decision

Use runs `881-883` as the guarded pair-component oracle no-repair block for
the remaining 116-panel worst high-band frequency bin.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_pair_component_oracle_scorecard_validation_sensitivity.py
3 passed
```

Figure check:

```text
2645x873, dynamic range=255
```
