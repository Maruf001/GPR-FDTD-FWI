# BEM Experiment 276: Half-Space Finite-Rebar Threshold Calibration Template Fill Synthetic Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `275` synthetic template-fill validator. The goal is to
verify that the validator accepts the exact run `274` synthetic fill smoke and
rejects controlled damage to threshold rows, metadata rows, saved check rows,
summary counts, and false real/downstream readiness.

This run does not ingest real FDTD traces, set real thresholds, claim BEM/FDTD
agreement, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/276_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_TEMPLATE_FILL_SYNTHETIC_SENSITIVITY.md
```

## Result

```text
scenarios:                         25
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        24
observed failure scenarios:        24
unexpected outcomes:               0
sensitivity ready:                 true
synthetic fill smoke ready:        true
threshold calibration ready:       false
real BEM/FDTD comparison ready:    false
3D validation ready:               false
inversion-scale ready:             false
field transfer ready:              false
GPU work ready:                    false
field FWI ready:                   false
```

The exact run `274` synthetic fill smoke passes. All 24 damaged variants fail
as expected for missing threshold rows, blank or negative threshold values,
pair-ID drift, synthetic negative-control promotion, real-threshold promotion,
blank metadata values, hash drift, frequency-grid parsing failure, metadata
readiness drift, real-metadata promotion, saved-check drift, summary-count
drift, and false real/downstream readiness.

## Interpretation

The positive-control threshold-fill smoke is now guarded. It is useful for
testing future real threshold-intake mechanics, but it remains synthetic and
does not set real acceptance thresholds.

Real paired BEM/FDTD data remain required before threshold calibration,
BEM/FDTD agreement, 3D validation, inversion-scale use, field transfer, GPU/HPC
work, or field FWI can be claimed.

## Decision

Use runs `274`-`276` as the guarded positive-control threshold-fill smoke.
Real paired BEM/FDTD data remain required before calibration.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_sensitivity.py
6 passed
```

Figure validation:

```text
3797x890, dynamic range=255
```
