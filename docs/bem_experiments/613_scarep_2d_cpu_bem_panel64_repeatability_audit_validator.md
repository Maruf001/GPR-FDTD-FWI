# BEM Experiment 613: scarep 2D CPU BEM 64-Panel Repeatability Audit Validator

Date: 2026-06-30

## Purpose

Validate the run `612` 64-panel repeatability audit from generated artifacts.

The validator checks the three-repeat shape, 64-panel setting, identical
response hashes, identical time-B-scan hashes, sub-`1e-3` errors, and the
analytic-only claim boundary.

This is a CPU-only artifact validation. It does not rerun the BEM solve,
compare against project FDTD outputs, run 3D validation, launch GPU/HPC work,
run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/613_scarep_2d_cpu_bem_panel64_repeatability_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_repeatability_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel64_repeatability_audit_validator_summary.json
figures/scarep_2d_cpu_bem_panel64_repeatability_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              5
passed checks:                       5
failed checks:                       0
panels:                              64
repeats:                              3
complex relative L2 mean:             0.0007053747139208214
time-B-scan relative L2 mean:         0.0005202399688500149
wall seconds mean:                   20.594270388983812
response hash unique count:           1
time-B-scan hash unique count:        1
compared to analytic reference:       true
compared to project FDTD outputs:     false
real 3D validation ready:             false
GPU/HPC ready:                        false
field FWI ready:                      false
validation ready:                     true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source repeatability audit ready | pass |
| 2 | repeat rows preserve 64-panel problem shape | pass |
| 3 | errors and hashes are repeatable | pass |
| 4 | claim boundary remains analytic 2D only | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

Run `612` validates as a stable 64-panel CPU BEM repeatability result. The
result supports the repeat-sweep default, but it remains scoped to the scarep
analytic-cylinder validation problem.

## Decision

Use this validator as the artifact guard for run `612`.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_repeatability_audit.py
tests/test_scarep_2d_cpu_bem_panel64_repeatability_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel64_repeatability_audit_validation_sensitivity.py

9 passed
```

Figure validation:

```text
2285x840, dynamic range=255
```
