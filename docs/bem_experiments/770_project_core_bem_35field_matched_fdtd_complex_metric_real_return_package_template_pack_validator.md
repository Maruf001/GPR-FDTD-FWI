# BEM Experiment 770: Complex Metric Real-Return Package Template Pack Validator

Date: 2026-07-01

## Purpose

Validate the saved run `769` BEM/FDTD complex metric real-return template pack
from disk.

This run does not use real BEM values, does not use real FDTD exports, does not
accept templates as real returns, and does not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/770_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validator_observed_template_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source template pack ready:           true
validation checks:                    7
passed validation checks:             7
failed validation checks:             0
template files:                       5
template rows:                        279
blank required value cells:           3348
accepted as real returns:             0
real FDTD exported true rows:         0
real BEM/FDTD comparison ready:       false
gpu priority:                         none
```

Validation checks:

| Check | Result |
| --- | --- |
| source template pack ready | pass |
| five template files and 279 rows represented | pass |
| required columns are present in every template | pass |
| value fields remain blank and pair identifiers are present | pass |
| templates are output-local and not accepted as real returns | pass |
| real comparison remains blocked | pass |
| figure and script snapshots are present | pass |

## Interpretation

The saved real-return templates preserve the required complex metric schema.
They contain five files, 279 total rows, stable pair identifiers, all required
columns, and blank solver-produced fields.

The validator also confirms the claim boundary: no template is accepted as a
real return, no row claims a real FDTD export, and real BEM/FDTD comparison is
still blocked.

## Decision

Use run `770` as the saved-artifact validator for the run `769` template pack.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validator.py
9 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validator.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
