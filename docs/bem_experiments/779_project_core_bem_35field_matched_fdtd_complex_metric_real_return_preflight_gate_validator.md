# BEM Experiment 779: Complex Metric Real-Return Preflight Gate Validator

Date: 2026-07-01

## Purpose

Validate the saved run `778` BEM/FDTD complex metric real-return preflight gate
from disk.

This run does not create real solver-return files, does not stage files into
the live intake area, does not execute copy commands, does not accept template
files as real returns, and does not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/779_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source preflight gate ready:        true
validation checks:                  7
passed validation checks:           7
failed validation checks:           0
preflight files:                    5
required metric rows:               279
required columns:                   13
producer files present:             0
preflight-passed files:             0
ready-to-stage files:               0
executed commands:                  0
real BEM/FDTD comparison ready:     false
gpu priority:                       none
```

Validation checks:

| Check | Result |
| --- | --- |
| source preflight gate ready | pass |
| five files and 279 rows represented | pass |
| thirteen-column schema is enforced | pass |
| producer files remain absent | pass |
| no file passes or stages | pass |
| real comparison remains blocked | pass |
| figure and script snapshots are present | pass |

## Interpretation

The saved preflight gate is internally consistent. It preserves the five-file,
279-row, thirteen-column contract and keeps every real-return file non-stageable
while producer CSV files are absent.

## Decision

Use run `779` as the saved-artifact validator for the run `778` real-return
preflight gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validator.py
6 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validator.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
