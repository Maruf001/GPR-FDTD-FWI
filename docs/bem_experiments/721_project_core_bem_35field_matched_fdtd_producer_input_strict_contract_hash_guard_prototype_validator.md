# BEM Experiment 721: Producer Input Strict Contract-Hash Guard Prototype Validator

Date: 2026-07-01

## Purpose

Validate the saved run `720` strict contract-hash guard prototype.

The validator checks that the guard accepts the two canonical hash cases,
rejects the two arbitrary-hash cases and four damaged hash cases, and keeps all
downstream execution blocked.

This is CPU-only artifact validation. It does not run FDTD, execute the shared
exporter on real files, create accepted return files, run a real BEM/FDTD
comparison, launch GPU/HPC work, transfer to field evidence, or promote 3D
validation claims.

## Output

```text
outputs/bem_experiments/721_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                               7
checks passed:                        7
checks failed:                        0
producer input file keys:             2
required producer rows:             558
strict guard pass cases:              2
strict guard fail cases:              6
arbitrary hashes rejected:            2
ready for shared exporter patch:   true
exporter execution ready:         false
```

## Interpretation

The strict guard prototype is validated and preserves all downstream blockers.

## Decision

Use this as the tested basis for a shared-exporter patch.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype_validator.py
2 passed
```

Figure check:

```text
2465x859, dynamic range=255
```
