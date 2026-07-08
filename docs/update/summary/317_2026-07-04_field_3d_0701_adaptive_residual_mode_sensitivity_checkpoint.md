# Field 3D 0701 Adaptive Residual-Mode Sensitivity Checkpoint

Date: 2026-07-04

## What Changed

- Tested residual-mode sensitivity around the promoted adaptive `14-16` y/length row.
- Used Adamax because the optimizer-family stress showed it slightly improved raw field L1 while preserving the promoted y/length row.
- Compared:
  - `receiver_mean`,
  - `profile_mean`,
  - `global_mean`.

## Key Numbers

- Receiver-mean reference:
  - `203...receiver_mean_adamax_seed08...profiles14_16_len3`
    - field L1 `0.537808`
    - diameter `8.002 mm`
    - depth `1.488 m`
    - epsr `3.284`
  - `204...receiver_mean_adamax_seed12...profiles14_16_len3`
    - field L1 `0.537949`
    - diameter `11.908 mm`
    - depth `1.490 m`
    - epsr `3.299`
- Profile-mean:
  - `207...profile_mean_adamax_seed08...profiles14_16_len3`
    - field L1 `0.668999`
    - diameter `8.002 mm`
    - depth `1.483 m`
    - epsr `3.460`
  - `208...profile_mean_adamax_seed12...profiles14_16_len3`
    - field L1 `0.669111`
    - diameter `11.810 mm`
    - depth `1.490 m`
    - epsr `3.434`
- Global-mean:
  - `209...global_mean_adamax_seed08...profiles14_16_len3`
    - field L1 `0.640358`
    - diameter `8.002 mm`
    - depth `1.484 m`
    - epsr `3.273`
  - `210...global_mean_adamax_seed12...profiles14_16_len3`
    - field L1 `0.640265`
    - diameter `12.243 mm`
    - depth `1.482 m`
    - epsr `3.274`
- Residual-mode synthesis:
  - artifact `211_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_adamax_freq30_y_length_residual_mode_sensitivity`
  - best label `receiver_mean_seed08`
  - near-best labels `receiver_mean_seed08`, `receiver_mean_seed12`
  - full field-L1 range `0.537808120-0.669110835`
  - near-best field-L1 range `0.537808120-0.537949026`
  - near-best diameter range `8.002197370-11.907625943 mm`
  - y center `1.50 m`
  - profile window `14-16`
  - center-span length `0.20 m`

## What Remains Blocked

- Residual mode changes absolute loss and material estimates.
- Receiver-mean is the only near-best residual mode, so the product should state that the current operational objective is receiver-mean controlled.
- Diameter remains a range.
- Still no full finite-length 3D FDTD inversion.

## Current Decision

The promoted y/length row is geometrically stable under residual-mode stress:

- all modes use profile window `14-16`,
- depths remain around `1.48-1.49 m`,
- diameter remains split by seed around `8-12 mm`.

But the fit quality is residual-mode sensitive:

- receiver-mean is clearly best,
- global-mean and profile-mean are worse under the current objective.

The product claim should keep `receiver_mean` as part of the operational method definition.

## Next Defensible Task

Wire residual-mode sensitivity into the product report and shipping snapshot:

- add residual-mode status fields,
- keep operational row as receiver-mean,
- change the blocker language from "residual-mode sensitivity remains" to "receiver-mean controls the current product fit; profile/global modes are worse but do not move y/length."

After that, source-frequency robustness around the promoted `14-16` row is the next product-relevant stress test.

## Validation And Resources

- Additional figure check:
  - `211.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1888, 767)`, min/max `(0, 255)`, stddev `69.945`
- Previous focused validation still applies from checkpoint 315:
  - `21 passed`
  - py_compile passed
- Diff hygiene passed.

## Artifact Paths

- Residual-mode synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/211_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_adamax_freq30_y_length_residual_mode_sensitivity`
- Profile-mean runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/207_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_profile_mean_adamax_seed08_shiftreg_w0005_freq30mhz_profiles14_16_len3`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/208_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_profile_mean_adamax_seed12_shiftreg_w0005_freq30mhz_profiles14_16_len3`
- Global-mean runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/209_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_global_mean_adamax_seed08_shiftreg_w0005_freq30mhz_profiles14_16_len3`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/210_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_global_mean_adamax_seed12_shiftreg_w0005_freq30mhz_profiles14_16_len3`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
