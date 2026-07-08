# BEM Experiment 616: scarep 2D CPU BEM 128-Panel Repeatability Audit Validator

Date: 2026-06-30

## Purpose

Validate the run `615` 128-panel repeatability audit from generated artifacts.

The validator checks that the three repeat rows preserve the 128-panel problem
shape, the frequency-response and reconstructed time-B-scan hashes are
identical, the errors stay below the `2e-4` high-accuracy target, the claim
boundary remains analytic 2D only, and the figure/script artifacts exist.

This is a CPU-only artifact validation. It does not run a new BEM solve,
compare against project FDTD outputs, run 3D validation, launch GPU/HPC work,
run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/616_scarep_2d_cpu_bem_panel128_repeatability_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel128_repeatability_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel128_repeatability_audit_validator_summary.json
figures/scarep_2d_cpu_bem_panel128_repeatability_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              5
passed checks:                       5
failed checks:                       0
panels:                            128
repeats:                             3
complex relative L2 mean:            0.00017926490798156496
time-B-scan relative L2 mean:        0.00013202484159666165
wall seconds mean:                  79.57735419630383
response hash unique count:          1
time-B-scan hash unique count:       1
compared to project FDTD outputs:    false
real 3D validation ready:            false
GPU/HPC ready:                       false
field FWI ready:                     false
validation ready:                    true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source repeatability audit ready | pass |
| 2 | repeat rows preserve 128-panel problem shape | pass |
| 3 | errors and hashes are high-accuracy repeatable | pass |
| 4 | claim boundary remains analytic 2D only | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

The 128-panel repeatability audit validates from artifacts. It can now be used
as a guarded high-accuracy endpoint without rerunning the expensive CPU solves
each time a downstream policy or comparison-preparation step needs the result.

## Decision

Use this validator as the artifact guard for run `615`. Keep project-FDTD
comparison, 3D validation, GPU/HPC, and field-FWI claims blocked until matched
comparisons are produced.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel128_repeatability_audit.py
tests/test_scarep_2d_cpu_bem_panel128_repeatability_audit_validator.py

6 passed
```

Figure validation:

```text
2285x834, dynamic range=255
```
