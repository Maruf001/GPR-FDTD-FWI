# Field 3D 0701 Fine Source-Frequency Checkpoint

Date: 2026-07-04

## What Changed

- Extended source-frequency sensitivity around the checkpoint `309` best source setting.
- Ran both `8 mm` and `12 mm` seeds at `40 MHz` and `60 MHz`, with the same receiver-mean AdamW adaptive setup and time-shift regularization weight `0.005`.
- Synthesized the expanded frequency set and refreshed the product-facing artifacts.

## Key Numbers

- Fine frequency runs:
  - `152_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq40mhz`
    - field L1 `0.742824912`
    - diameter `8.002203889 mm`
    - epsr `3.330204964`
  - `153_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq40mhz`
    - field L1 `0.743090868`
    - diameter `11.726145633 mm`
    - epsr `3.357307911`
  - `154_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq60mhz`
    - field L1 `0.801801383`
    - diameter `8.002217859 mm`
  - `155_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq60mhz`
    - field L1 `0.806615949`
    - diameter `11.769626290 mm`
- Fine source-frequency synthesis:
  - artifact `156_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_source_frequency_fine_sensitivity`
  - run count `13`
  - best label `seed08_freq40`
  - best source frequency `40 MHz`
  - tested source frequencies `40, 50, 60, 75, 90, 100, 125, 150 MHz`
  - near-best source frequencies `40 MHz`
  - best field L1 `0.742824912`
  - near-best field L1 range `0.742824912-0.743090868`
  - near-best diameter range `8.002203889-11.726145633 mm`
  - diameter status `optimizer_seed_diameter_near_best_narrow_range`
  - gradient status `radius_gradient_available`
- Refreshed product artifacts:
  - 0701 product report `157_field_3d_0701_predictor_product_report`
  - product leaderboard `030_field_prediction_product_leaderboard`
  - shipping snapshot `031_field_prediction_shipping_snapshot`

## What Remains Blocked

- The source-frequency fit is much better at `40 MHz`, but the near-best diameter still spans `8.00-11.73 mm`.
- This confirms source frequency is a major model parameter and should be fitted or calibrated, not assumed.
- Diameter is still not unique, and the product must keep the range.
- Full finite-length 3D FDTD inversion is still not implemented in this path.

## Current Decision

The current 0701 product-facing adaptive diagnostic should now report:

- best source frequency `40 MHz`,
- best point diameter `8.00 mm`,
- adaptive near-best diameter range `8.00-11.73 mm`,
- best adaptive scattered field L1 `0.742824912`,
- x/y/z/length/material values unchanged from the global-y product report.

This is the strongest real-field fit so far, but it increases the importance of the source-model caveat.

## Next Defensible Task

Continue real-data product improvement:

- test whether `40 MHz` transfers to an adjacent profile/window in the 0701 stack,
- or run a narrower `30-45 MHz` check for both seeds to see whether 40 MHz is a boundary optimum,
- then refresh only if the better source setting is stable.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `21 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `156.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1889, 767)`, min/max `(0, 255)`, stddev `76.610`
  - `157.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `55.256`
  - `030.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `63.654`
  - `031.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `68.752`

## Artifact Paths

- Fine source-frequency synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/156_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_source_frequency_fine_sensitivity`
- Refreshed 0701 product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/157_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/030_field_prediction_product_leaderboard`
- Refreshed shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/031_field_prediction_shipping_snapshot`
- Fine source-frequency runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/152_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq40mhz`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/153_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq40mhz`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/154_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq60mhz`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/155_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq60mhz`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
