# Field 3D 0701 Common-Objective Y/Length Support Checkpoint

Date: 2026-07-04

## What Changed

- Extended the adaptive scattered objective from profile-window y localization into y-length support testing.
- Tested length-3 and length-4 windows under the same 30 MHz receiver-mean AdamW scattered objective used by the adaptive y bracket.
- Added explicit y/length fields to scattered optimizer seed synthesis:
  - best profile length,
  - y center,
  - center-span length,
  - window-span length,
  - near-best y/length ranges.
- Refreshed the product report, product leaderboard, and shipping snapshot to expose the adaptive common-objective y/length estimate.

## Key Numbers

- Length-3 checks:
  - `186...profiles13_15_len3` seed08:
    - field L1 `0.580339`
    - diameter `8.002 mm`
  - `187...profiles13_15_len3` seed12:
    - field L1 `0.580364`
    - diameter `11.955 mm`
  - `188...profiles14_16_len3` seed08:
    - field L1 `0.537834`
    - diameter `8.002 mm`
    - depth `1.488 m`
    - epsr `3.297`
    - background sigma `0.003776 S/m`
  - `189...profiles14_16_len3` seed12:
    - field L1 `0.537872`
    - diameter `11.897 mm`
  - `190...profiles15_17_len3` seed08:
    - field L1 `0.650415`
    - diameter `8.002 mm`
  - `191...profiles15_17_len3` seed12:
    - field L1 `0.650437`
    - diameter `11.823 mm`
- Length-4 checks:
  - `192...profiles13_16_len4` seed08:
    - field L1 `0.558899`
    - diameter `8.002 mm`
  - `193...profiles13_16_len4` seed12:
    - field L1 `0.559073`
    - diameter `11.909 mm`
  - `194...profiles14_17_len4` seed08:
    - field L1 `0.584490`
    - diameter `8.002 mm`
  - `195...profiles14_17_len4` seed12:
    - field L1 `0.584610`
    - diameter `11.911 mm`
- Combined y/length synthesis:
  - artifact `197_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_freq30_y_length_support`
  - best label `p14_16_seed08`
  - best profile window `14-16`
  - best profile length `3`
  - adaptive y center `1.50 m`
  - adaptive y window `[1.4, 1.6] m`
  - adaptive center-span length `0.20 m`
  - adaptive window-span length `0.30 m`
  - best field L1 `0.537833989`
  - near-best profile windows `14-16`
  - near-best diameter range `8.002208546-11.896786280 mm`
  - near-best length center-span range `0.20-0.20 m`
- Product report `198`:
  - primary legacy/global y row still reports y center `1.75 m`
  - adaptive scattered y/length reports y center `1.50 m`, length center-span `0.20 m`
  - y conflict against primary row is now `0.25 m`
  - adaptive depth `1.488030195 m`
  - adaptive epsr `3.296650887`
  - adaptive background sigma `0.003776330 S/m`
- Refreshed product artifacts:
  - leaderboard `038_field_prediction_product_leaderboard`
  - shipping snapshot `039_field_prediction_shipping_snapshot`

## What Remains Blocked

- There is still a product-level y conflict:
  - older global y/length objective: y center `1.75 m`
  - current adaptive scattered objective: y center `1.50 m`
- The adaptive objective now supports a length proxy, but this is still a profile-window proxy, not a full finite-length 3D steel-cylinder FDTD inversion.
- Diameter is narrowed to `8.00-11.90 mm`, but still not a unique single value.

## Current Decision

The current best common-objective adaptive prediction for the 0701 stack is:

- x remains inherited from the current local bridge product: `9.819 m`
- y center `1.50 m`
- y window `[1.4, 1.6] m`
- length center-span `0.20 m`
- length window-span `0.30 m`
- z depth `1.488 m`
- epsr `3.297`
- background sigma `0.003776 S/m`
- diameter range `8.00-11.90 mm`
- field L1 `0.537834`

This is stronger than the previous adaptive y-only bracket because the length-3 window `14-16` beat both adjacent length-3 windows and the tested length-4 windows under the same objective.

## Next Defensible Task

The next product-relevant branch is to decide whether the adaptive scattered estimate should supersede the older primary y/length row.

Useful bounded options:

- build a reconciler artifact that compares the older global-y objective and the adaptive scattered objective and defines the product promotion rule;
- or refresh the product report to promote the adaptive scattered y/length estimate as the operational row while retaining the old global-y estimate as a legacy diagnostic.

After that, test a small optimizer-family sensitivity around the promoted `14-16` window, including AdamW, Adamax, and Adam, to see whether the y/length and diameter range survive optimizer choice.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `21 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `197.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1889, 767)`, min/max `(0, 255)`, stddev `73.014`
  - `198.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `53.340`
  - `038.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `64.293`
  - `039.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `64.482`

## Artifact Paths

- Combined adaptive y/length synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/197_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_freq30_y_length_support`
- Refreshed product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/198_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/038_field_prediction_product_leaderboard`
- Refreshed shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/039_field_prediction_shipping_snapshot`
- New length-support runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/186_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz_profiles13_15_len3`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/187_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz_profiles13_15_len3`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/188_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz_profiles14_16_len3`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/189_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz_profiles14_16_len3`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/190_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz_profiles15_17_len3`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/191_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz_profiles15_17_len3`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/192_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz_profiles13_16_len4`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/193_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz_profiles13_16_len4`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/194_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz_profiles14_17_len4`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/195_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz_profiles14_17_len4`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
