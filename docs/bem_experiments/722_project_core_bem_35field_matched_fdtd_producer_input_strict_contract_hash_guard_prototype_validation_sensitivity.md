# BEM Experiment 722: Producer Input Strict Contract-Hash Guard Prototype Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `721` strict contract-hash guard prototype validator.

The sensitivity audit checks that the validator accepts the exact run `720`
state and rejects damaged or falsely promoted states, including wrong probe
counts, false pass/fail counts, canonical-hash rejection, arbitrary-hash
acceptance, and false exporter/GPU readiness.

This is CPU-only validator sensitivity auditing. It does not run FDTD, execute
the shared exporter on real files, create accepted return files, run a real
BEM/FDTD comparison, launch GPU/HPC work, transfer to field evidence, or
promote 3D validation claims.

## Output

```text
outputs/bem_experiments/722_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype_validation_sensitivity_case_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype_validation_sensitivity.png
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

The validator accepts only the exact strict-guard prototype. It rejects damaged
guard outputs and false downstream promotion.

## Decision

Proceed only to a guarded shared-exporter patch.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_guard_prototype_validation_sensitivity.py
2 passed
```

Figure check:

```text
2753x874, dynamic range=255
```
