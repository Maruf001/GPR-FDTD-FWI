# BEM Experiment 273: Half-Space Finite-Rebar Threshold Calibration Template Pack Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the threshold-calibration template pack from runs `271` and `272`.
The goal is to verify that the pack accepts the exact empty first-real-pair
template, rejects controlled damage to the threshold and metadata tables, and
does not falsely promote real BEM/FDTD agreement or downstream readiness.

This is a CPU-only validation run. It does not ingest real FDTD traces, set
numerical agreement thresholds, launch GPU/HPC work, run 3D validation, run
field FWI, or claim BEM/FDTD agreement.

## Output

```text
outputs/bem_experiments/273_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_TEMPLATE_PACK_SENSITIVITY.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_sensitivity.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_sensitivity.py
```

## Result

```text
scenarios:                         27
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        26
observed failure scenarios:        26
unexpected outcomes:               0
sensitivity ready:                 true
threshold calibration ready:       false
real BEM/FDTD comparison ready:    false
3D validation ready:               false
inversion-scale half-space ready:  false
field transfer ready:              false
GPU/HPC work ready:                false
field FWI ready:                   false
```

The exact run `271` threshold-calibration template passes. All 26 damaged
variants fail as expected for count drift, missing threshold rows, changed
metric names, prefilled threshold values, false threshold-readiness flags,
synthetic negative-control promotion, missing metadata rows, changed metadata
fields, prefilled metadata values, false metadata-readiness flags, optionalized
required metadata, and false real/downstream readiness.

## Interpretation

The first-real-pair threshold-calibration template is now guarded. It remains a
blank collection template, not evidence of numerical BEM/FDTD agreement. The
synthetic negative control is still useful as a false-promotion guard but cannot
be used to set acceptance thresholds.

Real FDTD traces, real frequency extraction, a real paired BEM/FDTD comparison,
and explicit threshold calibration remain required before any 3D validation,
inversion-scale half-space claim, field transfer, GPU/HPC escalation, or field
FWI claim.

## Decision

Use runs `271`-`273` as the guarded first-real-pair threshold-calibration
template pack. The next defensible BEM-side work is either a real-return intake
path if real FDTD traces arrive, or a bounded synthetic/contract audit that does
not promote agreement without real paired traces.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_sensitivity.py
6 passed
```

Figure validation:

```text
3581x886, dynamic range=255
```
