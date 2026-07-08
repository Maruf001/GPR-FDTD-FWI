# Field Prediction Fit Recipe Checkpoint

## What changed
- Added `run_field_prediction_fit_recipe.py`, a reusable recipe builder for current field-prediction fitting commands.
- Added tests:
  - `tests/test_field_prediction_fit_recipe.py`
- The first implemented recipe is:
  - dataset `external_2025_pipe_0806`
  - recipe `current_sample42_adamw_conductivity_diam12`
  - optimizer `AdamW`
  - conductivity enabled
  - diameter seed `12 mm`
  - sample start `42`
  - current `0806` stack and sample-42 seed artifacts

## Key numbers
- Validation:
  - `python -m py_compile run_field_prediction_fit_recipe.py`: passed.
  - `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_fit_recipe.py tests/test_field_prediction_current_query.py -q`: `6 passed`.
  - `git diff --check` on the fit-recipe/query branch: passed.
- Dry-run command:
  - `python run_field_prediction_fit_recipe.py --dataset external_2025_pipe_0806 --iterations 2`
  - produced the full command for `run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py` with:
    - `--optimizer adamw`
    - `--diameter-seed-mm 12.0`
    - `--optimize-conductivity`
    - `--sample-start 42`
    - `--residual-mode profile_mean`

## Current decision
The current `0806` fitting path is now reproducible from a small recipe CLI instead of a manually reconstructed long command. This moves the deliverable closer to a real predictor workflow.

## What remains blocked
- The recipe CLI currently defines the current `0806` transfer recipe only.
- It does not automatically synthesize/update leaderboards after execution yet.
- `0701` is already a shipped card row but does not have a fresh rerun recipe encoded here.

## Artifact paths
- `run_field_prediction_fit_recipe.py`
- `tests/test_field_prediction_fit_recipe.py`
- Current card/query base:
  - `outputs/validation_exp_on_field_data/product_leaderboard/088_field_prediction_current_predictor_card_0806_sample_window_diameter_family_readable`

## Next defensible task
Extend the recipe layer into a small pipeline wrapper that can execute a recipe and immediately write a card-compatible prediction row or synthesis input, so future real-data runs are less manual.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
