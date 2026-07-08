# BEM Experiment 157: Symmetry Calibration Fresh-Case Transfer Audit

Date: 2026-06-27

## Purpose

Test whether the run `150`/`151` BEM symmetry calibration candidate transfers
to independent project-core cases.

Run `156` ruled out simple phase wrapping as the explanation for the frequency
holdout gap. This run moves to a stronger validation question: apply the
original frozen symmetry calibration coefficients to the three fresh
project-core cases saved by run `094`, without refitting on those cases.

This is a CPU-only audit from saved BEM-track arrays. It does not rerun FDTD,
rerun BEM solvers, compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/157_project_core_bem_symmetry_calibration_fresh_case_transfer_audit
```

Key artifacts:

```text
data/project_core_bem_symmetry_calibration_fresh_case_transfer_rows.csv
data/project_core_bem_symmetry_calibration_fresh_case_transfer_audit_summary.json
figures/project_core_bem_symmetry_calibration_fresh_case_transfer_audit.png
docs/PROJECT_CORE_BEM_SYMMETRY_CALIBRATION_FRESH_CASE_TRANSFER_AUDIT.md
scripts/run_project_core_bem_symmetry_calibration_fresh_case_transfer_audit.py
scripts/test_project_core_bem_symmetry_calibration_fresh_case_transfer_audit.py
```

## Result

```text
original case baseline relative L2:             0.117062890994582
original case calibrated relative L2:           0.06410622276417251
original case holdout relative L2:              0.08334442794624965
fresh cases:                                    3
frozen transfer non-regression passes:          1
frozen transfer strict-gate passes:             0
same-case oracle full-improvement count:        0
same-case oracle holdout-improvement count:     0
best frozen transfer case:                      lower_contrast_radius_25mm
best frozen transfer relative L2:               0.21310977787624946
best frozen transfer holdout relative L2:       0.1919548954039901
worst frozen transfer regression case:          lower_contrast_radius_25mm
worst frozen transfer regression delta L2:      0.026251853264532887
fresh-case non-regression ready:                false
fresh-case transfer ready:                      false
project-core bridge ready:                      false
3D validation ready:                            false
field FWI ready:                                false
GPU/HPC ready:                                  false
```

Fresh-case transfer table:

| Case | Baseline L2 | Frozen transfer L2 | Baseline holdout L2 | Frozen holdout L2 | Non-regression | Strict gate |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| lower_contrast_radius_25mm | 0.18685792461171657 | 0.21310977787624946 | 0.18043513172879502 | 0.1919548954039901 | false | false |
| shifted_deeper_epsr4 | 0.5997321402926066 | 0.5905198028158744 | 0.5658425787173198 | 0.5614421219165107 | true | false |
| larger_high_contrast_epsr6 | 0.5119171157297535 | 0.5204036464521341 | 0.48531827326835125 | 0.4879914555668226 | false | false |

## Interpretation

The original symmetry calibration improves the original saved case, but it does
not transfer reliably to independent project-core cases. Only one of three
fresh cases is a non-regression, and no fresh case reaches the strict `0.1`
scattered-field gate.

The same-case refit diagnostic also fails to improve the fresh cases, which
means this calibration family is not a stable project-core adapter for the
saved run `094` cases.

## Decision

Do not promote the symmetry calibration branch to a project-core bridge, 3D
validation, GPU/HPC, or field FWI. Treat it as a local diagnostic for the
original saved case until a transfer-stable correction family is found.

This result makes the next BEM branch clearer: return to a physically grounded
project-core adapter family, not a receiver-position correction calibrated on a
single case.

## Validation

Focused tests:

```text
tests/test_project_core_bem_symmetry_calibration_fresh_case_transfer_audit.py
4 passed
```

Figure validation:

```text
project_core_bem_symmetry_calibration_fresh_case_transfer_audit.png
2896x842, dynamic range=255
```
