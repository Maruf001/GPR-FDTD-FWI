# BEM Experiment 289: Threshold-Calibration Return Readiness Pack Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `288` validator for the BEM first-real-pair
threshold-calibration return-readiness pack.

This run checks whether the validator accepts the exact saved run `287` pack
and rejects controlled damage to threshold rows, metadata rows, support rows,
blocker rows, summary counts, guard flags, and downstream readiness states.

This run does not execute future real-pair commands, inspect real FDTD traces,
compare real BEM/FDTD outputs, set thresholds, run 3D validation, run inversion
scale studies, transfer to field evidence, use GPU/HPC, or run field FWI.

## Output

```text
outputs/bem_experiments/289_project_core_bem_halfspace_finite_rebar_threshold_calibration_return_readiness_pack_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_return_readiness_pack_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_return_readiness_pack_sensitivity_summary.json
data/figure_validation.csv
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_return_readiness_pack_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_RETURN_READINESS_PACK_SENSITIVITY.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_return_readiness_pack_sensitivity.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_return_readiness_pack_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         42
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        41
observed failure scenarios:        41
unexpected outcomes:               0
sensitivity ready:                 true
pack validation ready:             true
return readiness pack ready:       true
threshold metrics:                 4
required metadata fields:          8
real BEM/FDTD comparison ready:    false
threshold calibration ready:       false
3D validation ready:               false
inversion-scale ready:             false
field transfer ready:              false
GPU work ready:                    false
field FWI ready:                   false
```

## Interpretation

The return-readiness pack validator accepts the exact run `287` pack and
rejects 41 damaged variants. The rejected cases cover threshold-row drift,
metadata-row drift, support/blocker drift, summary-count drift, guard-readiness
drift, premature calibrated-threshold or metadata readiness, real-trace
promotion, real-comparison promotion, threshold promotion, 3D/inversion
promotion, field-transfer promotion, GPU promotion, and field-FWI promotion.

## Decision

Use runs `287-289` as the guarded BEM first-real-pair return-readiness pack.
Real traces, a real BEM/FDTD comparison, and accepted thresholds remain
required before downstream work.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_return_readiness_pack_sensitivity.py
5 passed
```

Figure validation:

```text
4445x904, dynamic range=255
```
