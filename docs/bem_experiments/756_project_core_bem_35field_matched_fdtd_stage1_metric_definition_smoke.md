# BEM Experiment 756: Stage-1 Metric Definition Smoke

Date: 2026-07-01

## Purpose

Define the numerical metrics that will be used when real matched BEM/FDTD
values arrive.

Run `755` showed that the stage-1 positive-control rows cannot feed a real
comparison. This run adds a deliberately tiny synthetic pair only to exercise
the formulas for amplitude error, wrapped phase error, and complex relative
error.

This run does not use real BEM/FDTD values, run FDTD, make a real comparison
claim, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/756_project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_metric_rows.csv
data/project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_summary.json
figures/project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source handoff guard ready:          true
synthetic metric rows:               2
full strict file rows required:      558
receiver-frequency pairs required:   279
max amplitude relative error:        0.104315
max absolute phase error:            6.340192 degrees
max complex relative error:          0.156174
metric formula ready:                true
uses real BEM/FDTD values:           false
real BEM/FDTD comparison ready:      false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

Metric rows:

| Case | Receiver | Frequency | Amplitude relative error | Phase error | Complex relative error |
| --- | ---: | ---: | ---: | ---: | ---: |
| synthetic center pair | 15 | 1.00 GHz | 0.104315 | 6.340192 deg | 0.156174 |
| synthetic off-center pair | 16 | 1.25 GHz | 0.004963 | 5.710593 deg | 0.099504 |

## Interpretation

The amplitude, phase, and complex-error formulas are executable and tested on
complex-valued rows. Phase error is wrapped into the `[-180, 180]` degree
range before absolute phase error is reported.

The rows are synthetic by construction. They do not measure BEM/FDTD agreement
and do not change the comparison decision boundary.

## Decision

Use run `756` as the metric-definition smoke for the future matched BEM/FDTD
comparison. Keep real comparison, 3D validation, GPU/HPC, field transfer, and
field FWI blocked until the full strict live-return files contain real numeric
values.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke.py
4 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke.py: pass
tests/test_project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke.py: pass
```

Figure check:

```text
1852x850, dynamic range=255
```
