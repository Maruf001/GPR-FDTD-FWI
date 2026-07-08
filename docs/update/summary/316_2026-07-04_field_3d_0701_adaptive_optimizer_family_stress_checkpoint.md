# Field 3D 0701 Adaptive Optimizer-Family Stress Checkpoint

Date: 2026-07-04

## What Changed

- Stress-tested the promoted adaptive y/length row under multiple optimizers:
  - AdamW,
  - Adam,
  - Adamax.
- Used the same product-relevant setup for all runs:
  - profile window `14-16`,
  - source frequency `30 MHz`,
  - residual mode `receiver_mean`,
  - timing regularization weight `0.005`,
  - timing regularization scale `5` samples,
  - diameter seeds `8 mm` and `12 mm`.
- Synthesized the six optimizer-family runs into a single stability artifact.

## Key Numbers

- AdamW references:
  - `188...adamw_seed08...profiles14_16_len3`
    - field L1 `0.537834`
    - diameter `8.002 mm`
  - `189...adamw_seed12...profiles14_16_len3`
    - field L1 `0.537872`
    - diameter `11.897 mm`
- Adam:
  - `202...adam_seed08...profiles14_16_len3`
    - field L1 `0.537832`
    - diameter `8.002 mm`
  - `201...adam_seed12...profiles14_16_len3`
    - field L1 `0.537918`
    - diameter `11.908 mm`
- Adamax:
  - `203...adamax_seed08...profiles14_16_len3`
    - field L1 `0.537808`
    - diameter `8.002 mm`
  - `204...adamax_seed12...profiles14_16_len3`
    - field L1 `0.537949`
    - diameter `11.908 mm`
- Optimizer-family synthesis:
  - artifact `206_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_freq30_y_length_optimizer_family`
  - all six optimizer/seed runs are near-best
  - best objective label `adam_seed08`
  - best raw field-L1 run is Adamax seed08 at `0.537808`
  - near-best diameter range `8.002196439-11.907658540 mm`
  - y center `1.50 m`
  - profile window `14-16`
  - profile length `3`
  - center-span length `0.20 m`
  - field-L1 range `0.537808120-0.537949026`
  - objective-loss range `0.537900984-0.538004994`

## What Remains Blocked

- Optimizer family does not resolve diameter to a single value; it confirms the `8.00-11.91 mm` range.
- This stress test covers optimizer choice, not residual-mode choice or source-frequency choice.
- The result still uses a profile-window length proxy rather than a full 3D finite-length FDTD inversion.

## Current Decision

The promoted adaptive y/length row is stable across AdamW, Adam, and Adamax:

- y center remains `1.50 m`,
- window remains `14-16`,
- center-span length remains `0.20 m`,
- field loss changes only at the `1e-4` scale,
- diameter remains a narrow seed-dependent range around `8-12 mm`.

This strengthens the product claim that the y/length/material row is not an AdamW-only artifact.

## Next Defensible Task

Run residual-mode sensitivity around the promoted row:

- keep window `14-16`,
- keep source frequency `30 MHz`,
- keep optimizer family to the current best or default AdamW/Adam,
- compare `profile_mean`, `receiver_mean`, and `global_mean` residual modes.

If residual-mode sensitivity is acceptable, promote the current shipping row from "provisional" toward a stronger product-ready status. If not, keep the current claim boundary but report which residual mode controls the estimate.

## Validation And Resources

- Product test/compile validation from checkpoint 315 still applies:
  - `21 passed`
  - py_compile passed
  - touched-file `git diff --check` passed
- Additional figure check:
  - `206.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1888, 767)`, min/max `(0, 255)`, stddev `70.841`
- Diff hygiene:
  - touched-file `git diff --check` passed after this branch.
- Compute note:
  - Run `200...adam_seed08...` is a failed partial run from a mistyped radius-summary filename.
  - Successful Adam seed08 rerun is `202...adam_seed08...`.

## Artifact Paths

- Optimizer-family synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/206_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_freq30_y_length_optimizer_family`
- Adam runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/202_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adam_seed08_shiftreg_w0005_freq30mhz_profiles14_16_len3`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/201_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adam_seed12_shiftreg_w0005_freq30mhz_profiles14_16_len3`
- Adamax runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/203_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamax_seed08_shiftreg_w0005_freq30mhz_profiles14_16_len3`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/204_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamax_seed12_shiftreg_w0005_freq30mhz_profiles14_16_len3`
- AdamW reference runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/188_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005_freq30mhz_profiles14_16_len3`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/189_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005_freq30mhz_profiles14_16_len3`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
