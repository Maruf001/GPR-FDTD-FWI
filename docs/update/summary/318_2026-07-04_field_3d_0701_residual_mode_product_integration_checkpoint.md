# Field 3D 0701 Residual-Mode Product Integration Checkpoint

Date: 2026-07-04

## What Changed

- Wired residual-mode sensitivity into the product report, product leaderboard, and shipping snapshot.
- Added product fields:
  - `residual_mode_sensitivity_status`,
  - `residual_mode_sensitivity_best_label`,
  - `residual_mode_sensitivity_near_best_labels`,
  - `residual_mode_sensitivity_field_l1_loss_range`.
- Updated shipping wording so residual-mode is no longer listed as an untested blocker:
  - receiver-mean controls the current product fit,
  - profile/global residual modes are worse,
  - y/length remains stable.

## Key Numbers

- Residual-mode synthesis artifact:
  - `211_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_adamax_freq30_y_length_residual_mode_sensitivity`
- Product report:
  - `212_field_3d_0701_predictor_product_report`
  - operational source `adaptive_scattered_common_objective`
  - y center `1.50 m`
  - length center-span `0.20 m`
  - diameter range `8.002208546-11.896786280 mm`
  - fit loss `0.537833989`
  - residual-mode status `receiver_mean_controls_loss_y_length_stable`
- Product index:
  - leaderboard `043_field_prediction_product_leaderboard`
  - shipping snapshot `045_field_prediction_shipping_snapshot`
- Residual-mode field-L1 range:
  - `0.537808120-0.669110835`
- Near-best residual-mode labels:
  - `receiver_mean_seed08`
  - `receiver_mean_seed12`

## What Remains Blocked

- Diameter remains a narrow range, not a unique value.
- Source-frequency and timing-prior sensitivity still need the same product-level stress around the promoted `14-16` row.
- The length is still a profile-window proxy, not a full finite-length 3D FDTD inversion.

## Current Decision

The current product method definition should explicitly include:

- adaptive scattered common objective,
- receiver-mean residualization,
- `30 MHz` source,
- timing prior weight `0.005`,
- profile window `14-16`.

Residual-mode stress does not invalidate the y/length prediction, but it does show that receiver-mean is the only near-best residual mode.

## Next Defensible Task

Run source-frequency and timing-prior sensitivity around the promoted row:

- profile window `14-16`,
- receiver-mean residualization,
- Adamax or AdamW,
- diameter seeds `8` and `12`,
- compare a small source-frequency ladder around `30 MHz`.

If source-frequency sensitivity is stable, update the product status language to distinguish remaining diameter range from y/length/material stability.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `21 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `211.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1888, 767)`, min/max `(0, 255)`, stddev `69.945`
  - `212.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `56.611`
  - `043.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `63.984`
  - `045.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `64.482`

## Artifact Paths

- Product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/212_field_3d_0701_predictor_product_report`
- Product leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/043_field_prediction_product_leaderboard`
- Shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/045_field_prediction_shipping_snapshot`
- Residual-mode synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/211_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_adamax_freq30_y_length_residual_mode_sensitivity`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
