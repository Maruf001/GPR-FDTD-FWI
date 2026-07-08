# BEM Experiment 769: Complex Metric Real-Return Package Template Pack

Date: 2026-07-01

## Purpose

Create an output-local real-return template pack for the BEM/FDTD complex
metric addendum files.

This run writes blank CSV templates only. It does not use real BEM values, does
not use real FDTD exports, does not accept templates as real returns, and does
not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/769_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack
```

Key artifacts:

```text
data/complex_metric_real_return_templates/
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_template_file_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source addendum ready:                 true
source intake ready:                   true
source consumer ready:                 true
template files:                        5
template rows:                         279
expected metric rows:                  279
template rows match required rows:     true
required columns per row:              13
blank required value cells:            3348
real FDTD exported true rows:          0
accepted as real returns:              0
output-local templates:                5
real BEM/FDTD comparison ready:        false
gpu priority:                          none
```

Template coverage:

| Stage | Rows | Blank required value cells |
| ---: | ---: | ---: |
| 1 | 1 | 12 |
| 2 | 8 | 96 |
| 3 | 30 | 360 |
| 4 | 120 | 1440 |
| 5 | 120 | 1440 |

## Interpretation

The real-return handoff now has five producer-facing CSV templates. Together
they cover all 279 receiver-frequency rows required by the complex metric
addendum schema. Each row has a stable `pair_id`, but the numerical fields,
normalization label, solver identifiers, solver status, log hash, and real FDTD
export flag are blank.

The templates are intentionally non-evidence. They live only inside this BEM
experiment output folder and are not placed in the live return area. If copied
into the live path without real solver values, the existing intake gate should
reject them because the required numeric and solver fields are blank.

## Decision

Use run `769` to guide future real BEM/FDTD complex metric returns. Keep real
BEM/FDTD comparison blocked until real live files pass the run `763-765` intake
block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack.py
5 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack.py: pass
```

Figure check:

```text
2212x846, dynamic range=255
```
