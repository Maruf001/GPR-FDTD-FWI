# BEM Experiment 159: Fresh-Case Structural Residual Localization Audit

Date: 2026-06-27

## Purpose

Localize the residual mismatch in the three fresh project-core cases after the
symmetry-calibration transfer and scalar-factor explanations failed.

Runs `157` and `158` showed that the single-case symmetry calibration does not
transfer and that simple global or per-frequency scalar factors do not improve
held-out receivers. This run asks where the remaining fresh-case residual is
concentrated across receivers and frequencies.

This is a CPU-only audit from saved BEM-track arrays. It does not rerun FDTD,
rerun BEM solvers, compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/159_project_core_bem_fresh_case_structural_residual_localization_audit
```

Key artifacts:

```text
data/project_core_bem_fresh_case_structural_residual_case_rows.csv
data/project_core_bem_fresh_case_structural_residual_receiver_rows.csv
data/project_core_bem_fresh_case_structural_residual_frequency_rows.csv
data/project_core_bem_fresh_case_structural_residual_localization_audit_summary.json
figures/project_core_bem_fresh_case_structural_residual_localization_audit.png
docs/PROJECT_CORE_BEM_FRESH_CASE_STRUCTURAL_RESIDUAL_LOCALIZATION_AUDIT.md
scripts/run_project_core_bem_fresh_case_structural_residual_localization_audit.py
scripts/test_project_core_bem_fresh_case_structural_residual_localization_audit.py
```

## Result

```text
fresh cases:                             3
worst case:                              shifted_deeper_epsr4
worst case relative L2:                  0.5997321402926066
most common top receiver index:          6
top receiver consistent cases:           3
max top receiver energy fraction:        0.2818350658783482
min top-5 frequency energy fraction:     0.6363043457279565
max top-5 frequency energy fraction:     0.6572763240658624
structural residual localization ready:  true
scalar factor explanation ready:         false
symmetry calibration transfer ready:     false
project-core bridge ready:               false
3D validation ready:                     false
field FWI ready:                         false
GPU/HPC ready:                           false
```

Case localization:

| Case | L2 | Top receiver | Top receiver fraction | Top frequency Hz | Top-5 frequency fraction |
| --- | ---: | ---: | ---: | ---: | ---: |
| lower_contrast_radius_25mm | 0.18685792461171657 | 6 | 0.1887262858834605 | 2748998620.694625 | 0.6383710940647526 |
| shifted_deeper_epsr4 | 0.5997321402926066 | 6 | 0.2818350658783482 | 2124226206.9003918 | 0.6363043457279565 |
| larger_high_contrast_epsr6 | 0.5119171157297535 | 6 | 0.18584455841243264 | 1124590344.8296192 | 0.6572763240658624 |

## Interpretation

The fresh-case residual is structured rather than scalar. Receiver `6` is the
largest residual-energy receiver in all three fresh cases, and the top five
frequency bins carry more than 63 percent of residual energy in each case.

## Decision

Keep the project-core bridge blocked. The next BEM adapter branch should target
receiver-edge and frequency-local operator mismatch on fresh cases, not scalar
source normalization or the single-case symmetry calibration.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fresh_case_structural_residual_localization_audit.py
4 passed
```

Figure validation:

```text
project_core_bem_fresh_case_structural_residual_localization_audit.png
2896x842, dynamic range=255
```
