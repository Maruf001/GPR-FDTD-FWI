# Field 3D 0701 Source-Frequency Sensitivity Checkpoint

Date: 2026-07-04

## What Changed

- Added a `--source-frequency-hz` control to the Fast-GPR scattered geometry/material optimizer.
- Confirmed this is a forward/source-model parameter rather than a differentiable CUDA parameter in the packaged Fast-GPR code.
- Ran source-frequency sensitivity on the real 0701 global-y receiver-mean adaptive path with AdamW, time-shift regularization weight `0.005`, and seeds `8 mm` / `12 mm` where needed.
- Synthesized the source-frequency branch and refreshed the product-facing artifacts.

## Key Numbers

- Source-frequency runs:
  - `143_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq75mhz`
    - field L1 `0.898817062`
    - diameter `11.877365410 mm`
  - `144_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq125mhz`
    - field L1 `0.985417485`
    - diameter `11.982164346 mm`
  - `145_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq150mhz`
    - field L1 `0.987597764`
    - diameter `12.000000104 mm`
  - `146_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq50mhz`
    - field L1 `0.750857472`
    - diameter `12.000000104 mm`
  - `147_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq90mhz`
    - field L1 `0.917657673`
    - diameter `11.877126992 mm`
  - `148_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq75mhz`
    - field L1 `0.909697890`
    - diameter `8.002200164 mm`
  - `149_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq50mhz`
    - field L1 `0.751709878`
    - diameter `8.002216928 mm`
- Source-frequency synthesis:
  - artifact `150_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_source_frequency_sensitivity`
  - run count `9`
  - best label `seed12_freq50`
  - best source frequency `50 MHz`
  - source frequencies tested `50, 75, 90, 100, 125, 150 MHz`
  - near-best source frequencies `50 MHz`
  - best field L1 `0.750857472`
  - near-best field L1 range `0.750857472-0.751709878`
  - near-best diameter range `8.002216928-12.000000104 mm`
  - diameter status `optimizer_seed_diameter_near_best_narrow_range`
  - gradient status `radius_gradient_available`
- Refreshed product artifacts:
  - 0701 product report `151_field_3d_0701_predictor_product_report`
  - product leaderboard `028_field_prediction_product_leaderboard`
  - shipping snapshot `029_field_prediction_shipping_snapshot`

## What Remains Blocked

- Source-frequency tuning gives a much better adaptive scattered fit, but it does not identify a unique diameter.
- Both `8 mm` and `12 mm` are near-best at the best `50 MHz` source setting.
- The field fit is now source-model sensitive, so the product must report diameter as a range and flag source-frequency sensitivity.
- Full finite-length 3D FDTD inversion is still not implemented; y/length remains a stack-profile proxy.

## Current Decision

The product-facing 0701 adaptive diagnostic should use the source-frequency sensitivity artifact:

- best source frequency `50 MHz`,
- best point diameter `12.00 mm`,
- near-best diameter range `8.00-12.00 mm`,
- best adaptive scattered field L1 `0.750857472`,
- x/y/z/length/material values unchanged from the global-y product report.

This is a real fitting improvement, but it strengthens the source-model caveat rather than removing the diameter range.

## Next Defensible Task

Continue attacking source-model and geometry coupling on real data:

- run a finer source-frequency check around `40-60 MHz` for both `8 mm` and `12 mm`,
- or test whether the `50 MHz` source setting transfers to another nearby real profile/window,
- then refresh the product only if the range remains stable and the better fit is not a one-window artifact.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `21 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `150.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1888, 767)`, min/max `(0, 255)`, stddev `76.384`
  - `151.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `55.763`
  - `028.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `63.654`
  - `029.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `68.752`

## Artifact Paths

- Source-frequency synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/150_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_source_frequency_sensitivity`
- Refreshed 0701 product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/151_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/028_field_prediction_product_leaderboard`
- Refreshed shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/029_field_prediction_shipping_snapshot`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
