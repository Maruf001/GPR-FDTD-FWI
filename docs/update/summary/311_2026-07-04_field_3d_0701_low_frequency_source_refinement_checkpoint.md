# Field 3D 0701 Low-Frequency Source Refinement Checkpoint

Date: 2026-07-04

## What Changed

- Extended the source-frequency sweep below the checkpoint `310` best `40 MHz` setting.
- Ran `30 MHz`, `35 MHz`, and `45 MHz` for both `8 mm` and `12 mm` seeds on the same real 0701 global-y receiver-mean adaptive path.
- Synthesized all source-frequency runs from `30-150 MHz`.
- Refreshed the 0701 product report, product leaderboard, and shipping snapshot.

## Key Numbers

- New low-frequency runs:
  - `158_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz`
    - field L1 `0.742666006`
    - diameter `8.002170362 mm`
  - `159_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz`
    - field L1 `0.742735386`
    - diameter `11.813549325 mm`
  - `160_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq35mhz`
    - field L1 `0.742713749`
    - diameter `8.002203889 mm`
  - `161_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq35mhz`
    - field L1 `0.742693901`
    - diameter `11.735735238 mm`
  - `162_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq45mhz`
    - field L1 `0.743810892`
    - diameter `8.002203889 mm`
  - `163_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq45mhz`
    - field L1 `0.744525731`
    - diameter `11.818168685 mm`
- Low-frequency synthesis:
  - artifact `164_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_source_frequency_low_fine_sensitivity`
  - run count `19`
  - best label `seed08_freq30`
  - best source frequency `30 MHz`
  - tested source frequencies `30, 35, 40, 45, 50, 60, 75, 90, 100, 125, 150 MHz`
  - near-best source frequencies `30, 35, 40, 45 MHz`
  - best field L1 `0.742666006`
  - near-best field L1 range `0.742666006-0.744525731`
  - near-best diameter range `8.002170362-11.818168685 mm`
  - diameter status `optimizer_seed_diameter_near_best_narrow_range`
  - gradient status `radius_gradient_available`
- Refreshed product artifacts:
  - 0701 product report `165_field_3d_0701_predictor_product_report`
  - product leaderboard `032_field_prediction_product_leaderboard`
  - shipping snapshot `033_field_prediction_shipping_snapshot`

## What Remains Blocked

- The low-frequency source model improves the fit, but the near-best diameter remains a range.
- `30-45 MHz` are all near-best source settings, so source frequency itself is not uniquely identified either.
- This strengthens the source-model caveat: diameter, source frequency, and timing remain coupled.
- Full finite-length 3D FDTD geometry remains future work; the current y/length claim is still a stack-profile proxy.

## Current Decision

The current 0701 product should report:

- best source frequency `30 MHz`,
- near-best source-frequency band `30-45 MHz`,
- adaptive best point diameter `8.00 mm`,
- adaptive near-best diameter range `8.00-11.82 mm`,
- best adaptive scattered field L1 `0.742666006`.

This is the strongest real-field fit so far, but it does not justify a unique diameter claim.

## Next Defensible Task

The next product-relevant task is transfer/stability:

- test whether the `30-45 MHz` source-frequency band and `8-11.8 mm` diameter range transfer to an adjacent 0701 profile/window,
- or run a lower-bound check below `30 MHz` only if the source-frequency optimum must be localized before transfer.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `21 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `164.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1889, 767)`, min/max `(0, 255)`, stddev `77.299`
  - `165.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `55.256`
  - `032.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `63.654`
  - `033.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `68.752`

## Artifact Paths

- Low-frequency synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/164_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_source_frequency_low_fine_sensitivity`
- Refreshed 0701 product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/165_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/032_field_prediction_product_leaderboard`
- Refreshed shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/033_field_prediction_shipping_snapshot`
- Low-frequency runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/158_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/159_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/160_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq35mhz`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/161_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq35mhz`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/162_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq45mhz`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/163_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq45mhz`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
