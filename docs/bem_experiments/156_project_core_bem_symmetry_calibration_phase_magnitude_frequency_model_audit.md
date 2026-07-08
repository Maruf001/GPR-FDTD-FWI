# BEM Experiment 156: Symmetry Calibration Phase/Magnitude Frequency Model Audit

Date: 2026-06-27

## Purpose

Test whether the run `150`/`151` BEM symmetry calibration candidate fails
frequency holdout because the previous models interpolated complex coefficients
directly.

Runs `152` through `155` showed that polynomial, nearest-neighbor, linear,
cubic, PCHIP, and Akima interpolation of real/imaginary coefficients do not
make the candidate frequency-generalized. This run tests a different
parameterization: coefficient log-magnitude plus unwrapped phase, with and
without linear phase detrending.

This is a CPU-only audit from saved bridge arrays. It does not rerun FDTD,
rerun BEM solvers, compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/156_project_core_bem_symmetry_calibration_phase_magnitude_frequency_model_audit
```

Key artifacts:

```text
data/project_core_bem_symmetry_calibration_phase_magnitude_frequency_model_rows.csv
data/project_core_bem_symmetry_calibration_phase_magnitude_frequency_model_audit_summary.json
figures/project_core_bem_symmetry_calibration_phase_magnitude_frequency_model_audit.png
docs/PROJECT_CORE_BEM_SYMMETRY_CALIBRATION_PHASE_MAGNITUDE_FREQUENCY_MODEL_AUDIT.md
scripts/run_project_core_bem_symmetry_calibration_phase_magnitude_frequency_model_audit.py
scripts/test_project_core_bem_symmetry_calibration_phase_magnitude_frequency_model_audit.py
```

## Result

```text
candidate train receivers:                         0;2;4;6
candidate holdout receivers:                       1;3;5
candidate spatial degree:                          1
phase/magnitude methods:                           4
phase/magnitude modes:                             2
phase/magnitude model rows:                        44
passing phase/magnitude rows:                      0
alternating passing phase/magnitude rows:          0
best held-frequency scheme:                        drop_low_edge
best held-frequency mode:                          magnitude_phase
best held-frequency method:                        linear
best held-frequency relative L2:                   0.11704123813863182
best alternating scheme:                           even_train_odd_hold
best alternating mode:                             magnitude_phase
best alternating method:                           linear
best alternating held-frequency relative L2:       0.1225366210060622
best holdout receiver held-frequency L2:           0.08774003872787993
phase/magnitude frequency model ready:             false
project-core bridge ready:                         false
3D validation ready:                               false
field FWI ready:                                   false
GPU/HPC ready:                                     false
```

Best phase/magnitude outcomes by frequency split:

| Scheme | Mode | Method | Held-frequency L2 | Holdout receiver held-frequency L2 | Passes |
| --- | --- | --- | ---: | ---: | --- |
| drop_both_edges | phase_detrended_magnitude_phase | linear | 0.14177652791301407 | 0.13366027387227855 | false |
| drop_high_edge | phase_detrended_magnitude_phase | linear | 0.15849793260528372 | 0.1808008100416571 | false |
| drop_low_edge | magnitude_phase | linear | 0.11704123813863182 | 0.09549811429170899 | false |
| even_train_odd_hold | magnitude_phase | linear | 0.1225366210060622 | 0.08774003872787993 | false |
| low_mid_high_sparse | magnitude_phase | pchip | 0.14285351779702277 | 0.12926718427943426 | false |
| odd_train_even_hold | phase_detrended_magnitude_phase | akima | 0.12707467307672088 | 0.1259727548472636 | false |

## Interpretation

Log-magnitude and unwrapped-phase coefficient models do not close the frequency
holdout gap. The best held-frequency result remains above the `0.1` gate, and
no alternating frequency split passes.

This rules out a simple explanation that the prior no-go came only from
interpolating real and imaginary coefficient parts or from phase wrapping.

## Decision

Treat the BEM symmetry calibration as a per-frequency candidate only. Do not
promote project-core comparison, 3D validation, GPU/HPC, or field FWI from this
branch.

The next defensible BEM branches are either a fresh matched-case validation or a
more structural frequency model, not another simple coefficient interpolation
variant.

## Validation

Focused tests:

```text
tests/test_project_core_bem_symmetry_calibration_phase_magnitude_frequency_model_audit.py
6 passed
```

Figure validation:

```text
project_core_bem_symmetry_calibration_phase_magnitude_frequency_model_audit.png
2896x847, dynamic range=255
```
