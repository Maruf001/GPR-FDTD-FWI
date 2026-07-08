# BEM Experiment 610: scarep 2D CPU BEM Panel Accuracy-Cost Policy Validator

Date: 2026-06-30

## Purpose

Validate the run `609` panel accuracy/cost policy from generated artifacts.

The validator checks the result boundary: 64 panels are the repeat-sweep
default, 128 panels are the high-accuracy endpoint, the current ladder does
not meet a `1e-4` target, and no project-FDTD, 3D, GPU/HPC, or field-FWI claim
is promoted.

This is a CPU-only artifact validation. It does not rerun the BEM solve,
compare against project FDTD outputs, run 3D validation, launch GPU/HPC work,
run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/610_scarep_2d_cpu_bem_panel_accuracy_cost_policy_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel_accuracy_cost_policy_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel_accuracy_cost_policy_validator_summary.json
figures/scarep_2d_cpu_bem_panel_accuracy_cost_policy_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              5
passed checks:                       5
failed checks:                       0
thresholds tested:                   6
thresholds met:                      5
thresholds unmet:                    1
repeat-sweep default panels:         64
high-accuracy panels:                128
strict 1e-4 threshold met:           false
complex error order:                 1.9961624062950216
time-B-scan error order:             1.9918880456546393
wall-time cost exponent:             1.6952684551080672
compared to scarep analytic ref:     true
compared to project FDTD outputs:    false
real 3D validation ready:            false
GPU/HPC ready:                       false
field FWI ready:                     false
validation ready:                    true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source panel policy ready | pass |
| 2 | threshold ladder matches 8-128 sweep | pass |
| 3 | 64 default and 128 high-accuracy endpoint preserved | pass |
| 4 | convergence and claim boundary preserved | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

The run `609` policy is a valid 2D BEM numerical policy against the scarep
analytic dielectric-cylinder reference. It is not yet a matched comparison to
the project FDTD experiment stream, and it is not a 3D, GPU/HPC, or field-FWI
launch condition.

## Decision

Use this validator as the artifact guard for run `609`. Use 64 panels for
repeated scarep 2D CPU BEM sweeps unless a tighter validation endpoint is
needed; use 128 panels for high-accuracy checks.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel_accuracy_cost_policy_validator.py
tests/test_scarep_2d_cpu_bem_panel_accuracy_cost_policy_validation_sensitivity.py

6 passed
```

Figure validation:

```text
2285x839, dynamic range=255
```
