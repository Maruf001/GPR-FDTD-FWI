# BEM Experiment 352: Real-Pair Trace Export Packet Contract Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `351` validator with controlled damaged variants.

The exact run `350` packet contract should pass. Damaged variants should fail
when they change packet counts, remove trace rows, change receiver keys, alter
metadata items, change acceptance-check counts, drift expected frequency or
residual row counts, falsely promote execution, damage figure validation, or
remove script snapshots.

This run does not stage real FDTD traces, execute a real BEM/FDTD comparison,
calibrate thresholds, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/352_project_core_bem_real_pair_trace_export_packet_contract_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_real_pair_trace_export_packet_contract_validation_sensitivity_scenarios.csv
data/project_core_bem_real_pair_trace_export_packet_contract_validation_sensitivity_summary.json
figures/project_core_bem_real_pair_trace_export_packet_contract_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                    13
expected pass:                1
observed pass:                1
expected failures:            12
observed failures:            12
unexpected outcomes:          0
sensitivity ready:            true
accepts exact run 350:        true
rejects damaged variants:     true
real pair execution ready:    false
GPU work ready:               false
field FWI ready:              false
figure size:                  3293x891
figure dynamic range:         255
```

## Interpretation

The validator accepts the exact run `350` packet contract and rejects all
controlled corruptions. This guards the packet contract without promoting the
real comparison itself.

## Decision

Use runs `350-352` as the guarded real-pair export packet contract. Keep real
BEM/FDTD execution, threshold calibration, broad replacement, 3D validation,
GPU/HPC work, field transfer, and field FWI blocked until an actual packet is
staged and validated.
