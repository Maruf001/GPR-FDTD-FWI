# BEM Experiment 619: scarep 2D CPU BEM 64-vs-128 Panel Repeatability Tradeoff Scorecard Validator

Date: 2026-06-30

## Purpose

Validate the run `618` 64-vs-128 panel repeatability tradeoff scorecard from
generated artifacts.

The validator checks that the scorecard preserves the 64-panel repeat-sweep
default role, the 128-panel high-accuracy endpoint role, the error/runtime
tradeoff ratios, the analytic-only claim boundary, and the figure/script
artifacts.

This is a CPU-only artifact validation. It does not rerun BEM solves, compare
against project FDTD outputs, run 3D validation, launch GPU/HPC work, run field
FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/619_scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard_validator_summary.json
figures/scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              5
passed checks:                       5
failed checks:                       0
repeat default panels:              64
high-accuracy panels:              128
complex error reduction 64 to 128:   3.9348175940455667
time-B-scan error reduction:         3.9404703126958314
wall-time ratio 128 to 64:           3.8640530930812176
compared to project FDTD outputs:    false
real 3D validation ready:            false
GPU/HPC ready:                       false
field FWI ready:                     false
validation ready:                    true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source scorecard ready | pass |
| 2 | score rows preserve 64 and 128 policy roles | pass |
| 3 | tradeoff ratios support policy | pass |
| 4 | claim boundary remains analytic 2D only | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

The 64-vs-128 scorecard validates as the guarded panel-policy artifact. It
supports the current rule: 64 panels for repeated sweeps and 128 panels for
high-accuracy endpoint confirmation.

## Decision

Use this validator as the artifact guard for run `618`.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard.py
tests/test_scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard_validator.py

6 passed
```

Figure validation:

```text
2285x830, dynamic range=255
```
