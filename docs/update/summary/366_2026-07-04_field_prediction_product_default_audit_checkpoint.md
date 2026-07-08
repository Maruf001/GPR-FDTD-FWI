# Field Prediction Product Default Audit Checkpoint

## What changed
- Added `run_field_prediction_product_default_audit.py`, which checks current default artifact pointers used by the product scripts.
- Added tests:
  - `tests/test_field_prediction_product_default_audit.py`
- Generated:
  - `090_field_prediction_product_default_audit_current`

## Key numbers
- Default audit `090`:
  - decision `product_defaults_ready`
  - missing count `0`
  - transfer alignment `true`
  - transfer candidate datasets:
    - `external_2025_pipe_0806`
- Checked defaults:
  - current product pointer transfer leaderboard:
    - `085_field_prediction_transfer_leaderboard_with_0806_sample_window_diameter_family`
  - predictor card default pointer:
    - `086_field_prediction_current_product_pointer_with_0806_sample_window_diameter_family`
  - current query default card:
    - `088_field_prediction_current_predictor_card_0806_sample_window_diameter_family_readable`
  - workflow synthesis:
    - `321_field_3d_0806_transfer_combined_sample_window_diameter_seed_family`
  - fit recipe paths:
    - `263` 0806 stack NPZ
    - `263` 0806 stack rows
    - `306` 0806 sample-42 seed summary

## Current decision
The product defaults are internally consistent. The current query/card/pointer/fit recipe all resolve to existing artifacts and the current transfer candidate remains `external_2025_pipe_0806`.

## What remains blocked
- Default audit checks current files; it does not validate scientific promotion.
- The current workflow still needs explicit release-promotion criteria for turning `0806` from transfer candidate into shipped row.

## Validation/resource checks
- `python -m py_compile run_field_prediction_product_default_audit.py`: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_product_default_audit.py tests/test_field_prediction_workflow_command_pack.py tests/test_field_prediction_fit_recipe.py -q`: `6 passed`.
- `git diff --check` on default-audit branch files: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/product_leaderboard/090_field_prediction_product_default_audit_current`
- `outputs/validation_exp_on_field_data/product_leaderboard/090_field_prediction_product_default_audit_current/data/field_prediction_product_default_audit_summary.json`
- `run_field_prediction_product_default_audit.py`
- `tests/test_field_prediction_product_default_audit.py`

## Next defensible task
Define a concrete release-promotion checklist for `0806` that separates what is already satisfied from the exact remaining checks needed to move it from transfer candidate to shipped row.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
