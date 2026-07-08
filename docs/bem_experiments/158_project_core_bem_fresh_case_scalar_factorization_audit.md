# BEM Experiment 158: Fresh-Case Scalar Factorization Audit

Date: 2026-06-27

## Purpose

Test whether the saved fresh-case project-core adapter mismatch can be
explained by simple scalar amplitude or phase factors.

Run `157` showed that the original symmetry calibration does not transfer to
the three fresh run `094` cases. This run asks a simpler physical question:
does a global or per-frequency complex scalar, fitted only on training
receivers, improve held-out receivers?

This is a CPU-only audit from saved BEM-track arrays. It does not rerun FDTD,
rerun BEM solvers, compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/158_project_core_bem_fresh_case_scalar_factorization_audit
```

Key artifacts:

```text
data/project_core_bem_fresh_case_scalar_factorization_rows.csv
data/project_core_bem_fresh_case_scalar_factorization_audit_summary.json
figures/project_core_bem_fresh_case_scalar_factorization_audit.png
docs/PROJECT_CORE_BEM_FRESH_CASE_SCALAR_FACTORIZATION_AUDIT.md
scripts/run_project_core_bem_fresh_case_scalar_factorization_audit.py
scripts/test_project_core_bem_fresh_case_scalar_factorization_audit.py
```

## Result

```text
fresh cases:                            3
factor models:                          4
scalar rows:                            12
deployable scalar rows:                 6
deployable scalar factor passes:        0
deployable holdout improvements:        0
oracle strict-gate passes:              0
best deployable holdout case:           lower_contrast_radius_25mm
best deployable holdout model:          global_train_scalar
best deployable holdout L2:             0.18135484838602173
best deployable holdout delta:          0.0009197166572267046
scalar factorization ready:             false
simple source-factor explanation ready: false
project-core bridge ready:              false
3D validation ready:                    false
field FWI ready:                        false
GPU/HPC ready:                          false
```

Deployable scalar rows:

| Case | Model | Full L2 | Holdout L2 | Holdout delta | Passes |
| --- | --- | ---: | ---: | ---: | --- |
| lower_contrast_radius_25mm | global_train_scalar | 0.18711987338902178 | 0.18135484838602173 | 0.0009197166572267046 | false |
| lower_contrast_radius_25mm | per_frequency_train_scalar | 0.18840250065386588 | 0.18596528427971643 | 0.005530152550921402 | false |
| shifted_deeper_epsr4 | global_train_scalar | 0.6005550027077914 | 0.5690312825167175 | 0.0031887037993977296 | false |
| shifted_deeper_epsr4 | per_frequency_train_scalar | 0.605000960137882 | 0.5861031256926741 | 0.020260546975354288 | false |
| larger_high_contrast_epsr6 | global_train_scalar | 0.5123731990537908 | 0.48704914188803367 | 0.001730868619682413 | false |
| larger_high_contrast_epsr6 | per_frequency_train_scalar | 0.5161435397643421 | 0.5014966599177554 | 0.01617838664940413 | false |

## Interpretation

Train-receiver scalar factors do not improve held-out receivers on the fresh
cases, and no deployable scalar row reaches the strict gate. A simple
source-amplitude, global phase, or per-frequency scalar explanation is
therefore not supported.

## Decision

Keep the project-core bridge blocked. The next BEM adapter work should focus on
structural field/operator mismatch rather than scalar source or amplitude
normalization.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fresh_case_scalar_factorization_audit.py
5 passed
```

Figure validation:

```text
project_core_bem_fresh_case_scalar_factorization_audit.png
2896x842, dynamic range=255
```
