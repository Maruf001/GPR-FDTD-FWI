# BEM Experiment 887: Panel-116 Worst-Bin Phase-Only Aperture Model Scorecard

Date: 2026-07-01

## Purpose

Check whether a unit-amplitude aperture phase model can repair the remaining
`2.3125 GHz` worst-bin mismatch.

This run reads the saved run `869` complex receiver responses and the validated
runs `884-886` diagnostic synthesis. It fits only phase corrections across the
receiver aperture, so the response amplitude is not rescaled. It does not rerun
BEM, project FDTD, field processing, 3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/887_scarep_2d_cpu_bem_panel116_worst_bin_phase_only_aperture_model_scorecard
```

## Result

```text
source spatial audit ready:                 true
source diagnostic synthesis ready:          true
source diagnostic validation ready:         true
source diagnostic sensitivity ready:        true
receiver rows:                              13
model rows:                                  6
frequency:                                  2.3125 GHz
target relative L2:                         0.001
uncorrected relative L2:                    0.002030466081391074
best in-sample model:                       constant_odd_even_phase
best in-sample relative L2:                 0.0018234403083841053
best in-sample reduction fraction:          0.10195972979028295
best leave-one-out model:                   constant_phase
best leave-one-out relative L2:             0.0019827840138898723
best leave-one-out reduction fraction:      0.023483311510692412
any in-sample model passes target:          false
any leave-one-out model passes target:      false
phase-only model repair ready:              false
source/receiver phase refinement required:  true
project FDTD comparison ready:              false
field transfer ready:                       false
real 3D validation ready:                   false
gpu priority:                               none
```

Model rows:

| Model | In-sample relative L2 | Leave-one-out relative L2 | In-sample reduction | Leave-one-out reduction |
| --- | ---: | ---: | ---: | ---: |
| constant phase | 0.001906219429484527 | 0.0019827840138898723 | 0.06119119794477209 | 0.023483311510692412 |
| odd linear centered phase | 0.0020296602251662194 | 0.0021373533375989616 | 0.00039688238687659796 | -0.05264173442122176 |
| even quadratic centered phase | 0.0020266990818076027 | 0.002137962247755276 | 0.001855238862641055 | -0.05294162131019522 |
| constant plus odd linear phase | 0.001905471442752991 | 0.0021028225941482374 | 0.061559579735727 | -0.03563542056688385 |
| constant plus even quadratic phase | 0.0018253245205861234 | 0.0020026289109027796 | 0.101031759498493 | 0.013709744153530977 |
| constant odd even phase | 0.0018234403083841053 | 0.002223830148891042 | 0.10195972979028295 | -0.09523137040905116 |

## Interpretation

A phase-only aperture correction is not enough. The best in-sample model
reduces the worst-bin relative L2 by about ten percent, but it remains above
target. The best leave-one-out model is only a constant phase shift, reduces
the error by about two percent, and also remains above target.

The richer phase models fit the saved receiver row better in sample, but they
do not hold out. This points away from a simple unit-amplitude aperture phase
repair and toward a richer source/receiver representation or boundary/source
model change.

## Decision

Do not promote a phase-only aperture correction, hard per-frequency acceptance,
project-FDTD comparison, field transfer, or 3D/HPC claim from this run.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_phase_only_aperture_model_scorecard.py
3 passed
```

Figure check:

```text
2716x862, dynamic range=255
```

