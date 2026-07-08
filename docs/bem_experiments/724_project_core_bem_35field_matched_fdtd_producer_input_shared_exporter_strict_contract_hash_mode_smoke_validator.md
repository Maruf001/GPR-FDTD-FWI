# BEM Experiment 724: Shared Exporter Strict Contract-Hash Mode Smoke Validator

Date: 2026-07-01

## Purpose

Validate the saved run `723` shared-exporter strict contract-hash mode smoke.

The validator checks that strict mode is available, canonical hashes pass,
arbitrary hashes fail, the synthetic command-line smoke has expected return
codes, and no real evidence or downstream readiness is created.

This is CPU-only artifact validation. It does not run FDTD, accept live
producer files, create real evidence, run a real BEM/FDTD comparison, launch
GPU/HPC work, transfer to field evidence, or promote 3D validation claims.

## Output

```text
outputs/bem_experiments/724_project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                               6
checks passed:                        6
checks failed:                        0
strict mode available:             true
strict-mode pass cases:               2
strict-mode fail cases:               6
arbitrary hashes rejected:            2
synthetic accepted files:             1
real evidence files:                  0
exporter execution ready:         false
```

## Interpretation

The strict-mode smoke validates on synthetic probes and does not create real
evidence.

## Decision

Use strict mode for future real matched-FDTD producer input acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke_validator.py
2 passed
```

Figure check:

```text
2285x838, dynamic range=255
```
