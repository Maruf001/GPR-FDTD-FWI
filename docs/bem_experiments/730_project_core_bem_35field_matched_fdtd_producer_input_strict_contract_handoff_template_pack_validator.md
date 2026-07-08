# BEM Experiment 730: Producer Input Strict-Contract Handoff Template Pack Validator

Date: 2026-07-01

## Purpose

Validate the saved run `729` strict-contract producer input handoff templates.

The validator checks that the templates preserve 558 rows, prefill 558 exact
contract hashes, keep real solver and value fields blank, and do not promote
exporter execution or real comparison.

This is CPU-only artifact validation. It does not run FDTD, write live producer
files, execute the exporter on live files, create real evidence, run a real
BEM/FDTD comparison, launch GPU/HPC work, transfer to field evidence, or
promote 3D validation claims.

## Output

```text
outputs/bem_experiments/730_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                                7
checks passed:                         7
checks failed:                         0
template files:                        2
template rows:                       558
prefilled exact contract hashes:     558
blank real solver provenance cells: 2232
blank returned FDTD values:          558
completed actions:                     1
exporter execution ready:          false
```

## Interpretation

The strict-contract handoff templates validate as non-live templates with exact
hashes prefilled.

## Decision

Use the templates for handoff only. Keep exporter execution blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack_validator.py
2 passed
```

Figure check:

```text
2393x859, dynamic range=255
```
