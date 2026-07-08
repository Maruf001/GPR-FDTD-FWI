# Field 3D 0701 Scattered Radius Contrast Checkpoint

Date: 2026-07-04

## What Changed

- Extended `run_field_3d_0701_fastgpr_radius_forward_contrast.py` to compute:
  - homogeneous baseline prediction,
  - anomaly-minus-background scattered response,
  - scattered relative L2 versus the reference radius,
  - scatter-to-baseline norm ratio.
- Added tests for the scattered-response status path.
- Ran a 1 cm grid scattered-response contrast for the real 0701 product window.
- Ran a radius-threshold diagnostic to find when the current Fast-GPR bridge starts responding to anomaly diameter.
- Refreshed the 0701 product report and product leaderboard to cite the scattered-response diagnostic.

## Key Numbers

- Scattered rebar-scale contrast:
  - artifact `067_field_3d_0701_fastgpr_radius_forward_contrast_dx01_dt002_scattered`
  - `dx_m = 0.01`
  - `fast_dt_ns = 0.02`
  - diameters `8, 12, 16, 20, 24, 30 mm`
  - max full relative L2 vs 8 mm `0.0`
  - max scattered relative L2 vs 8 mm `0.0`
  - max scatter-to-baseline norm ratio `0.0`
  - status `forward_predictions_radius_invariant_at_current_precision`
- Radius threshold diagnostic:
  - artifact `068_field_3d_0701_fastgpr_radius_forward_contrast_dx01_dt002_radius_threshold`
  - diameters `30, 50, 100, 200, 500, 1000 mm`
  - relative L2 vs 30 mm:
    - 30 mm: `0.0`
    - 50 mm: `0.0`
    - 100 mm: `2.66e-08`
    - 200 mm: `5.63e-08`
    - 500 mm: `9.69e-03`
    - 1000 mm: `6.56e-01`
  - field loss remained flat across the threshold scan.

## Product Update

- Refreshed product report:
  - `069_field_3d_0701_predictor_product_report`
  - x `9.819386 m`
  - y center `0.200000 m`
  - z `1.507637 m`
  - length proxy `0.200000 m`
  - diameter top candidate `8.0 mm`
  - diameter supported/near-best range `8.0-30.0 mm`
  - diameter status `not_identified_flat_loss_across_scanned_diameters`
  - radius forward status `forward_predictions_radius_invariant_at_current_precision`
  - max scatter-to-baseline norm ratio `0.0`
- Refreshed top-level leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/005_field_prediction_product_leaderboard`
  - current `external_2025_pipe_0701` row points at report `069`.

## What Remains Blocked

- The current Fast-GPR bridge is not radius-sensitive at rebar scale, even after subtracting a homogeneous baseline.
- The bridge begins to change only for much larger anomalies, and the field loss remains flat even then.
- Therefore no optimizer variant can recover a reliable diameter from this bridge until the forward/objective model changes.

## Current Decision

The 0701 product can currently ship as an x/y/z/length/material proxy with explicit diameter-range reporting. It cannot ship as a unique diameter predictor under the current Fast-GPR bridge.

## Next Defensible Task

Build a new radius-sensitive bridge candidate rather than tuning the optimizer:

- test a surface-style or bistatic geometry where localized rebar-scale scatter appears in the recorded component,
- test component choice/source polarization and source/receiver depth against forward contrast before running inversion,
- only promote an optimizer after forward contrast is nonzero for `8-30 mm`.

## Validation And Resources

- `python -m py_compile run_field_3d_0701_fastgpr_radius_forward_contrast.py`
- `python -m py_compile run_field_3d_0701_predictor_product_report.py run_field_prediction_product_leaderboard.py`
- `python -m pytest tests/test_field_3d_0701_fastgpr_radius_sensitivity_scan.py tests/test_field_3d_0701_fastgpr_radius_forward_contrast.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_3d_0701_fastgpr_y_length_optimizer_comparison.py tests/test_field_3d_0701_fastgpr_y_length_window_optimizer_scan.py -q`
  - `22 passed`
- Touched-file `git diff --check` passed.
- Figures inspected:
  - `067.../figures/field_3d_0701_fastgpr_radius_forward_contrast.png`
  - `068.../figures/field_3d_0701_fastgpr_radius_forward_contrast.png`
  - `069.../figures/field_3d_0701_predictor_product_report.png`
  - `005.../figures/field_prediction_product_leaderboard.png`

## Artifact Paths

- Scattered radius contrast:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/067_field_3d_0701_fastgpr_radius_forward_contrast_dx01_dt002_scattered`
- Radius threshold diagnostic:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/068_field_3d_0701_fastgpr_radius_forward_contrast_dx01_dt002_radius_threshold`
- Updated product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/069_field_3d_0701_predictor_product_report`
- Updated product leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/005_field_prediction_product_leaderboard`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
