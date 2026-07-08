# BEM Experiment 165: Fresh-Case Aperture-Average Operator Audit

Date: 2026-06-27

## Purpose

Test whether lateral source/receiver aperture averaging reduces the fresh-case
project-core mismatch.

Run `164` showed that binary target-cell weighting gives the best small
improvement among simple target discretizations. This run keeps that binary
target weighting and compares point source/receiver fields against a three-
point 5 mm lateral aperture average.

This is a CPU-only project-core adapter recomputation. It does not compare
against field data, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/165_project_core_bem_fresh_case_aperture_average_operator_audit
```

Key artifacts:

```text
data/project_core_bem_fresh_case_aperture_average_case_rows.csv
data/project_core_bem_fresh_case_aperture_average_variant_rows.csv
data/project_core_bem_fresh_case_aperture_average_operator_audit_summary.json
figures/project_core_bem_fresh_case_aperture_average_operator_audit.png
docs/PROJECT_CORE_BEM_FRESH_CASE_APERTURE_AVERAGE_OPERATOR_AUDIT.md
scripts/run_project_core_bem_fresh_case_aperture_average_operator_audit.py
scripts/test_project_core_bem_fresh_case_aperture_average_operator_audit.py
```

## Result

```text
fresh cases:                         3
aperture modes:                      2
formula variant rows:                18
aperture improvements:               2
aperture regressions:                1
strict-gate passes:                  0
all best cases pass gate:            false
worst best case:                     shifted_deeper_epsr4
worst best mode:                     x3_5mm_aperture_binary_weight
worst best L2:                       0.598056418177049
max aperture improvement vs point:   0.0006734139418853591
aperture-average operator ready:     false
project-core bridge ready:           false
3D validation ready:                 false
field FWI ready:                     false
GPU/HPC ready:                       false
```

| Case | Point best L2 | Aperture best L2 | Aperture improvement | Overall best mode |
| --- | ---: | ---: | ---: | --- |
| lower_contrast_radius_25mm | 0.18052318332440823 | 0.18198863535931897 | -0.001465452034910747 | point_binary_weight |
| shifted_deeper_epsr4 | 0.5987298321189344 | 0.598056418177049 | 0.0006734139418853591 | x3_5mm_aperture_binary_weight |
| larger_high_contrast_epsr6 | 0.5104330810109461 | 0.5102417712653161 | 0.00019130974562997505 | x3_5mm_aperture_binary_weight |

## Interpretation

A simple three-point 5 mm lateral aperture average does not close the
fresh-case project-core gap. It slightly improves two cases, slightly regresses
one case, and all cases remain far above the strict scattered-field gate.

## Decision

Keep the project-core bridge blocked. A simple lateral aperture average is not
enough. Source/receiver modeling would need a more faithful antenna model or a
Green-function/interface update before 3D validation, GPU/HPC, or field FWI.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fresh_case_aperture_average_operator_audit.py
5 passed
```

Figure validation:

```text
project_core_bem_fresh_case_aperture_average_operator_audit.png
2896x842, dynamic range=255
```
