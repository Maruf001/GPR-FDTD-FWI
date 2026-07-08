# Field 3D 0701 Receiver-Mean Scattered Optimizer Checkpoint

Date: 2026-07-04

## What Changed

- Ran receiver-mean residual-mode cross-checks for the scattered optimizer.
- Reused the matched AdamW settings from checkpoint 295:
  - learning rate `0.03`
  - weight decay `0.001`
  - iterations `3`
  - diameter seeds `16, 20, 24 mm`
- Synthesized the receiver-mean seed set.
- Updated the combined optimizer claim synthesis to include:
  - mixed optimizer seed synthesis,
  - matched profile-mean AdamW synthesis,
  - matched receiver-mean AdamW synthesis.
- Refreshed the product report and product leaderboard.

## Key Numbers

- Receiver-mean AdamW seed runs:
  - `097_adamw_receiver_seed16`: best loss `0.780144810677`, best diameter `16.000167 mm`
  - `098_adamw_receiver_seed20`: best loss `0.781049847603`, best diameter `19.999932 mm`
  - `099_adamw_receiver_seed24`: best loss `0.779722452164`, best diameter `23.999739 mm`
- Receiver-mean synthesis:
  - artifact `100_field_3d_0701_scattered_optimizer_receiver_mean_adamw_seed_gradient_synthesis`
  - best label `adamw_receiver_seed24`
  - near-best labels `adamw_receiver_seed16`, `adamw_receiver_seed20`, `adamw_receiver_seed24`
  - near-best diameter range `16.000167-23.999739 mm`
  - diameter status `optimizer_seed_diameter_degenerate`
  - max raw radius gradient `2.590248e-13`
  - max raw time-shift gradient `2.634177e-02`
  - gradient status `radius_gradient_negligible_timing_dominated`
- Combined claim synthesis with receiver-mean:
  - artifact `101_field_3d_0701_scattered_optimizer_claim_synthesis_with_receiver_mean`
  - input synthesis count `3`
  - diagnostic optimizer top/common candidate `19.999932 mm`
  - diagnostic optimizer union range `15.999997-23.999739 mm`
  - claim status `optimizer_sensitive_diagnostic_range_with_common_overlap_radius_gradient_weak`
- Refreshed product report:
  - artifact `102_field_3d_0701_predictor_product_report`
  - source artifact for optimizer claim points to `101.../field_3d_0701_scattered_optimizer_claim_synthesis_rows.csv`
- Refreshed leaderboard:
  - artifact `009_field_prediction_product_leaderboard`
  - 0701 source summary points to `102_field_3d_0701_predictor_product_report`

## What Remains Blocked

- Receiver-mean residuals do not fix diameter identifiability.
- Radius gradients remain effectively zero while time-shift gradients dominate.
- The product can report a useful 20 mm diagnostic candidate and a `16-24 mm` optimizer-sensitive range, but not a unique radius.
- This remains a surface-style/smooth-cylinder bridge, not a complete finite-length 3D steel-rebar inversion.

## Current Decision

Residual-mode cross-check strengthens the claim boundary rather than the diameter claim. The current product-grade wording should be:

- common diagnostic diameter candidate near `20 mm`,
- optimizer-sensitive diagnostic diameter range about `16-24 mm`,
- no unique radius claim because multiple residual/optimizer settings keep wide near-best ranges and radius gradients are negligible.

## Next Defensible Task

The next branch should either:

- change the scattered objective normalization to make radius gradients visible, or
- run the same gradient-diagnostic optimizer on the GSSI surface adapter, where shallower geometry may produce stronger radius sensitivity.

## Validation And Resources

- `python -m py_compile run_field_3d_0701_scattered_optimizer_claim_synthesis.py`
- `python -m pytest tests/test_field_3d_0701_scattered_optimizer_claim_synthesis.py -q`
  - `2 passed`
- `python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_scattered_optimizer_claim_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_3d_0701_fastgpr_radius_scattered_objective_scan.py tests/test_field_3d_0701_scattered_radius_objective_synthesis.py -q`
  - `22 passed`
- Touched-file `git diff --check` passed.
- Figure checks:
  - `100.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1889, 767)`, min/max `(0, 255)`, stddev `70.08`
  - `101.../figures/field_3d_0701_scattered_optimizer_claim_synthesis.png`: size `(1725, 767)`, min/max `(0, 255)`, stddev `40.67`
  - `102.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `54.76`
  - `009.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `64.79`

## Artifact Paths

- Receiver-mean optimizer runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/097_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_adamw_seed16_receiver_mean_grad`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/098_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_adamw_seed20_receiver_mean_grad`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/099_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_adamw_seed24_receiver_mean_grad`
- Receiver-mean synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/100_field_3d_0701_scattered_optimizer_receiver_mean_adamw_seed_gradient_synthesis`
- Combined claim synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/101_field_3d_0701_scattered_optimizer_claim_synthesis_with_receiver_mean`
- Refreshed product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/102_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/009_field_prediction_product_leaderboard`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
