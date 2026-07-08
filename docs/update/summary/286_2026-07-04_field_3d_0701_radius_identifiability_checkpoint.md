# Field 3D 0701 Radius Identifiability Checkpoint

Date: 2026-07-04

## What Changed

- Added `run_field_3d_0701_fastgpr_radius_sensitivity_scan.py`.
- Added `run_field_3d_0701_fastgpr_radius_forward_contrast.py`.
- Added focused tests for both scripts.
- Ran a real-field 0701 fixed-radius sensitivity scan on the current Fast-GPR product window.
- Ran forward-only radius contrast diagnostics at the original 5 cm bridge grid and at a 1 cm diagnostic grid.
- Refreshed the 0701 product report with explicit radius/diameter evidence.
- Refreshed the top-level product leaderboard to point at the updated 0701 product report.

## Key Numbers

- Radius sensitivity scan:
  - artifact `060_field_3d_0701_fastgpr_radius_sensitivity_scan`
  - diameters scanned `8, 12, 16, 20, 24, 30 mm`
  - profile window `1-3`
  - y center `0.200 m`
  - length proxy `0.200 m`
  - top fixed-radius candidate `8.0 mm`
  - near-best range `8.0-30.0 mm`
  - loss range `[0.707178115845, 0.707178115845]`
  - status `not_identified_flat_loss_across_scanned_diameters`
- Original bridge forward contrast:
  - artifact `061_field_3d_0701_fastgpr_radius_forward_contrast`
  - `dx_m = 0.05`
  - max relative L2 across `8-30 mm` predictions `0.0`
  - status `forward_predictions_radius_invariant_at_current_precision`
- Fine-grid bridge forward contrast:
  - artifact `063_field_3d_0701_fastgpr_radius_forward_contrast_dx01_dt002`
  - `dx_m = 0.01`
  - `fast_dt_ns = 0.02`
  - max relative L2 across `8-30 mm` predictions `0.0`
  - status `forward_predictions_radius_invariant_at_current_precision`
- Extreme stress contrast:
  - artifact `065_field_3d_0701_fastgpr_radius_forward_contrast_dx01_dt002_extreme`
  - compared `8 mm` against `1000 mm` with `anomaly_delta_epsr = 100`
  - max relative L2 `0.9998005`
  - status `forward_changes_but_field_loss_radius_flat`

## Product Update

- Refreshed product report:
  - `066_field_3d_0701_predictor_product_report`
  - x `9.819386 m`
  - y center `0.200000 m`
  - z `1.507637 m`
  - length proxy `0.200000 m`
  - diameter top candidate `8.0 mm`
  - diameter near-best/supported range `8.0-30.0 mm`
  - diameter status `not_identified_flat_loss_across_scanned_diameters`
  - radius forward status `forward_predictions_radius_invariant_at_current_precision`
  - epsr `4.803974`
  - background conductivity `0.008404 S/m`
  - fit loss `0.707159`
- Refreshed product leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/003_field_prediction_product_leaderboard`
  - top-level row for `external_2025_pipe_0701` now points at report `066`.

## What Remains Blocked

- Rebar-scale radius/diameter is not identifiable with the current 0701 Fast-GPR smooth-cylinder bridge.
- The blocker is not Adam/AdamW/Adamax; the current forward bridge is invariant for `8-30 mm` radii.
- A full finite-length 3D steel-cylinder inversion is still not implemented. The current y/length estimate is a profile-window support proxy.

## Current Decision

Do not claim a unique 0701 diameter from this Fast-GPR bridge. Report the top fixed-radius candidate and the full near-best range. The next implementation work must change the forward bridge/objective if diameter is a shipping requirement.

## Next Defensible Task

Build the next radius-sensitive bridge candidate:

- Add a scattered-field objective or anomaly-minus-background response instead of fitting mostly direct/background waveform content.
- Test whether source/receiver placement and component choice can produce measurable rebar-scale radius contrast before running another optimizer.
- If the forward contrast becomes nonzero for `8-30 mm`, rerun the fixed-radius scan and then update the product report again.

## Validation And Resources

- `python -m py_compile run_field_3d_0701_fastgpr_radius_sensitivity_scan.py`
- `python -m py_compile run_field_3d_0701_fastgpr_radius_forward_contrast.py`
- `python -m py_compile run_field_3d_0701_predictor_product_report.py`
- `python -m py_compile run_field_prediction_product_leaderboard.py`
- `python -m pytest tests/test_field_3d_0701_fastgpr_radius_sensitivity_scan.py tests/test_field_3d_0701_fastgpr_radius_forward_contrast.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_3d_0701_fastgpr_y_length_optimizer_comparison.py tests/test_field_3d_0701_fastgpr_y_length_window_optimizer_scan.py -q`
  - `21 passed`
- Touched-file `git diff --check` passed.
- Figures inspected:
  - `060.../figures/field_3d_0701_fastgpr_radius_sensitivity_scan.png`
  - `063.../figures/field_3d_0701_fastgpr_radius_forward_contrast.png`
  - `065.../figures/field_3d_0701_fastgpr_radius_forward_contrast.png`
  - `066.../figures/field_3d_0701_predictor_product_report.png`
  - `003.../figures/field_prediction_product_leaderboard.png`

## Artifact Paths

- Radius scan:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/060_field_3d_0701_fastgpr_radius_sensitivity_scan`
- Forward contrast:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/061_field_3d_0701_fastgpr_radius_forward_contrast`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/063_field_3d_0701_fastgpr_radius_forward_contrast_dx01_dt002`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/065_field_3d_0701_fastgpr_radius_forward_contrast_dx01_dt002_extreme`
- Updated product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/066_field_3d_0701_predictor_product_report`
- Updated leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/003_field_prediction_product_leaderboard`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
