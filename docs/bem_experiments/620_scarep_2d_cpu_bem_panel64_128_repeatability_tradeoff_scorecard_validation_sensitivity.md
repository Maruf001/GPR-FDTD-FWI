# BEM Experiment 620: scarep 2D CPU BEM 64-vs-128 Panel Repeatability Tradeoff Scorecard Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `619` 64-vs-128 panel tradeoff scorecard validator.

The sensitivity run mutates the scorecard artifacts in memory and checks
whether the validator rejects damaged states. The damage cases cover score-row
shape, policy roles, target thresholds, error-reduction ratios, wall-time
ratio, 64-panel policy confirmation, 128-panel policy confirmation,
project-FDTD promotion, 3D promotion, GPU/HPC promotion, field-FWI promotion,
figure damage, and missing script snapshots.

This is a CPU-only artifact sensitivity run. It does not rerun BEM solves,
compare against project FDTD outputs, run 3D validation, launch GPU/HPC work,
run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/620_scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard_validation_sensitivity_summary.json
figures/scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
cases:                         16
expected pass cases:            1
expected fail cases:           15
actual pass cases:              1
actual fail cases:             15
unexpected outcomes:            0
exact source passes:          true
damaged cases rejected:        true
compared to project FDTD:      false
real 3D validation ready:      false
GPU/HPC ready:                 false
field FWI ready:               false
sensitivity ready:             true
```

## Interpretation

The validator is sensitive to the failure modes that would undermine the
64-vs-128 panel policy. It accepts only the exact scorecard and rejects damaged
policy roles, tradeoff ratios, claim-boundary promotion, damaged figures, and
missing script snapshots.

## Decision

Keep run `618` as the guarded panel-count tradeoff scorecard.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard.py
tests/test_scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard_validator.py
tests/test_scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard_validation_sensitivity.py

9 passed
```

Figure validation:

```text
2284x855, dynamic range=255
```
