# BEM Experiment 764: Metric Addendum Intake Gate Validator

Date: 2026-07-01

## Purpose

Validate run `763` from saved outputs.

This run checks that the complex-valued metric addendum intake gate is
internally consistent: five expected files are represented, required rows and
cells are preserved, the current state remains pre-return, missing columns are
explicit while files are absent, and real comparison remains blocked.

This run does not use real BEM/FDTD values, run FDTD, make a real comparison
claim, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/764_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source intake gate ready:             true
validation checks:                    7
passed validation checks:             7
failed validation checks:             0
expected addendum files:              5
missing live files:                   5
required metric rows:                 279
required metric cells:                3627
required complex component cells:     1116
accepted files:                       0
accepted metric rows:                 0
metric addendum intake accepted:      false
real BEM/FDTD comparison ready:       false
gpu priority:                         none
```

Saved-output validation checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source intake gate ready | pass |
| 2 | five expected addendum files are represented | pass |
| 3 | required rows and cells are preserved | pass |
| 4 | current state remains pre-return | pass |
| 5 | missing columns are explicit while files are absent | pass |
| 6 | real comparison remains blocked | pass |
| 7 | figure and script snapshots are present | pass |

## Interpretation

The complex metric addendum intake gate is reproducible from saved artifacts.
The current state remains pre-return because the five expected files are still
absent.

## Decision

Use runs `763-764` as the guarded intake definition for future complex
BEM/FDTD metric files. Keep real comparison, 3D validation, GPU/HPC, field
transfer, and field FWI blocked until all five files pass intake.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_validator.py
4 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_validator.py: pass
tests/test_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
