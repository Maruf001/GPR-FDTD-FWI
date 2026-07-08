# BEM Experiment 155: Symmetry Calibration Smooth Frequency Interpolation Audit

Date: 2026-06-27

## Purpose

Test smooth coefficient interpolation for the run `150`/`151` BEM symmetry
calibration candidate.

Runs `152` through `154` showed that global polynomial, nearest-neighbor, and
linear interpolation do not close the frequency-holdout gap. This run tests
three smoother interpolation families: cubic splines, PCHIP interpolation, and
Akima interpolation.

This is a CPU-only audit from saved bridge arrays. It does not rerun FDTD,
rerun BEM solvers, compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/155_project_core_bem_symmetry_calibration_smooth_frequency_interpolation_audit
```

Key artifacts:

```text
data/project_core_bem_symmetry_calibration_smooth_frequency_interpolation_rows.csv
data/project_core_bem_symmetry_calibration_smooth_frequency_interpolation_audit_summary.json
figures/project_core_bem_symmetry_calibration_smooth_frequency_interpolation_audit.png
docs/PROJECT_CORE_BEM_SYMMETRY_CALIBRATION_SMOOTH_FREQUENCY_INTERPOLATION_AUDIT.md
scripts/run_project_core_bem_symmetry_calibration_smooth_frequency_interpolation_audit.py
scripts/test_project_core_bem_symmetry_calibration_smooth_frequency_interpolation_audit.py
```

## Result

```text
candidate train receivers:                     0;2;4;6
candidate holdout receivers:                   1;3;5
candidate spatial degree:                      1
smooth methods:                                3
smooth interpolation rows:                     16
passing smooth interpolation rows:             0
alternating passing smooth rows:               0
best held-frequency scheme:                    even_train_odd_hold
best held-frequency method:                    pchip
best held-frequency relative L2:               0.1169203875467621
best holdout receiver held-frequency L2:       0.08738552226676755
smooth frequency interpolation ready:          false
project-core bridge ready:                     false
3D validation ready:                           false
field FWI ready:                               false
GPU/HPC ready:                                 false
```

Best smooth interpolation outcomes:

| Scheme | Best method | Held-frequency L2 | Holdout receiver held-frequency L2 | Passes |
| --- | --- | ---: | ---: | --- |
| even_train_odd_hold | pchip | 0.1169203875467621 | 0.08738552226676755 | false |
| odd_train_even_hold | akima | 0.13377502059010674 | 0.12497399787905542 | false |
| low_mid_high_sparse | pchip | 0.1306967579310097 | 0.11264399728213652 | false |
| drop_low_edge | akima | 0.11704123813863186 | 0.09549811429170904 | false |
| drop_high_edge | akima | 0.19647943153102287 | 0.21269692300472653 | false |
| drop_both_edges | akima | 0.14861493620687222 | 0.1464865498668703 | false |

## Interpretation

Cubic, PCHIP, and Akima interpolation do not close the frequency holdout gap.
No alternating frequency split passes, so simple smooth coefficient
interpolation is not enough.

The current BEM symmetry calibration design remains a per-frequency candidate,
not a frequency-generalized bridge.

## Decision

Keep the BEM symmetry calibration design as a per-frequency candidate. Do not
promote project-core comparison, 3D validation, GPU/HPC, or field FWI until a
stronger frequency model or fresh matched validation passes.

## Validation

Focused tests:

```text
tests/test_project_core_bem_symmetry_calibration_smooth_frequency_interpolation_audit.py
5 passed
```

Figure validation:

```text
project_core_bem_symmetry_calibration_smooth_frequency_interpolation_audit.png
2896x855, dynamic range=255
```
