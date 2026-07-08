# BEM Experiment 718: Producer Input Strict Contract-Hash Policy Audit Validator

Date: 2026-07-01

## Purpose

Validate the saved run `717` strict contract-hash audit.

The validator checks that the two canonical contract hashes cover both
matched-FDTD producer input files, the audit exposes the arbitrary-hash
acceptance gap, and all exporter/comparison/GPU/HPC paths remain blocked.

This is CPU-only artifact validation. It does not run FDTD, execute the
exporter on real files, create accepted return files, run a real BEM/FDTD
comparison, launch GPU/HPC work, transfer to field evidence, or promote 3D
validation claims.

## Output

```text
outputs/bem_experiments/718_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                                7
checks passed:                         7
checks failed:                         0
producer input file keys:              2
required producer rows:              558
arbitrary hex64 hashes accepted now:   2
strict-policy pass cases:              2
ready for hardening patch:          true
exporter execution ready:          false
```

## Interpretation

The audit is internally consistent. It identifies a real acceptance weakness
without promoting any current real-return evidence.

## Decision

Proceed only to a guarded exporter hardening patch. Keep real producer returns
blocked until exact contract-hash enforcement is validated.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit_validator.py
2 passed
```

Figure check:

```text
2465x865, dynamic range=255
```
