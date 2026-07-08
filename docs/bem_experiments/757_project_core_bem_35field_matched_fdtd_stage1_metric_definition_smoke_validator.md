# BEM Experiment 757: Stage-1 Metric Definition Smoke Validator

Date: 2026-07-01

## Purpose

Validate run `756` from saved outputs.

This run checks that the metric-definition smoke is internally consistent:
the synthetic rows remain synthetic, the amplitude/phase/complex-error
formulas recompute from saved values, metric maxima match the row data, and
real BEM/FDTD comparison remains blocked.

This run does not use real BEM/FDTD values, run FDTD, make a real comparison
claim, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/757_project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source metric smoke ready:           true
validation checks:                   7
passed validation checks:            7
failed validation checks:            0
synthetic metric rows:               2
full strict file rows required:      558
receiver-frequency pairs required:   279
metric formula ready:                true
uses real BEM/FDTD values:           false
real BEM/FDTD comparison ready:      false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

Saved-output validation checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source metric smoke ready | pass |
| 2 | synthetic rows remain synthetic | pass |
| 3 | metric formulas recompute | pass |
| 4 | metric maxima are preserved | pass |
| 5 | strict comparison boundary is preserved | pass |
| 6 | downstream states remain blocked | pass |
| 7 | figure and script snapshots are present | pass |

## Interpretation

Run `756` is reproducible from saved artifacts. The metric formulas are now
checked independently of the live script execution path.

The validation does not make a BEM/FDTD agreement claim because the metric rows
are synthetic and the full strict real-return set is still absent.

## Decision

Use runs `756-757` as the metric-definition block for future real numeric
BEM/FDTD comparison. Keep real comparison, 3D validation, GPU/HPC, field
transfer, and field FWI blocked until all 558 strict rows contain accepted
real values.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_validator.py
4 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_validator.py: pass
tests/test_project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
