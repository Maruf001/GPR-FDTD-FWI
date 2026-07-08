# Field 3D 0701 Adjacent-Window Transfer Checkpoint

Date: 2026-07-04

## What Changed

- Added `--profile-start` and `--profile-end` overrides to the Fast-GPR scattered optimizer.
- Added profile-window metadata to scattered optimizer seed synthesis.
- Tested the current best source setting (`30 MHz`) on adjacent 0701 profile windows:
  - profiles `16-17`
  - profiles `17-18`
  - profiles `18-19`
- Refreshed the product report, leaderboard, and shipping snapshot to carry the adaptive best and near-best profile-window diagnostics.

## Key Numbers

- Transfer runs:
  - `166_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz_profiles16_17`
    - field L1 `0.659852386`
    - diameter `8.002176881 mm`
    - depth `1.476 m`
  - `167_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz_profiles16_17`
    - field L1 `0.659969091`
    - diameter `11.722712778 mm`
    - depth `1.476 m`
  - `158_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz`
    - profile window `17-18`
    - field L1 `0.742666006`
    - diameter `8.002170362 mm`
  - `159_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz`
    - profile window `17-18`
    - field L1 `0.742735386`
    - diameter `11.814474128 mm`
  - `168_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz_profiles18_19`
    - field L1 `0.699200749`
    - diameter `8.002200164 mm`
  - `169_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz_profiles18_19`
    - field L1 `0.699162245`
    - diameter `12.000000104 mm`
- Transfer synthesis:
  - artifact `170_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_freq30_profile_transfer`
  - best profile window `16-17`
  - near-best profile windows `16-17`
  - profile windows tested `16-17`, `17-18`, `18-19`
  - best field L1 `0.659852386`
  - near-best field L1 range `0.659852386-0.659969091`
  - near-best diameter range `8.002176881-11.722712778 mm`
  - best source frequency `30 MHz`
  - diameter status `optimizer_seed_diameter_near_best_narrow_range`
- Refreshed product artifacts:
  - 0701 product report `171_field_3d_0701_predictor_product_report`
  - product leaderboard `034_field_prediction_product_leaderboard`
  - shipping snapshot `035_field_prediction_shipping_snapshot`

## What Remains Blocked

- The adaptive scattered objective fits best on profile window `16-17`, while the earlier global y/length product scan promoted `17-18`.
- That is a real y-window sensitivity, not a stable single y-position claim.
- Diameter remains a near-best range `8.00-11.72 mm`.
- Full finite-length 3D FDTD inversion is still not implemented; current y/length values are still stack/profile-window proxies.

## Current Decision

The current product-facing 0701 adaptive diagnostic should report:

- best adaptive profile window `16-17`,
- best source frequency `30 MHz`,
- adaptive best point diameter `8.00 mm`,
- adaptive near-best diameter range `8.00-11.72 mm`,
- best adaptive scattered field L1 `0.659852386`.

The main product geometry row still reports the global-y product x/y/z/length values, but the claim boundary must explicitly say the adaptive scattered objective is profile-window sensitive.

## Next Defensible Task

The next product-relevant task is to reconcile y-window sensitivity:

- either run the y/length global scan under the same low-frequency scattered objective,
- or build a synthesis that compares the global-y length scan objective against the adaptive scattered objective and determines which product y estimate should be primary.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `21 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `170.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1889, 767)`, min/max `(0, 255)`, stddev `75.896`
  - `171.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `55.256`
  - `034.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `63.654`
  - `035.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `68.752`

## Artifact Paths

- Transfer synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/170_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_freq30_profile_transfer`
- Refreshed 0701 product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/171_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/034_field_prediction_product_leaderboard`
- Refreshed shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/035_field_prediction_shipping_snapshot`
- Adjacent-window transfer runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/166_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz_profiles16_17`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/167_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz_profiles16_17`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/168_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz_profiles18_19`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/169_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz_profiles18_19`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
