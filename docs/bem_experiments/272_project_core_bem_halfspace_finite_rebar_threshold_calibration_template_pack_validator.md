# BEM Experiment 272: Half-Space Finite-Rebar Threshold Calibration Template Pack Validator

Date: 2026-06-28

## Purpose

Validate the run `271` threshold-calibration template pack from a consumer
perspective.

Run `271` created blank threshold and metadata templates for the first real
matched BEM/FDTD pair. This validator checks that the rows remain blank,
required, uncalibrated, and separated from the synthetic negative control.

It does not ingest real FDTD traces, set numerical thresholds, claim BEM/FDTD
agreement, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/272_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_validator_checks.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_TEMPLATE_PACK_VALIDATOR.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_validator.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_validator.py
```

## Result

```text
validation checks:                  5
validation passes:                  5
blocking failures:                  0
validation ready:                   true
source threshold rows:              4
source metadata rows:               8
threshold calibration ready:        false
synthetic negative control usable:  false
real BEM/FDTD comparison ready:     false
field FWI ready:                    false
```

The validator checks:

| Check | Result |
| --- | --- |
| Template summary counts are consistent | pass |
| Threshold rows are blank and uncalibrated | pass |
| Metadata rows are required and blank | pass |
| Synthetic negative control not calibration source | pass |
| Real comparison and downstream states blocked | pass |

## Interpretation

The threshold-calibration template pack is internally consistent: threshold
rows and metadata rows are blank, required, uncalibrated, and separated from
the synthetic negative control.

## Decision

Use run `272` as the positive validator for the first-real-pair threshold-
calibration template pack. Sensitivity remains required before treating the
template as fully guarded.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_validator.py
5 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_validator.png
2609x835, dynamic range=255
```
