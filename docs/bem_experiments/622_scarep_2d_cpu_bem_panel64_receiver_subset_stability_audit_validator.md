# BEM Experiment 622: scarep 2D CPU BEM 64-Panel Receiver-Subset Stability Audit Validator

Date: 2026-06-30

## Purpose

Validate run `621` from saved artifacts.

The validator checks source readiness, the ten receiver/scan-line subset rows,
the `1e-3` subset error gate, saved NPZ array hashes, blocked project-FDTD and
3D/field/GPU claims, and figure/script artifacts.

This is an artifact validation run. It does not rerun BEM solves, compare
against project FDTD outputs, run 3D validation, launch GPU/HPC work, transfer
to field work, run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/622_scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit_validator_summary.json
figures/scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              5
passed checks:                       5
failed checks:                       0
panels:                             64
subset cases:                       10
minimum subset scan count:           3
worst subset complex relative L2:    0.0007704118971318319
worst subset time-B-scan relative L2:0.0005678637768138664
complex subsets below 1e-3:          10
time-B-scan subsets below 1e-3:      10
compared to project FDTD:            false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
validation ready:                    true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source subset audit ready | pass |
| 2 | subset rows preserve receiver-line design | pass |
| 3 | all subset errors remain below target | pass |
| 4 | arrays and claim boundary remain analytic 2D only | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

Run `621` validates as a saved analytic 2D BEM artifact. The subset table,
array hashes, figure, and claim boundary are internally consistent.

## Decision

Use this validator as the artifact guard for run `621`.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit.py
tests/test_scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit_validator.py

7 passed
```

Figure validation:

```text
2285x830, dynamic range=255
```
