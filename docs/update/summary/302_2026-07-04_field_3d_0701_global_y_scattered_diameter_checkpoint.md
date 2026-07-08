# Field 3D 0701 Global-Y Scattered Diameter Checkpoint

Date: 2026-07-04

## What Changed

- Re-ran the fixed-radius scattered-response diameter diagnostic on the improved 0701 global y-window from checkpoint 301.
- Used the global fine y-window summary as the profile/material/depth source:
  - profiles `17-18`
  - y center `1.750 m`
  - raw length proxy `0.100 m`
  - epsr seed around `3.365`
- Ran two residual modes:
  - profile-mean residual
  - receiver-mean residual
- Made `run_field_3d_0701_scattered_radius_objective_synthesis.py` path-configurable and added near-best union/common-overlap fields.
- Refreshed the 0701 product report and product leaderboard.

## Key Numbers

- Profile-mean global-y scattered-radius scan:
  - artifact `107_field_3d_0701_fastgpr_radius_scattered_objective_scan_global_y175_profile_mean`
  - top diameter `8.0 mm`
  - near-best diameter range `8.0-12.0 mm`
  - best scattered L1 loss `0.957590`
  - status `scattered_objective_candidate_separated`
- Receiver-mean global-y scattered-radius scan:
  - artifact `108_field_3d_0701_fastgpr_radius_scattered_objective_scan_global_y175_receiver_mean`
  - top diameter `8.0 mm`
  - near-best diameter range `8.0-8.0 mm`
  - best scattered L1 loss `0.913576`
  - status `scattered_objective_candidate_separated`
- Global-y scattered-radius synthesis:
  - artifact `110_field_3d_0701_scattered_radius_objective_synthesis_global_y175`
  - decision `scattered_radius_objective_residual_modes_agree`
  - common top diameter `8.0 mm`
  - near-best union range `8.0-12.0 mm`
  - common overlap `8.0-8.0 mm`
  - min/max loss spread `0.022620975971-0.027784943581`
- Refreshed 0701 product report:
  - artifact `111_field_3d_0701_predictor_product_report`
  - x `9.819386151982 m`
  - y center `1.750 m`
  - z `1.507775545120 m`
  - raw length proxy `0.100 m`
  - supported length range `0.100-0.500 m`
  - epsr `3.364521503448`
  - fit loss `0.602550268173`
  - diagnostic scattered diameter top `8.0 mm`
  - diagnostic scattered diameter common overlap `8.0-8.0 mm`
- Refreshed leaderboard:
  - artifact `016_field_prediction_product_leaderboard`
  - current best products remain:
    - `external_2025_pipe_0701:fastgpr_3d_stack_y_length_proxy`
    - `gssi51600s:fastgpr_corrected_surface_bscan`

## What Remains Blocked

- The stronger `8 mm` result is still a scattered-response diagnostic, not the full adaptive geometry/material optimizer result.
- The full objective still has diameter ambiguity elsewhere, and adaptive optimizers can trade radius against material/time parameters.
- The 0701 y/length estimate still depends on assumed profile spacing, not measured survey geometry.

## Current Decision

The improved global y-window materially strengthens the 0701 diameter diagnostic:

- old promoted scattered diagnostic: `20 mm` top candidate from the earlier window,
- new global-y scattered diagnostic: `8 mm` common top with residual-mode overlap `8-8 mm`,
- product report now uses the new `8 mm` scattered diagnostic but still keeps diameter bounded because full adaptive optimization has not yet confirmed uniqueness.

The current product-facing 0701 estimate is therefore:

- x `9.819 m`,
- y center `1.750 m`,
- z `1.508 m`,
- length proxy `0.100 m`, supported `0.100-0.500 m`,
- epsr `3.365`,
- conductivity `0.00358 S/m`,
- diameter diagnostic top `8 mm`, with claim boundary preserved.

## Next Defensible Task

Run the adaptive scattered geometry/material optimizer on the global y-window:

- use seeds around `8, 12, 16, 20 mm`,
- keep the global y-window profiles `17-18`,
- compare whether radius gradients remain meaningful after material/time adaptation,
- promote only if the adaptive optimizer supports the `8 mm` diagnostic rather than drifting into a broad radius/material tradeoff.

## Validation And Resources

- `python -m pytest tests/test_field_3d_0701_predictor_product_report.py tests/test_field_3d_0701_y_length_global_claim_synthesis.py tests/test_field_3d_0701_scattered_radius_objective_synthesis.py tests/test_field_prediction_product_leaderboard.py -q`
  - `13 passed`
- `python -m py_compile run_field_3d_0701_predictor_product_report.py run_field_3d_0701_y_length_global_claim_synthesis.py run_field_3d_0701_scattered_radius_objective_synthesis.py run_field_3d_0701_fastgpr_radius_scattered_objective_scan.py run_field_prediction_product_leaderboard.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `107.../figures/field_3d_0701_fastgpr_radius_scattered_objective_scan.png`: size `(1821, 733)`, min/max `(0, 255)`, stddev `38.69`
  - `108.../figures/field_3d_0701_fastgpr_radius_scattered_objective_scan.png`: size `(1821, 733)`, min/max `(0, 255)`, stddev `38.95`
  - `110.../figures/field_3d_0701_scattered_radius_objective_synthesis.png`: size `(1804, 733)`, min/max `(0, 255)`, stddev `70.14`
  - `111.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `53.91`
  - `016.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `64.29`

## Artifact Paths

- Global-y profile-mean scattered scan:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/107_field_3d_0701_fastgpr_radius_scattered_objective_scan_global_y175_profile_mean`
- Global-y receiver-mean scattered scan:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/108_field_3d_0701_fastgpr_radius_scattered_objective_scan_global_y175_receiver_mean`
- Global-y scattered synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/110_field_3d_0701_scattered_radius_objective_synthesis_global_y175`
- Refreshed 0701 product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/111_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/016_field_prediction_product_leaderboard`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
