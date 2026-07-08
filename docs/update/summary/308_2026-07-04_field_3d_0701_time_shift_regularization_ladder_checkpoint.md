# Field 3D 0701 Time-Shift Regularization Ladder Checkpoint

Date: 2026-07-04

## What Changed

- Extended checkpoint `307` from a two-weight sensitivity check to a four-weight time-shift regularization ladder.
- Ran receiver-mean AdamW adaptive checks on the same global-y 0701 real field window with:
  - weights `0.0025`, `0.005`, `0.01`, `0.02`
  - seeds `8 mm` and `12 mm`
  - scale `5` Fast-GPR samples
- Synthesized all eight regularized runs.
- Refreshed the 0701 product report, product leaderboard, and shipping snapshot to cite the full ladder artifact.

## Key Numbers

- Additional ladder runs:
  - `137_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w00025`
    - best objective `0.912259161`
    - best raw field L1 `0.912250161`
    - best diameter `8.002206683 mm`
  - `138_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w00025`
    - best objective `0.922890365`
    - best raw field L1 `0.922828734`
    - best diameter `11.927725747 mm`
  - `139_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w001`
    - best objective `0.912286162`
    - best raw field L1 `0.912250161`
    - best diameter `8.002206683 mm`
  - `140_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w001`
    - best objective `0.923624039`
    - best raw field L1 `0.923624039`
    - best diameter `12.000000104 mm`
- Full ladder synthesis:
  - artifact `141_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_shiftreg_weight_ladder`
  - run count `8`
  - best label `seed12_w0005`
  - best field L1 `0.908185482`
  - best diameter `11.927716434 mm`
  - near-best diameter range `8.002206683-11.927716434 mm`
  - near-best labels `seed08_w00025`, `seed08_w0005`, `seed12_w0005`, `seed08_w001`, `seed08_w002`
  - time-shift regularization weights `[0.0025, 0.005, 0.01, 0.02]`
  - diameter status `optimizer_seed_diameter_near_best_narrow_range`
  - gradient status `radius_gradient_negligible_timing_dominated`
- Refreshed product artifacts:
  - 0701 product report `142_field_3d_0701_predictor_product_report`
  - product leaderboard `026_field_prediction_product_leaderboard`
  - shipping snapshot `027_field_prediction_shipping_snapshot`

## What Remains Blocked

- The best field L1 occurs at `11.93 mm` only for the `0.005` timing prior. Seed `8 mm` is more stable across all tested timing-prior weights.
- The product should therefore keep diameter as `8.00-11.93 mm`, not a unique `11.93 mm` claim.
- Radius gradients remain timing-dominated, so source/time modeling remains the main diameter blocker.
- Full finite-length 3D FDTD geometry is still not implemented in this product path; y/length remains a stack-profile proxy.

## Current Decision

The full ladder strengthens the current deliverable without overclaiming:

- best point: `11.93 mm`,
- stable lower candidate: `8.00 mm`,
- reportable adaptive diameter range: `8.00-11.93 mm`,
- x/y/z/length/material values remain unchanged from the global-y product report,
- the claim boundary must mention residual-mode and timing-prior sensitivity.

## Next Defensible Task

The next real-data improvement should attack the timing-dominated gradient directly:

- add a source-time parameterization or source wavelet alignment term rather than only a scalar shift penalty,
- compare whether it preserves the `0.908185` field L1 while reducing diameter sensitivity,
- or test the same regularized receiver-mean path on another real field stack/window before claiming transfer.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `21 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `141.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1888, 767)`, min/max `(0, 255)`, stddev `76.351`
  - `142.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `55.748`
  - `026.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `63.654`
  - `027.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `68.752`

## Artifact Paths

- Full ladder synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/141_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_shiftreg_weight_ladder`
- Refreshed 0701 product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/142_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/026_field_prediction_product_leaderboard`
- Refreshed shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/027_field_prediction_shipping_snapshot`
- Additional ladder run outputs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/137_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w00025`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/138_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w00025`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/139_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w001`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/140_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w001`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
