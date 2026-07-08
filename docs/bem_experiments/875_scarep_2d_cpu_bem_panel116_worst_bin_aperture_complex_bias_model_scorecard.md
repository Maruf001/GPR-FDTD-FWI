# BEM Experiment 875: Panel-116 Worst-Bin Aperture Complex-Bias Model Scorecard

Date: 2026-07-01

## Purpose

Check whether a smooth aperture-dependent complex bias explains and repairs the
worst remaining 116-panel high-band frequency bin.

This run reads saved receiver residual rows from run `869` and the guarded
aperture-trim block from runs `872-874`. It does not rerun BEM, FDTD, field
processing, 3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/875_scarep_2d_cpu_bem_panel116_worst_bin_aperture_complex_bias_model_scorecard
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_worst_bin_aperture_complex_bias_model_scorecard_model_rows.csv
data/scarep_2d_cpu_bem_panel116_worst_bin_aperture_complex_bias_model_scorecard_summary.json
figures/scarep_2d_cpu_bem_panel116_worst_bin_aperture_complex_bias_model_scorecard.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source trim scorecard ready:            true
source trim validation ready:           true
source trim sensitivity ready:          true
source spatial audit ready:             true
model rows:                             3
receiver rows:                          13
frequency:                              2.3125 GHz
target relative L2:                     0.001
uncorrected relative L2:                0.002030466081391074
best in-sample model:                   quadratic_aperture_complex_bias
best in-sample relative L2:             0.0018381250513289863
best in-sample reduction:               0.0947275267609073
best in-sample ratio R2:                0.10664060177057122
best leave-one-out model:               constant_complex_bias
best leave-one-out relative L2:         0.0020966945192620154
best leave-one-out reduction:           -0.032617357402773446
any in-sample model passes target:      false
any leave-one-out model passes target:  false
all leave-one-out models worse:         true
smooth complex-bias repair ready:       false
project FDTD comparison ready:          false
field transfer ready:                   false
3D validation ready:                    false
```

## Interpretation

The quadratic model gives the best in-sample reduction, but the corrected
relative L2 remains about `0.00184`, still above the `0.001` target. The
leave-one-out check is more important: every smooth complex-bias model is
worse than the uncorrected response when each receiver is predicted from the
other receivers.

This means a smooth aperture-dependent complex-bias correction is not supported
as a reliable fix for the remaining worst-bin mismatch.

## Decision

Keep this as no-repair diagnostic evidence. Do not promote smooth
aperture-bias correction, hard per-frequency acceptance, project-FDTD
comparison, field transfer, or 3D/HPC claims from this result.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_aperture_complex_bias_model_scorecard.py
3 passed
```

Figure check:

```text
2644x851, dynamic range=255
```
