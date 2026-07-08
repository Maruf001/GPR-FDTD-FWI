# BEM Experiment 733: Strict-Template Producer Input Acceptance Dry Run Validator

Date: 2026-07-01

## Purpose

Validate run `732` as a strict matched-FDTD producer input acceptance dry run.

This run is validation only. It does not execute FDTD, run BEM/FDTD
comparison, write live producer input files, run 3D validation, launch GPU/HPC
work, transfer to field data, or run field FWI.

## Output

```text
outputs/bem_experiments/733_project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                             7
passed checks:                      7
failed checks:                      0
dry-run files:                      2
template rows:                      558
strict contract hash matches:       558
strict contract hash errors:        0
accepted files:                     0
validation errors:                  2232
live input files present:           0
exporter execution ready:           false
field transfer ready:               false
validation ready:                   true
```

Validation checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source strict dry run ready | pass |
| 2 | file and row shape | pass |
| 3 | strict contract hashes pass | pass |
| 4 | blank templates rejected | pass |
| 5 | real-data error families | pass |
| 6 | downstream remains blocked | pass |
| 7 | figure and scripts exist | pass |

## Interpretation

The validator confirms that run `732` is a correct no-go dry run. The row
identities and strict contract hashes are valid, while exporter execution
remains blocked by missing real FDTD solver provenance and returned FDTD
values.

## Decision

Use run `732` as the current strict acceptance dry-run boundary. Do not promote
exporter execution or BEM/FDTD comparison until real live producer input files
pass strict acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run_validator.py
3 passed
```

Figure check:

```text
2285x857, dynamic range=255
```
