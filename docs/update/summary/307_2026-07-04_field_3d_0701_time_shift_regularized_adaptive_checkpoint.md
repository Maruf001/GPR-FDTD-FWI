# Field 3D 0701 Time-Shift-Regularized Adaptive Checkpoint

Date: 2026-07-04

## What Changed

- Added optional time-shift prior regularization to the 0701 Fast-GPR scattered geometry/material optimizer.
- Kept raw field L1 separate from the optimized objective loss so regularized and unregularized evidence are not mixed silently.
- Ran receiver-mean AdamW adaptive checks on the promoted global-y window for seeds `8 mm` and `12 mm` at two time-shift prior strengths:
  - `weight=0.02`, scale `5` Fast-GPR samples
  - `weight=0.005`, scale `5` Fast-GPR samples
- Synthesized regularization sensitivity across the four runs.
- Refreshed the 0701 product report, product leaderboard, and shipping snapshot to expose the regularized adaptive evidence.

## Key Numbers

- Regularized runs:
  - `128_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w002`
    - best objective `0.912322164`
    - best raw field L1 `0.912250161`
    - best diameter `8.002206683 mm`
  - `129_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w002`
    - best objective `0.923624039`
    - best raw field L1 `0.923624039`
    - best diameter `12.000000104 mm`
    - no loss decrease under the stronger time prior
  - `131_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005`
    - best objective `0.912268162`
    - best raw field L1 `0.912250161`
    - best diameter `8.002206683 mm`
  - `132_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005`
    - best objective `0.908307612`
    - best raw field L1 `0.908185482`
    - best diameter `11.927716434 mm`
- Regularization sensitivity synthesis:
  - artifact `135_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_shiftreg_sensitivity`
  - best label `seed12_w0005`
  - best loss key `objective_loss`
  - best field L1 `0.908185482`
  - near-best diameter range `8.002206683-11.927716434 mm`
  - near-best labels `seed08_w002`, `seed08_w0005`, `seed12_w0005`
  - time-shift regularization weights tested `[0.005, 0.02]`
  - diameter status `optimizer_seed_diameter_near_best_narrow_range`
  - gradient status `radius_gradient_negligible_timing_dominated`
- Refreshed 0701 product report:
  - artifact `136_field_3d_0701_predictor_product_report`
  - x `9.819386152 m`
  - y center `1.750 m`
  - z `1.507775545 m`
  - length proxy `0.100 m`, supported length `0.100-0.500 m`
  - epsr `3.364521503`
  - background conductivity `0.003581968 S/m`
  - adaptive regularized diameter best/range `11.927716434 mm` / `8.002206683-11.927716434 mm`
  - adaptive best raw field L1 `0.908185482`
- Refreshed top-level artifacts:
  - leaderboard `024_field_prediction_product_leaderboard`
  - shipping snapshot `025_field_prediction_shipping_snapshot`

## What Remains Blocked

- The time-shift-regularized objective improves the best adaptive field L1, but diameter remains a range.
- Stronger time prior favors `8 mm`; weaker time prior keeps `11.93 mm` as the best point while still retaining `8 mm` near-best. This is useful evidence, not a unique diameter claim.
- Radius gradients remain timing-dominated, so source/time modeling is still the main blocker to a stronger diameter claim.
- The current y/length estimate is still a stack/profile-window proxy, not a full finite-length 3D steel-cylinder FDTD inversion.

## Current Decision

The product-facing 0701 predictor should now cite the regularized adaptive sensitivity artifact `135`, because it gives the strongest current raw field fit while preserving the honest range:

- best point: `11.93 mm`,
- supported adaptive range: `8.00-11.93 mm`,
- x/y/z/length/material values unchanged from the global-y product report,
- explicit caveat: residual-mode and timing-prior sensitivity remain.

## Next Defensible Task

Continue improving the real-data predictor, not synthetic detours:

- test a source/time model with an explicit source-time parameter prior rather than only a shift penalty,
- or run a small regularization-weight ladder around `0.0025-0.01` to see whether the `11.93 mm` best field L1 is stable,
- then promote only if the field L1 and diameter range remain stable.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `21 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `135.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1889, 767)`, min/max `(0, 255)`, stddev `76.009`
  - `136.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `55.748`
  - `024.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `63.654`
  - `025.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `68.752`

## Artifact Paths

- Regularized optimizer runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/128_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w002`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/129_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w002`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/131_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_shiftreg_w0005`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/132_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_shiftreg_w0005`
- Regularization sensitivity synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/135_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_shiftreg_sensitivity`
- Refreshed 0701 product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/136_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/024_field_prediction_product_leaderboard`
- Refreshed shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/025_field_prediction_shipping_snapshot`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
