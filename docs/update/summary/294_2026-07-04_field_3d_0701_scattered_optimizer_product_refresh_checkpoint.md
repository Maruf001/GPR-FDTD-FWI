# Field 3D 0701 Scattered Optimizer Product Refresh Checkpoint

Date: 2026-07-04

## What Changed

- Added `run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py`.
- Added focused tests for scattered optimizer helper logic and summary synthesis.
- Ran the first real-field autograd scattered-response optimizer branch:
  - differentiable Fast-GPR anomaly forward,
  - differentiable Fast-GPR baseline forward,
  - anomaly-minus-baseline prediction,
  - residualized 0701 field window objective,
  - optimized epsr, x/depth proxy, radius, conductivity, and continuous time shift.
- Added `run_field_3d_0701_scattered_optimizer_seed_synthesis.py`.
- Refreshed the 0701 product report to carry both:
  - fixed scattered-objective diagnostic diameter candidate,
  - scattered-optimizer near-best diameter range.
- Refreshed the product leaderboard to point at the new product report.

## Key Numbers

- Scattered optimizer runs:
  - `085_adam_seed20`: best loss `0.784753441811`, best diameter `19.999992 mm`, mean iteration runtime `12.41 s`
  - `086_adamw_seed20`: best loss `0.777351498604`, best diameter `19.999932 mm`, mean iteration runtime `21.75 s`
  - `087_adam_seed16`: best loss `0.777131259441`, best diameter `15.999997 mm`, mean iteration runtime `18.52 s`
  - `088_adam_seed24`: best loss `0.802903592587`, best diameter `23.999996 mm`, mean iteration runtime `11.77 s`
- Optimizer seed synthesis:
  - artifact `089_field_3d_0701_scattered_optimizer_seed_synthesis`
  - best label `adam_seed16`
  - best diameter `15.999997 mm`
  - near-best diameter range `15.999997-19.999932 mm`
  - near-best labels `adamw_seed20`, `adam_seed16`
  - diameter status `optimizer_seed_diameter_near_best_narrow_range`
  - mean iteration runtime across runs `16.11 s`
- Refreshed product report:
  - artifact `090_field_3d_0701_predictor_product_report`
  - x `9.819386151982 m`
  - assumed y center `0.200000 m`
  - z depth `1.507637023926 m`
  - y-length proxy `0.200000 m`
  - epsr `4.803974151611`
  - background conductivity `0.008403605781 S/m`
  - full-objective diameter range `8-30 mm`
  - fixed scattered diagnostic diameter `20.0 mm`
  - scattered-optimizer diagnostic best diameter `15.999997 mm`
  - scattered-optimizer diagnostic near-best range `15.999997-19.999932 mm`
- Refreshed leaderboard:
  - artifact `007_field_prediction_product_leaderboard`
  - 0701 best product points to `090_field_3d_0701_predictor_product_report`
  - GSSI best product remains `049_gssi51600s_surface_bscan_product_report`

## What Remains Blocked

- Diameter is still not a unique product-grade claim. The optimizer supports a narrow diagnostic range, not a single radius.
- The current 0701 x/y/z/y-length output is still a stack/y-window proxy, not a full finite-length steel rebar 3D inversion.
- The surface-style bridge geometry remains a sensitivity model; receiver y `0.50 m` is not yet a validated measured acquisition parameter.
- The optimizer runs are short smoke runs. Longer and multi-profile validation is needed before upgrading the diameter claim.

## Current Decision

The deliverable is stronger than checkpoint 293 because it now reports a field-data optimizer-supported diameter range, not just a fixed-radius scan candidate. The defensible current statement is:

- x/y/z/material/y-window proxy is product-visible but provisional,
- full-objective diameter remains `8-30 mm`,
- scattered-response diagnostics support a practical diameter range around `16-20 mm`,
- 24 mm is disfavored in this optimizer smoke,
- no unique 3D diameter or rebar length claim yet.

## Next Defensible Task

Run a stricter scattered-optimizer validation:

- repeat seed `16, 20, 24 mm` with matched optimizer settings,
- add Adamax or longer AdamW where useful,
- log per-parameter gradient magnitudes,
- decide whether the near-best `16-20 mm` range is stable under residual mode and optimizer choice.

## Validation And Resources

- `python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py`
- `python -m py_compile run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_prediction_product_leaderboard.py`
- `python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py -q`
  - `5 passed`
- `python -m pytest tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py -q`
  - `12 passed`
- `python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_3d_0701_fastgpr_radius_scattered_objective_scan.py tests/test_field_3d_0701_scattered_radius_objective_synthesis.py -q`
  - `18 passed`
- Touched-file `git diff --check` passed.
- Figure checks:
  - `089.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1889, 767)`, min/max `(0, 255)`, stddev `70.46`
  - `090.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `54.14`
  - `007.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `64.79`

## Artifact Paths

- Scattered optimizer runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/085_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_adam_smoke`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/086_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_adamw_smoke`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/087_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_adam_seed16_smoke`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/088_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_adam_seed24_smoke`
- Optimizer seed synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/089_field_3d_0701_scattered_optimizer_seed_synthesis`
- Refreshed product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/090_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/007_field_prediction_product_leaderboard`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
