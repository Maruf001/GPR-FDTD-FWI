# Field 3D 0701 Adaptive Y-Bracket Product Refresh Checkpoint

Date: 2026-07-04

## What Changed

- Extended the 0701 low-frequency adaptive scattered profile-window scan from `16-19` to a bracketed `13-20` sweep.
- Added predictor metadata to scattered optimizer seed synthesis:
  - best adaptive depth,
  - best background permittivity,
  - best background/anomaly conductivity,
  - best timing shift.
- Refreshed the 0701 product report so it exposes the adaptive scattered y estimate as a first-class product field instead of hiding it inside diagnostics.
- Refreshed the product leaderboard and shipping snapshot so the current blocker says exactly where the primary y estimate and adaptive scattered y estimate conflict.

## Key Numbers

- New adaptive scattered profile-window runs:
  - `174...profiles15_16` seed08:
    - field L1 `0.583741`
    - diameter `8.002 mm`
    - depth `1.481 m`
  - `175...profiles15_16` seed12:
    - field L1 `0.583907`
    - diameter `11.789 mm`
    - depth `1.480 m`
  - `176...profiles19_20` seed08:
    - field L1 `0.687840`
    - diameter `8.002 mm`
  - `177...profiles19_20` seed12:
    - field L1 `0.687720`
    - diameter `11.904 mm`
  - `178...profiles14_15` seed08:
    - field L1 `0.569337`
    - diameter `8.002 mm`
    - depth `1.488 m`
    - epsr `3.297`
    - background sigma `0.003753 S/m`
  - `179...profiles14_15` seed12:
    - field L1 `0.569402`
    - diameter `12.178 mm`
  - `180...profiles13_14` seed08:
    - field L1 `0.614326`
    - diameter `8.002 mm`
  - `181...profiles13_14` seed12:
    - field L1 `0.614320`
    - diameter `12.054 mm`
- Extended synthesis:
  - artifact `183_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_freq30_profile_transfer_extended_y_bracket`
  - best label `p14_15_seed08`
  - best profile window `14-15`
  - near-best profile windows `14-15`
  - tested profile windows `13-14`, `14-15`, `15-16`, `16-17`, `17-18`, `18-19`, `19-20`
  - best field L1 `0.569337308`
  - near-best field L1 range `0.569337308-0.569402158`
  - near-best diameter range `8.002221584-12.178489938 mm`
  - best source frequency `30 MHz`
  - mean iteration runtime `16.12 s`
- Product report `185`:
  - primary y center remains the older global y/length estimate `1.75 m`
  - adaptive scattered y center `1.45 m`
  - adaptive scattered y window `[1.4, 1.5] m`
  - adaptive y status `adaptive_scattered_bracketed_single_window_minimum`
  - y conflict `0.3 m`
  - adaptive depth `1.488175154 m`
  - adaptive epsr `3.296571254`
  - adaptive background sigma `0.003752571 S/m`
  - adaptive diameter range `8.002221584-12.178489938 mm`
- Product leaderboard and shipping snapshot:
  - leaderboard `036_field_prediction_product_leaderboard`
  - shipping snapshot `037_field_prediction_shipping_snapshot`
  - shipping blocker now explicitly states primary y `1.75 m` conflicts with adaptive scattered y `1.45 m`.

## What Remains Blocked

- The 0701 product now has two incompatible y estimates:
  - older global y/length objective: profile `17-18`, y center `1.75 m`
  - current adaptive scattered low-frequency objective: profile `14-15`, y center `1.45 m`
- Diameter is narrowed under the adaptive objective, but still not a single value:
  - current adaptive near-best range `8.00-12.18 mm`
- Full finite-length 3D FDTD inversion is still not implemented; current y/length remains a stack/profile-window proxy.

## Current Decision

The current shippable 0701 product should not claim a settled 3D y/length estimate. It should report the primary historical y/length row plus the adaptive scattered y bracket, and mark the y conflict as a product blocker.

The most useful current operational prediction from the adaptive scattered objective is:

- y center `1.45 m`
- y window `[1.4, 1.5] m`
- z depth `1.488 m`
- epsr `3.297`
- background sigma `0.003753 S/m`
- diameter range `8.00-12.18 mm`
- field L1 `0.569337`

## Next Defensible Task

Resolve the y-objective conflict before promoting a final 3D product estimate:

- either rerun the older y/length/global objective under the same 30 MHz adaptive scattered source/timing objective,
- or build a direct reconciler that evaluates both candidate y windows under a common objective and selects the primary product y/length row.

After that, the next product branch should test whether length is actually constrained around the selected y window, not only inferred from adjacent profile windows.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `21 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `183.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1889, 767)`, min/max `(0, 255)`, stddev `71.384`
  - `185.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `53.340`
  - `036.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `64.293`
  - `037.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `64.482`
- Compute note:
  - Fast-GPR optimizer compute used base Miniforge Python because the `gpr-fdtd-fwi` conda env does not currently contain `torch`.
  - Focused tests and compile checks still run in `gpr-fdtd-fwi`.

## Artifact Paths

- Extended adaptive y synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/183_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_freq30_profile_transfer_extended_y_bracket`
- Refreshed 0701 product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/185_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/036_field_prediction_product_leaderboard`
- Refreshed shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/037_field_prediction_shipping_snapshot`
- New adaptive profile-window runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/174_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz_profiles15_16`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/175_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz_profiles15_16`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/176_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz_profiles19_20`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/177_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz_profiles19_20`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/178_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz_profiles14_15`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/179_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz_profiles14_15`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/180_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz_profiles13_14`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/181_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz_profiles13_14`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
