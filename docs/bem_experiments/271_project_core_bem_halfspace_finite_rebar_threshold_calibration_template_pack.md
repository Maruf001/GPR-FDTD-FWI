# BEM Experiment 271: Half-Space Finite-Rebar Threshold Calibration Template Pack

Date: 2026-06-28

## Purpose

Create empty threshold and metadata templates for the first real matched
BEM/FDTD pair.

Runs `268-270` define and guard the threshold-calibration protocol. This run
turns that protocol into concrete blank CSV templates for future real paired
data.

It does not ingest real FDTD traces, set numerical thresholds, claim BEM/FDTD
agreement, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/271_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_rows.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_metadata_template_rows.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_TEMPLATE_PACK.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack.py
```

## Result

```text
threshold template rows:             4
metadata template rows:              8
required metadata fields:            8
calibrated thresholds:               0
metadata ready rows:                 0
template pack ready:                 true
threshold calibration ready:         false
synthetic negative control usable:   false
real trace files present:            false
real FDTD extraction ready:          false
real BEM/FDTD comparison ready:      false
field FWI ready:                     false
```

Threshold template metrics:

| Metric | Units |
| --- | --- |
| normalized_l2_error | dimensionless |
| max_relative_error | dimensionless |
| scan_peak_location_error | meters_and_receiver_steps |
| phase_reference_residual | radians |

## Interpretation

The first-real-pair threshold calibration now has a fixed empty template: four
threshold metrics and eight required metadata fields. No thresholds are set and
the synthetic negative control remains unusable for calibration.

## Decision

Use run `271` as the empty template pack for future first-real-pair threshold
calibration. Real paired data remain required.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack.py
4 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_pack.png
2645x842, dynamic range=255
```
