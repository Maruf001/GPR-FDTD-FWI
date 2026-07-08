# Field 3D 0701 Matched Scattered Optimizer Claim Checkpoint

Date: 2026-07-04

## What Changed

- Patched `run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py` to log per-parameter raw gradient magnitudes.
- Ran a matched AdamW seed set with identical optimizer settings:
  - learning rate `0.03`
  - weight decay `0.001`
  - residual mode `profile_mean`
  - iterations `3`
  - diameter seeds `16, 20, 24 mm`
- Patched `run_field_3d_0701_scattered_optimizer_seed_synthesis.py` to:
  - accept explicit `label=path` summary inputs,
  - include gradient diagnostics,
  - identify timing-dominated weak-radius-gradient cases.
- Added `run_field_3d_0701_scattered_optimizer_claim_synthesis.py`.
- Refreshed the 0701 product report and leaderboard with the combined optimizer claim boundary.

## Key Numbers

- Matched AdamW seed runs:
  - `091_adamw_seed16`: best loss `0.801464021206`, best diameter `16.000001 mm`, no loss decrease
  - `092_adamw_seed20`: best loss `0.777351498604`, best diameter `19.999932 mm`, loss decrease
  - `093_adamw_seed24`: best loss `0.777351498604`, best diameter `23.999739 mm`, loss decrease
- Gradient diagnostics from matched AdamW synthesis:
  - artifact `094_field_3d_0701_scattered_optimizer_matched_adamw_seed_gradient_synthesis`
  - best label `adamw_seed20`
  - near-best diameter range `19.999932-23.999739 mm`
  - max raw radius gradient `4.943591e-13`
  - max raw time-shift gradient `2.757849e-02`
  - gradient status `radius_gradient_negligible_timing_dominated`
- Combined optimizer claim synthesis:
  - artifact `095_field_3d_0701_scattered_optimizer_claim_synthesis`
  - mixed optimizer near-best range from checkpoint 294: `15.999997-19.999932 mm`
  - matched AdamW near-best range: `19.999932-23.999739 mm`
  - common overlap/top diagnostic candidate `19.999932 mm`
  - union diagnostic range `15.999997-23.999739 mm`
  - claim status `optimizer_sensitive_diagnostic_range_with_common_overlap_radius_gradient_weak`
- Refreshed product report:
  - artifact `096_field_3d_0701_predictor_product_report`
  - diagnostic fixed scattered diameter candidate `20.0 mm`
  - diagnostic optimizer common candidate `19.999932 mm`
  - diagnostic optimizer-sensitive range `15.999997-23.999739 mm`
  - diagnostic optimizer status `optimizer_sensitive_diagnostic_range_with_common_overlap_radius_gradient_weak`
- Refreshed leaderboard:
  - artifact `008_field_prediction_product_leaderboard`
  - 0701 best product points to `096_field_3d_0701_predictor_product_report`

## What Remains Blocked

- Diameter/radius is not product-identifiable. The radius-gradient signal is effectively absent under the matched AdamW scattered objective.
- The optimizer is improving mostly through timing/material/background behavior, not by changing radius.
- The product-facing diameter deliverable must remain a diagnostic candidate plus optimizer-sensitive range.
- y position and rebar length remain proxy quantities from the stack/window, not full finite-length 3D rebar inversion.

## Current Decision

The current strongest deliverable statement for the 0701 field stack is:

- x `9.819 m`, assumed y center `0.200 m`, z `1.508 m`,
- y-length proxy `0.200 m`,
- epsr `4.804`, background conductivity `0.00840 S/m`,
- fixed scattered-response diameter candidate `20 mm`,
- optimizer-sensitive diagnostic diameter range `16-24 mm` with common overlap near `20 mm`,
- no unique product-grade radius claim because radius gradients are negligible.

## Next Defensible Task

The next useful branch should attack the source of the radius-gradient weakness:

- run residual-mode cross-checks for the matched optimizer, especially `receiver_mean`,
- test whether a different scattered objective normalization gives nonzero radius gradients,
- or shift to the GSSI surface adapter and see whether a shallower event has stronger radius gradients.

## Validation And Resources

- `python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py`
- `python -m py_compile run_field_3d_0701_scattered_optimizer_seed_synthesis.py`
- `python -m py_compile run_field_3d_0701_scattered_optimizer_claim_synthesis.py`
- `python -m pytest tests/test_field_3d_0701_scattered_optimizer_claim_synthesis.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py -q`
  - `6 passed`
- `python -m pytest tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_3d_0701_scattered_optimizer_claim_synthesis.py -q`
  - `9 passed`
- `python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_scattered_optimizer_claim_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_3d_0701_fastgpr_radius_scattered_objective_scan.py tests/test_field_3d_0701_scattered_radius_objective_synthesis.py -q`
  - `22 passed`
- Touched-file `git diff --check` passed.
- Figure checks:
  - `094.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1889, 767)`, min/max `(0, 255)`, stddev `70.41`
  - `095.../figures/field_3d_0701_scattered_optimizer_claim_synthesis.png`: size `(1689, 767)`, min/max `(0, 255)`, stddev `37.89`
  - `096.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `54.76`
  - `008.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `64.79`

## Artifact Paths

- Matched AdamW runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/091_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_adamw_seed16_grad`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/092_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_adamw_seed20_grad`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/093_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_adamw_seed24_grad`
- Matched AdamW synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/094_field_3d_0701_scattered_optimizer_matched_adamw_seed_gradient_synthesis`
- Combined claim synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/095_field_3d_0701_scattered_optimizer_claim_synthesis`
- Refreshed product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/096_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/008_field_prediction_product_leaderboard`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
