# BEM Experiment 731: Producer Input Strict-Contract Handoff Template Pack Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `730` strict-contract template validator.

The sensitivity audit checks that the validator accepts the exact run `729`
template state and rejects missing hashes, changed row counts, falsely filled
solver/value fields, live-evidence promotion, and false exporter/GPU readiness.

This is CPU-only validator sensitivity auditing. It does not run FDTD, write
live producer files, execute the exporter on live files, create real evidence,
run a real BEM/FDTD comparison, launch GPU/HPC work, transfer to field
evidence, or promote 3D validation claims.

## Output

```text
outputs/bem_experiments/731_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack_validation_sensitivity_case_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity cases:                   16
expected pass cases:                  1
expected fail cases:                 15
actual pass cases:                    1
actual fail cases:                   15
unexpected outcomes:                  0
damaged cases:                       15
exporter execution ready:         false
real BEM/FDTD comparison ready:    false
GPU/HPC ready:                    false
```

## Interpretation

The validator accepts only the exact strict-contract template pack state. It
rejects damaged template counts, missing contract hashes, live-evidence
promotion, and false downstream readiness.

## Decision

Use the templates for handoff only. Keep exporter execution blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_handoff_template_pack_validation_sensitivity.py
2 passed
```

Figure check:

```text
2681x852, dynamic range=255
```
