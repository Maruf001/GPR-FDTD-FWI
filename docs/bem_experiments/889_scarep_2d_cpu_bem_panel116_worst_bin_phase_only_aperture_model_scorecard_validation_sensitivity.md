# BEM Experiment 889: Panel-116 Worst-Bin Phase-Only Aperture Model Scorecard Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `888` validator by damaging the saved run `887`
phase-only scorecard in controlled ways.

The sensitivity set checks scorecard-readiness damage, row removal, false
in-sample pass rows, false leave-one-out pass rows, false target demotion,
phase-repair promotion, holdout-split damage, unit-amplitude damage,
source/receiver refinement demotion, correction promotion, hard per-frequency
promotion, project-FDTD promotion, field promotion, real-3D promotion,
GPU-priority promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/889_scarep_2d_cpu_bem_panel116_worst_bin_phase_only_aperture_model_scorecard_validation_sensitivity
```

## Result

```text
scenarios:                         19
expected passes:                    1
expected failures:                 18
observed passes:                    1
observed failures:                 18
unexpected outcomes:                0
damaged scenarios:                 18
phase-only repair ready:        false
hard per-frequency ready:       false
correction promoted:            false
project FDTD comparison ready:  false
real 3D validation ready:       false
field transfer ready:           false
gpu priority:                   none
```

## Interpretation

The validator accepts only the exact saved phase-only scorecard. False repair
claims, row damage, holdout-split damage, and downstream promotion states are
rejected.

## Decision

Use runs `887-889` as the guarded phase-only no-repair block for the remaining
116-panel worst high-band frequency bin.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_phase_only_aperture_model_scorecard_validation_sensitivity.py
3 passed
```

Figure check:

```text
2861x893, dynamic range=255
```

