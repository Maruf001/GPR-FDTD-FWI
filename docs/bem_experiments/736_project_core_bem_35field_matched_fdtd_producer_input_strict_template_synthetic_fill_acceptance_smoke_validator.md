# BEM Experiment 736: Strict-Template Synthetic Fill Acceptance Smoke Validator

Date: 2026-07-01

## Purpose

Validate run `735` as an output-local synthetic positive control, not as real
BEM/FDTD evidence.

This run is validation only. It does not execute FDTD, create real BEM/FDTD
evidence, write live producer input files, run 3D validation, launch GPU/HPC
work, transfer to field data, or run field FWI.

## Output

```text
outputs/bem_experiments/736_project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                            6
passed checks:                     6
failed checks:                     0
synthetic files:                   2
synthetic input rows:              558
synthetic accepted files:          2
synthetic accepted rows:           558
synthetic validation errors:       0
real evidence ready files:         0
exporter execution ready:          false
field transfer ready:              false
validation ready:                  true
```

Validation checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source synthetic smoke ready | pass |
| 2 | synthetic file and row shape | pass |
| 3 | strict synthetic acceptance passes | pass |
| 4 | synthetic boundary preserved | pass |
| 5 | downstream remains blocked | pass |
| 6 | figure and scripts exist | pass |

## Interpretation

The validator confirms that the strict acceptance path is executable on
complete synthetic inputs while preserving the no-real-evidence boundary.

## Decision

Use run `735` as acceptance-path coverage only. Real matched-FDTD producer
input remains required before exporter execution, BEM/FDTD comparison, field
transfer, or 3D/GPU escalation.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke_validator.py
3 passed
```

Figure check:

```text
2285x856, dynamic range=255
```
