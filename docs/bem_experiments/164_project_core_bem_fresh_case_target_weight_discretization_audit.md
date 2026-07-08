# BEM Experiment 164: Fresh-Case Target-Weight Discretization Audit

Date: 2026-06-27

## Purpose

Test whether changing the target-cell quadrature weights in the project-core
grid-aware adapter reduces the fresh-case mismatch.

Runs `159` through `163` ruled out scalar factors, empirical scale tables, and
pure timing-delay phase ramps as bridge fixes. This run changes the target-cell
weighting itself and recomputes the local CPU adapter for the three fresh
cases.

This is a CPU-only project-core adapter recomputation. It does not compare
against field data, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/164_project_core_bem_fresh_case_target_weight_discretization_audit
```

Key artifacts:

```text
data/project_core_bem_fresh_case_target_weight_discretization_case_rows.csv
data/project_core_bem_fresh_case_target_weight_discretization_variant_rows.csv
data/project_core_bem_fresh_case_target_weight_discretization_audit_summary.json
figures/project_core_bem_fresh_case_target_weight_discretization_audit.png
docs/PROJECT_CORE_BEM_FRESH_CASE_TARGET_WEIGHT_DISCRETIZATION_AUDIT.md
scripts/run_project_core_bem_fresh_case_target_weight_discretization_audit.py
scripts/test_project_core_bem_fresh_case_target_weight_discretization_audit.py
```

## Result

```text
fresh cases:                         3
weight modes:                        5
formula variant rows:                45
case improvements:                   3
meaningful improvements >= 0.01:     0
strict-gate passes:                  0
all best cases pass gate:            false
worst best case:                     shifted_deeper_epsr4
worst best weight mode:              binary_contrast_area
worst best L2:                       0.5987298321189344
max best improvement vs subcell:     0.006334741287308349
target-weight discretization ready:  false
project-core bridge ready:           false
3D validation ready:                 false
field FWI ready:                     false
GPU/HPC ready:                       false
```

| Case | Subcell best L2 | Best weight mode | Best formula | Best L2 | Improvement |
| --- | ---: | --- | --- | ---: | ---: |
| lower_contrast_radius_25mm | 0.18685792461171657 | binary_contrast_area | product_no_div | 0.18052318332440823 | 0.006334741287308349 |
| shifted_deeper_epsr4 | 0.5997321402926066 | binary_contrast_area | receiver_conjugate_div_source | 0.5987298321189344 | 0.001002308173672195 |
| larger_high_contrast_epsr6 | 0.5119171157297535 | binary_contrast_area | product_no_div | 0.5104330810109461 | 0.0014840347188074254 |

## Interpretation

Binary or uniform target-cell weighting gives small improvements in all three
fresh cases. The gains are far too small to close the strict scattered-field
gate. The worst case remains near `0.599` relative L2.

## Decision

Keep the project-core bridge blocked. Target-cell weight discretization alone
is not the missing operator change. Prioritize Green-function structure,
material/interface modeling, or source/receiver aperture effects before 3D
validation, GPU/HPC, or field FWI.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fresh_case_target_weight_discretization_audit.py
5 passed
```

Figure validation:

```text
project_core_bem_fresh_case_target_weight_discretization_audit.png
2896x842, dynamic range=255
```
