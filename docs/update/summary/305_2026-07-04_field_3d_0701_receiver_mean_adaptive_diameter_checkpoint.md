# Field 3D 0701 Receiver-Mean Adaptive Diameter Checkpoint

Date: 2026-07-04

## What Changed

- Tested adaptive global-y scattered optimization with receiver-mean residuals, because the fixed receiver-mean scattered diagnostic was the strongest `8 mm` result.
- Ran AdamW, weight decay `0.01`, four iterations per seed.
- Seeds:
  - `8 mm`
  - `12 mm`
  - `16 mm`
  - `20 mm`
- Synthesized the receiver-mean adaptive seed set.
- Refreshed the 0701 product report, product leaderboard, and shipping snapshot.

## Key Numbers

- Receiver-mean adaptive runs:
  - `118_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08`
    - best diameter `8.002206683 mm`
    - best loss `0.912249922752`
    - decision `decreased_field_loss`
  - `120_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12`
    - best diameter `11.927723885 mm`
    - best loss `0.912220895290`
    - decision `decreased_field_loss`
  - `121_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed16`
    - best diameter `16.000000760 mm`
    - best loss `0.922251760960`
    - decision `no_loss_decrease`
  - `119_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed20`
    - best diameter `19.832640886 mm`
    - best loss `0.919367372990`
    - decision `decreased_field_loss`
- Receiver-mean adaptive synthesis:
  - artifact `122_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw`
  - best diameter `11.927723885 mm`
  - near-best range `8.002206683-11.927723885 mm`
  - diameter status `optimizer_seed_diameter_near_best_narrow_range`
  - gradient status `radius_gradient_available`
- Refreshed 0701 product report:
  - artifact `123_field_3d_0701_predictor_product_report`
  - fixed scattered diagnostic: top `8 mm`, common overlap `8-8 mm`
  - adaptive receiver-mean diagnostic: best `11.93 mm`, near-best `8.00-11.93 mm`
- Refreshed leaderboard:
  - artifact `020_field_prediction_product_leaderboard`
- Refreshed shipping snapshot:
  - artifact `021_field_prediction_shipping_snapshot`
  - 0701 diameter compact status `fixed_scattered_candidate_with_adaptive_narrow_range`
  - GSSI status remains `seed_sensitive_range`

## What Remains Blocked

- Receiver-mean adaptive optimization narrows diameter substantially, but still reports a range, not a unique diameter.
- Profile-mean adaptive optimization was broader, so residual-mode sensitivity remains a claim boundary.
- We still need source/time regularization or objective refinement before calling diameter fully identified.

## Current Decision

This is a real product improvement:

- fixed scattered global-y diagnostic supports `8 mm`,
- receiver-mean adaptive global-y optimizer supports `8-12 mm`,
- radius gradients are now available under the receiver-mean adaptive objective,
- product should report diameter as a narrow range, not as a unique value.

Current 0701 product-facing state:

- x `9.819 m`,
- y center `1.750 m`,
- z `1.508 m`,
- length proxy `0.100 m`, supported `0.100-0.500 m`,
- epsr `3.365`,
- conductivity `0.00358 S/m`,
- diameter fixed diagnostic `8 mm`,
- adaptive diameter range `8.00-11.93 mm`.

## Next Defensible Task

Use the receiver-mean adaptive result as the promoted 0701 diameter path and improve robustness:

- run a longer receiver-mean AdamW check from seeds `8` and `12`,
- or test source/time regularization to reduce residual-mode sensitivity,
- then update the product only if the `8-12 mm` range stays stable or narrows.

## Validation And Resources

- `python -m pytest tests/test_field_3d_0701_predictor_product_report.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `16 passed`
- `python -m py_compile run_field_3d_0701_predictor_product_report.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `118.../figures/field_3d_0701_fastgpr_scattered_geometry_material_optimizer.png`: size `(2365, 750)`, min/max `(0, 255)`, stddev `37.37`
  - `122.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1889, 767)`, min/max `(0, 255)`, stddev `70.60`
  - `123.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `53.91`
  - `020.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `64.29`
  - `021.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `64.48`

## Artifact Paths

- Receiver-mean adaptive runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/118_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/120_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/121_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed16`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/119_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed20`
- Receiver-mean adaptive synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/122_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw`
- Refreshed 0701 product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/123_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/020_field_prediction_product_leaderboard`
- Refreshed shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/021_field_prediction_shipping_snapshot`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
