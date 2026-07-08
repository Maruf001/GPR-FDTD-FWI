# BEM Experiment 077: 3D FDTD Frequency-Bin Import Template

Date: 2026-06-25

## Purpose

Write strict target/background frequency-bin CSV templates for future paired 3D
FDTD outputs. The receiver/frequency keys are prefilled from the run `073`
manifests, and the future FDTD extractor only needs to fill the six complex
field columns.

This is CPU-only import scaffolding. It does not launch 3D FDTD, field FWI,
GPU/HPC work, or neural-network training.

## Output

```text
outputs/bem_experiments/077_project_core_bem_3d_fdtd_frequency_bin_import_template
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_target_frequency_bin_import_template.csv
data/project_core_bem_3d_fdtd_background_frequency_bin_import_template.csv
data/project_core_bem_3d_fdtd_frequency_bin_import_package.csv
data/project_core_bem_3d_fdtd_frequency_bin_import_template_summary.json
figures/project_core_bem_3d_fdtd_frequency_bin_import_template.png
docs/PROJECT_CORE_BEM_3D_FDTD_FREQUENCY_BIN_IMPORT_TEMPLATE.md
```

## Result

```text
target template rows:                  124
background template rows:              124
required schema columns:               12
component columns to fill:             6
blank component cells:                 1488
strict columns match comparator:        true
matches run 075 target expected rows:  true
matches run 075 background rows:       true
import templates ready:                true
real FDTD data ready:                  false
comparison ready:                      false
3D validation claim ready:             false
```

## Interpretation

The future paired FDTD handoff is now explicit at the CSV level. Each side must
provide 124 rows: 31 receivers times four frequencies. The target and
background import templates already contain the exact receiver/frequency keys
and the exact 12 columns required by the run `075` comparator.

This removes manual table-shaping ambiguity but does not create real FDTD
field values. The 1,488 blank component cells are the work future FDTD
extraction must fill before comparison.

## Decision

Use these templates as the import surface for real paired FDTD target and
background data. Keep comparison, 3D validation, field FWI, heavy GPU work,
field 3D/HPC, and neural-network training blocked until the six complex field
columns are filled for both sides and pass the run `075` comparator.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_frequency_bin_import_template.py
3 passed
```

Figure check:

```text
1997x808, dynamic range=255
```
