# BEM Experiment 369: Real-Pair Return Packet Intake Worksheet Validator

Date: 2026-06-29

## Purpose

Validate the saved run `368` BEM/FDTD return-packet intake worksheet from
artifacts.

This run checks the worksheet counts, directory coverage, action-group
coverage, template non-evidence status, blocked real-packet state, derived row
expectations, figure validation, and script snapshots.

## Output

```text
outputs/bem_experiments/369_project_core_bem_real_pair_return_packet_intake_worksheet_validator
```

Key artifacts:

```text
data/project_core_bem_real_pair_return_packet_intake_worksheet_validator_checks.csv
data/project_core_bem_real_pair_return_packet_intake_worksheet_validator_summary.json
figures/project_core_bem_real_pair_return_packet_intake_worksheet_validator.png
docs/PROJECT_CORE_BEM_REAL_PAIR_RETURN_PACKET_INTAKE_WORKSHEET_VALIDATOR.md
scripts/
```

## Result

```text
validation checks:              8
passed checks:                  8
failed checks:                  0
validation ready:               true
packet items:                   34
projected trace files:          26
metadata/control items:         8
template files:                 35
missing packet items:           34
real packet files present:      false
real comparison ready:          false
threshold calibration ready:    false
GPU work ready:                 false
field transfer ready:           false
3D validation ready:            false
```

## Interpretation

The saved intake worksheet is internally consistent and remains non-evidence:
templates are present, but real packet files are still absent.

## Decision

Use run `369` as the validator for the run `368` intake worksheet. Real
comparison and threshold calibration remain blocked until real packet files
pass the acceptance gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_real_pair_return_packet_intake_worksheet_validator.py
3 passed
```

Python compile check:

```text
run_project_core_bem_real_pair_return_packet_intake_worksheet_validator.py: pass
tests/test_project_core_bem_real_pair_return_packet_intake_worksheet_validator.py: pass
```

Figure validation:

```text
3545x929, dynamic range=255
```
