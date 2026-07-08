# BEM Experiment 719: Producer Input Strict Contract-Hash Policy Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `718` strict contract-hash audit validator.

The sensitivity audit checks that the validator accepts the exact run `717`
state and rejects damaged or falsely promoted states, including missing contract
rows, damaged hashes, missing probe evidence, false exact-hash enforcement, and
false exporter/GPU readiness.

This is CPU-only validator sensitivity auditing. It does not run FDTD, execute
the exporter on real files, create accepted return files, run a real BEM/FDTD
comparison, launch GPU/HPC work, transfer to field evidence, or promote 3D
validation claims.

## Output

```text
outputs/bem_experiments/719_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit_validation_sensitivity_case_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity cases:                    17
expected pass cases:                   1
expected fail cases:                  16
actual pass cases:                     1
actual fail cases:                    16
unexpected outcomes:                   0
damaged cases:                        16
exporter execution ready:          false
real BEM/FDTD comparison ready:     false
GPU/HPC ready:                     false
```

## Interpretation

The validator accepts only the exact strict-hash audit state. It rejects damaged
contract hashes, missing probe evidence, false exact-enforcement claims, false
exporter readiness, and false downstream promotion.

## Decision

Use run `717` as the guarded basis for a later exporter hardening patch.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit_validation_sensitivity.py
2 passed
```

Figure check:

```text
2753x872, dynamic range=255
```
