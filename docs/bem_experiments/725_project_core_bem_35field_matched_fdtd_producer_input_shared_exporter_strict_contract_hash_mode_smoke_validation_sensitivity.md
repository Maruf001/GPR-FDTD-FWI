# BEM Experiment 725: Shared Exporter Strict Contract-Hash Mode Smoke Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `724` shared-exporter strict-mode validator.

The sensitivity audit checks that the validator accepts the exact run `723`
state and rejects damaged or falsely promoted states, including false strict
pass counts, arbitrary-hash acceptance, unexpected command-line smoke results,
false real evidence, and false downstream readiness.

This is CPU-only validator sensitivity auditing. It does not run FDTD, accept
live producer files, create real evidence, run a real BEM/FDTD comparison,
launch GPU/HPC work, transfer to field evidence, or promote 3D validation
claims.

## Output

```text
outputs/bem_experiments/725_project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke_validation_sensitivity_case_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity cases:                   17
expected pass cases:                  1
expected fail cases:                 16
actual pass cases:                    1
actual fail cases:                   16
unexpected outcomes:                  0
damaged cases:                       16
exporter execution ready:         false
real BEM/FDTD comparison ready:    false
GPU/HPC ready:                    false
```

## Interpretation

The validator accepts only the exact shared-exporter strict-mode smoke state.
It rejects damaged strict-mode behavior and false downstream promotion.

## Decision

Use strict mode for future real matched-FDTD producer input acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke_validation_sensitivity.py
2 passed
```

Figure check:

```text
2753x876, dynamic range=255
```
