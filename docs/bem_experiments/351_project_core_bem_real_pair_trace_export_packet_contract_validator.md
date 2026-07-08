# BEM Experiment 351: Real-Pair Trace Export Packet Contract Validator

Date: 2026-06-29

## Purpose

Validate the saved run `350` FDTD export packet contract from artifacts.

This run checks packet counts, trace-role coverage, receiver keys, metadata and
control items, expected frequency/residual row counts, blocked execution
states, figure validation, and script snapshots.

This run does not stage real FDTD traces, execute a real BEM/FDTD comparison,
calibrate thresholds, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/351_project_core_bem_real_pair_trace_export_packet_contract_validator
```

Key artifacts:

```text
data/project_core_bem_real_pair_trace_export_packet_contract_validator_checks.csv
data/project_core_bem_real_pair_trace_export_packet_contract_validator_summary.json
figures/project_core_bem_real_pair_trace_export_packet_contract_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                 7
passed checks:                     7
failed checks:                     0
validation ready:                  true
packet items:                      34
projected trace files:             26
metadata/control items:            8
acceptance checks:                 217
expected FDTD frequency-bin rows:  234
expected paired residual rows:     117
real pair execution ready:         false
GPU work ready:                    false
field FWI ready:                   false
figure size:                       3329x893
figure dynamic range:              255
```

## Interpretation

The run `350` packet contract validates from saved artifacts. The required
trace files, metadata items, acceptance checks, frequency-bin row count, and
residual row count are stable.

## Decision

Use run `351` as the validator for the real-pair export packet contract.
Sensitivity hardening remains required before treating the packet contract as
guarded.
