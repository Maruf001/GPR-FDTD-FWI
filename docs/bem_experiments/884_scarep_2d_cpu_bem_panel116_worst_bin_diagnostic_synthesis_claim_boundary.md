# BEM Experiment 884: Panel-116 Worst-Bin Diagnostic Synthesis Claim Boundary

Date: 2026-07-01

## Purpose

Synthesize the saved worst-bin diagnostic results into one claim-boundary table.

The run reads the scalar-gain decomposition, spatial residual anatomy,
aperture-trim scorecard, smooth complex-bias scorecard, receiver-pair symmetry
audit, and pair-component oracle scorecard. It does not rerun BEM, project
FDTD, field processing, 3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/884_scarep_2d_cpu_bem_panel116_worst_bin_diagnostic_synthesis_claim_boundary
```

## Result

```text
diagnostic rows:                         7
target relative L2:                      0.001
worst frequency:                         2.3125 GHz
full relative L2:                        0.0020304660813910734
best physical candidate relative L2:     0.001195683569955468
nonphysical lower-bound relative L2:     0.0005793593752068725
physical candidate pass count:           0
nonphysical lower bound passes target:   true
source/receiver spatial phase required:  true
hard per-frequency endpoint ready:       false
correction promoted:                     false
project FDTD comparison ready:           false
field transfer ready:                    false
real 3D validation ready:                false
gpu priority:                            none
```

The diagnostic rows are:

| Diagnostic | Source run | Value | Passes target | Physical repair candidate |
| --- | ---: | ---: | --- | --- |
| scalar gain amplitude phase | 866 | 0.0019054837810734088 | false | true |
| spatial anatomy | 869 | 0.5923362105102755 | false | false |
| strict center aperture trim | 872 | 0.001938978012629881 | false | true |
| smooth complex bias holdout | 875 | 0.0020966945192620154 | false | true |
| receiver pair symmetry | 878 | 0.7111267885406554 | false | false |
| antisymmetric pair oracle | 881 | 0.001195683569955468 | false | true |
| all-pair oracle lower bound | 881 | 0.0005793593752068725 | true | false |

## Interpretation

The remaining `2.3125 GHz` mismatch is not repaired by scalar gain, aperture
trimming, smooth aperture bias, or antisymmetric pair-component removal. The
only target-passing row is the nonphysical lower bound that removes all paired
receiver residuals and keeps only the center receiver residual.

This makes the next useful BEM physics question narrower: the unresolved
difference needs a source/receiver spatial phase model or boundary/source
representation change, not another scalar correction.

## Decision

Use run `884` as the current worst-bin diagnostic synthesis. Keep correction,
hard per-frequency acceptance, project-FDTD comparison, field transfer, and
3D/HPC claims blocked from this evidence.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_diagnostic_synthesis_claim_boundary.py
3 passed
```

Figure check:

```text
2825x872, dynamic range=255
```

