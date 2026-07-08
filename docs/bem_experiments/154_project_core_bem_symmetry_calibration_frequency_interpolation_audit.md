# BEM Experiment 154: Symmetry Calibration Frequency Interpolation Audit

Date: 2026-06-27

## Purpose

Test local interpolation methods for the run `150`/`151` per-frequency
calibration candidate.

Run `152` showed that global polynomial interpolation does not make the
candidate frequency-generalized. Run `153` validated that no-go. This run
checks whether simpler local interpolation methods, nearest neighbor and
linear interpolation of correction coefficients, close the frequency holdout
gap.

This is a CPU-only audit from saved bridge arrays. It does not rerun FDTD,
rerun BEM solvers, compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/154_project_core_bem_symmetry_calibration_frequency_interpolation_audit
```

Key artifacts:

```text
data/project_core_bem_symmetry_calibration_frequency_interpolation_rows.csv
data/project_core_bem_symmetry_calibration_frequency_interpolation_audit_summary.json
figures/project_core_bem_symmetry_calibration_frequency_interpolation_audit.png
docs/PROJECT_CORE_BEM_SYMMETRY_CALIBRATION_FREQUENCY_INTERPOLATION_AUDIT.md
scripts/run_project_core_bem_symmetry_calibration_frequency_interpolation_audit.py
scripts/test_project_core_bem_symmetry_calibration_frequency_interpolation_audit.py
```

## Result

```text
candidate train receivers:                 0;2;4;6
candidate holdout receivers:               1;3;5
candidate spatial degree:                  1
interpolation methods:                     2
interpolation rows:                        12
passing interpolation rows:                0
alternating passing interpolation rows:    0
best held-frequency scheme:                even_train_odd_hold
best held-frequency method:                linear
best held-frequency relative L2:           0.1116397436685101
best holdout receiver held-frequency L2:   0.08506285997113756
frequency interpolation ready:             false
project-core bridge ready:                 false
3D validation ready:                       false
field FWI ready:                           false
GPU/HPC ready:                             false
```

Method results:

| Scheme | Method | Held-frequency L2 | Holdout receiver held-frequency L2 | Passes |
| --- | --- | ---: | ---: | --- |
| even_train_odd_hold | linear | 0.1116397436685101 | 0.08506285997113756 | false |
| even_train_odd_hold | nearest | 0.1271161977099324 | 0.09598831668014958 | false |
| odd_train_even_hold | linear | 0.1328702143802861 | 0.12379352727571132 | false |
| odd_train_even_hold | nearest | 0.1650827105802914 | 0.14157457921347189 | false |
| drop_low_edge | linear | 0.11704123813863186 | 0.09549811429170904 | false |
| drop_high_edge | linear | 0.19647943153102287 | 0.21269692300472653 | false |
| drop_both_edges | linear | 0.14861493620687222 | 0.1464865498668703 | false |

## Interpretation

Nearest-neighbor and linear interpolation do not close the frequency holdout
gap. The best held-frequency result remains above the `0.1` gate, and no
alternating frequency split passes.

This means the current BEM adapter candidate remains a per-frequency
calibration candidate. It is not yet a frequency-generalized bridge.

## Decision

Keep the BEM symmetry calibration design as a per-frequency candidate. Do not
promote project-core comparison, 3D validation, GPU/HPC, or field FWI until a
stronger frequency model or fresh matched validation passes.

## Validation

Focused tests:

```text
tests/test_project_core_bem_symmetry_calibration_frequency_interpolation_audit.py
5 passed
```

Figure validation:

```text
project_core_bem_symmetry_calibration_frequency_interpolation_audit.png
2896x844, dynamic range=255
```
