# BEM Experiment 078: 3D FDTD Import Template Smoke

Date: 2026-06-25

## Purpose

Fill the run `077` target/background frequency-bin import templates with
deterministic finite synthetic field values, then check the filled tables with
the run `075` comparator preflight.

This is CPU-only schema smoke. It does not launch 3D FDTD, field FWI, GPU/HPC
work, or neural-network training.

## Output

```text
outputs/bem_experiments/078_project_core_bem_3d_fdtd_frequency_bin_import_template_smoke
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_target_frequency_bin_import_template_smoke.csv
data/project_core_bem_3d_fdtd_background_frequency_bin_import_template_smoke.csv
data/project_core_bem_3d_fdtd_frequency_bin_import_template_smoke_checks.csv
data/project_core_bem_3d_fdtd_frequency_bin_import_template_smoke_summary.json
figures/project_core_bem_3d_fdtd_frequency_bin_import_template_smoke.png
docs/PROJECT_CORE_BEM_3D_FDTD_FREQUENCY_BIN_IMPORT_TEMPLATE_SMOKE.md
```

## Result

```text
target synthetic rows:                    124
background synthetic rows:                124
target blank component cells after fill:  0
background blank component cells:         0
comparator checks:                        22
comparator failed checks:                 0
synthetic import smoke pass:              true
real FDTD data ready:                     false
comparison ready:                         false
3D validation claim ready:                false
```

## Interpretation

The run `077` import templates can be filled and accepted by the run `075`
comparator when every target/background receiver-frequency row has finite
complex field components.

This proves the import surface is mechanically usable. It is not real FDTD
data, not a BEM/FDTD comparison, and not 3D validation.

## Decision

Use this as an import-template smoke test. Keep real comparison, 3D validation,
field FWI, heavy GPU work, field 3D/HPC, and neural-network training blocked
until actual paired FDTD target/background outputs fill the same templates.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_frequency_bin_import_template_smoke.py
2 passed
```

Figure check:

```text
1924x810, dynamic range=255
```
