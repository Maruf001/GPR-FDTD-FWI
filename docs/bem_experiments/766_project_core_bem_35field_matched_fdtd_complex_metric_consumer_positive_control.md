# BEM Experiment 766: Complex Metric Consumer Positive Control

Date: 2026-07-01

## Purpose

Verify that the BEM/FDTD complex metric consumer can process the five-file
addendum shape defined in run `760`.

This run uses output-local synthetic complex values only. It does not use real
FDTD exports, does not accept the synthetic files as real addendum returns, and
does not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/766_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_metric_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_stage_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_synthetic_file_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_summary.json
data/synthetic_complex_metric_addendum/
figures/project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source addendum ready:                 true
synthetic addendum files:              5
synthetic metric rows:                 279
expected metric rows:                  279
required fields per row:               13
required complex component cells:      1116
computed metric rows:                  279
max amplitude relative error:          0.047619
max absolute phase error:              2.75 degrees
max complex relative error:            0.066792
real FDTD exported true rows:          0
synthetic positive-control rows:       279
schema shape compatible:               true
uses real BEM/FDTD values:             false
real BEM/FDTD comparison ready:        false
```

Stage coverage:

| Stage | Rows | Max amplitude relative error | Max phase error (degrees) | Max complex relative error |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 0.009901 | 1.75 | 0.031963 |
| 2 | 8 | 0.019608 | 2.00 | 0.039736 |
| 3 | 30 | 0.029126 | 2.25 | 0.048429 |
| 4 | 120 | 0.038462 | 2.50 | 0.057529 |
| 5 | 120 | 0.047619 | 2.75 | 0.066792 |

## Interpretation

The consumer mechanics now cover the full 279-row addendum shape. The metric
calculator can read schema-shaped complex values, compute amplitude relative
error, wrapped phase error, and complex relative error across all five stages,
and produce stage-level summaries.

This is not real comparison evidence. The rows are synthetic positive controls,
and `real_fdtd_exported` remains false for every row. Real comparison remains
blocked until the five real exported addendum files pass the run `763-765`
intake block.

## Decision

Use run `766` as BEM/FDTD complex-metric consumer mechanics coverage. Do not use
it as real BEM/FDTD agreement evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control.py
4 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control.py: pass
```

Figure check:

```text
2212x846, dynamic range=255
```
