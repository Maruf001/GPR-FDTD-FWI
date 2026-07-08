# Field 3D 0701 Global-Y Adaptive Scattered Optimizer Checkpoint

Date: 2026-07-04

## What Changed

- Ran the adaptive scattered geometry/material optimizer on the improved 0701 global y-window from checkpoint 301.
- Used profiles `17-18` from the global fine y scan.
- Used AdamW with weight decay `0.01`, four iterations per seed.
- Tested diameter seeds:
  - `8 mm`
  - `12 mm`
  - `16 mm`
  - `20 mm`
- Synthesized the adaptive global-y seed set with `run_field_3d_0701_scattered_optimizer_seed_synthesis.py`.
- Refreshed the 0701 product report and product leaderboard with the adaptive caveat.

## Key Numbers

- Adaptive global-y optimizer runs:
  - `112_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_adamw_seed08`
    - best diameter `8.002200164 mm`
    - best loss `0.967828154564`
    - max raw radius gradient `3.05e-12`
    - max raw time-shift gradient `0.032913`
  - `114_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_adamw_seed12`
    - best diameter `12.000000104 mm`
    - best loss `0.962134540081`
    - max raw radius gradient `6.11e-09`
    - max raw time-shift gradient `0.061482`
  - `115_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_adamw_seed16`
    - best diameter `16.000000760 mm`
    - best loss `0.964717745781`
    - max raw radius gradient `2.64e-09`
    - max raw time-shift gradient `0.059066`
  - `113_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_adamw_seed20`
    - best diameter `19.999999553 mm`
    - best loss `0.961901366711`
    - max raw radius gradient `5.37e-09`
    - max raw time-shift gradient `0.041582`
- Adaptive global-y seed synthesis:
  - artifact `116_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_adamw`
  - best diameter `19.999999553 mm`
  - near-best diameter range `12.000000104-19.999999553 mm`
  - status `optimizer_seed_diameter_degenerate`
  - gradient status `radius_gradient_negligible_timing_dominated`
  - mean iteration runtime about `11.36 s`
- Refreshed 0701 product report:
  - artifact `117_field_3d_0701_predictor_product_report`
  - fixed global-y scattered diagnostic still reports top `8 mm`, common overlap `8-8 mm`
  - adaptive global-y optimizer reports best `20 mm`, near-best `12-20 mm`, diameter degenerate
- Refreshed product leaderboard:
  - artifact `017_field_prediction_product_leaderboard`

## What Remains Blocked

- The adaptive optimizer does not confirm a unique `8 mm` diameter once material and timing are free.
- Radius gradients are still tiny relative to time-shift gradients.
- The adaptive objective is seed-locked over a broad range; it does not pull large seeds toward the fixed-radius `8 mm` diagnostic.

## Current Decision

The product-facing 0701 diameter statement must remain bounded:

- fixed-radius global-y scattered diagnostic: strong `8 mm` candidate with residual-mode agreement,
- adaptive global-y scattered optimizer: degenerate `12-20 mm` near-best range with timing-dominated gradients,
- therefore do not claim a unique adaptive FWI diameter yet.

The 0701 geometry/material product remains improved from checkpoint 301:

- x `9.819 m`,
- y center `1.750 m`,
- z `1.508 m`,
- length proxy `0.100 m`, supported `0.100-0.500 m`,
- epsr `3.365`,
- conductivity `0.00358 S/m`,
- diameter diagnostic top `8 mm`, adaptive caveat `12-20 mm`.

## Next Defensible Task

Create a product-facing field predictor snapshot/gap matrix that compares the current best 0701 and GSSI deliverables:

- x/y/z support,
- radius/diameter support,
- length support,
- epsr/conductivity support,
- optimizer method and runtime,
- current blocker for shipping a stronger claim.

Then use that snapshot to choose whether the next improvement should target 0701 adaptive radius gradients, GSSI 3D/y extension, or a shared source/time-alignment upgrade.

## Validation And Resources

- `python -m pytest tests/test_field_3d_0701_predictor_product_report.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_prediction_product_leaderboard.py tests/test_field_3d_0701_scattered_radius_objective_synthesis.py -q`
  - `15 passed`
- `python -m py_compile run_field_3d_0701_predictor_product_report.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_prediction_product_leaderboard.py run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `112.../figures/field_3d_0701_fastgpr_scattered_geometry_material_optimizer.png`: size `(2365, 750)`, min/max `(0, 255)`, stddev `36.53`
  - `113.../figures/field_3d_0701_fastgpr_scattered_geometry_material_optimizer.png`: size `(2365, 750)`, min/max `(0, 255)`, stddev `36.98`
  - `116.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1889, 767)`, min/max `(0, 255)`, stddev `70.51`
  - `117.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `53.91`
  - `017.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `64.29`

## Artifact Paths

- Adaptive global-y optimizer runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/112_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_adamw_seed08`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/114_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_adamw_seed12`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/115_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_adamw_seed16`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/113_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_adamw_seed20`
- Adaptive global-y seed synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/116_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_adamw`
- Refreshed 0701 product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/117_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/017_field_prediction_product_leaderboard`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
