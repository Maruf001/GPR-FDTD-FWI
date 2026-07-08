# Field Prediction 0806 Release-Promoted Default Wiring Checkpoint

## What changed
- Updated the default `0806` fit recipe to reproduce the promoted real-field candidate:
  - joint sample windows `38,42`
  - AdamW
  - conductivity/material/xz/time-shift optimization
  - negative prediction polarity
- Updated default product pointers:
  - transfer leaderboard default -> `109`
  - current predictor card default pointer -> `110`
  - current query default card -> `113`
- Refreshed range-policy defaults to current release-ready artifacts:
  - range policy `116`
  - range card `117`
- Added `run_field_prediction_release_promotion_card.py` and tests.
- Generated:
  - `118_field_prediction_workflow_command_pack_0806_release_promoted_default_range_refreshed`
  - `119_field_prediction_product_default_audit_0806_release_promoted_default_range_refreshed`

## Key numbers
- Default query now returns:
  - dataset `external_2025_pipe_0806`
  - tier `release_promoted_candidate`
  - action `ship_as_promoted_field_prediction`
  - x/y/z `2.4576 / 0.35 / 1.80861 m`
  - length-y range `0.129203-0.129327 m`
  - diameter range `13.8965-13.9116 mm`
  - diameter width `0.01519 mm`
  - top-margin z-depth range `1.8035-1.80861 m`
  - epsr `3.07435`
  - conductivity `0.00223608 S/m`
  - field L1 loss `0.787964`
- Workflow command pack `118`:
  - decision `workflow_command_pack_ready`
  - step count `12`
  - current synthesis `340`
  - release-promotion card `113`
  - range policy/card `116/117`
- Product default audit `119`:
  - decision `product_defaults_ready`
  - missing count `0`
  - transfer alignment `true`
  - release-card alignment `true`
  - range-policy alignment `true`
  - strict release decision `release_promotion_ready`
  - release-promotion card decision `release_promotion_card_ready`
  - release-promoted dataset `external_2025_pipe_0806`

## Current decision
The default product path now points to the release-promoted `0806` real-field 3D predictor output. A user can query the promoted prediction directly without passing a custom card path.

## What remains blocked
- The promoted `0806` result is still scoped to the current field event/window family, not a universal detector.
- `0704` and `07011` remain blocked transfer datasets.
- Additional robustness work should test nearby windows, alternative profile stacks, and possibly the GSSI 51600S field data under the same release-promoted workflow.

## Validation/resource checks
- `python -m py_compile run_field_prediction_fit_recipe.py run_field_prediction_workflow_command_pack.py run_field_prediction_product_default_audit.py`: passed.
- `python -m py_compile run_field_prediction_release_policy_variant.py run_field_prediction_range_release_candidate_card.py run_field_prediction_workflow_command_pack.py run_field_prediction_product_default_audit.py`: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_fit_recipe.py tests/test_field_prediction_workflow_command_pack.py tests/test_field_prediction_product_default_audit.py tests/test_field_prediction_current_query.py tests/test_field_prediction_release_promotion_card.py tests/test_field_prediction_release_promotion_checklist.py -q`: `15 passed`.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_workflow_command_pack.py tests/test_field_prediction_product_default_audit.py tests/test_field_prediction_release_policy_variant.py tests/test_field_prediction_range_release_candidate_card.py tests/test_field_prediction_fit_recipe.py -q`: `10 passed`.
- `git diff --check` on touched product/default files: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/product_leaderboard/113_field_prediction_release_promotion_card_0806_joint_two_window_release_ready`
- `outputs/validation_exp_on_field_data/product_leaderboard/118_field_prediction_workflow_command_pack_0806_release_promoted_default_range_refreshed`
- `outputs/validation_exp_on_field_data/product_leaderboard/119_field_prediction_product_default_audit_0806_release_promoted_default_range_refreshed`
- `run_field_prediction_fit_recipe.py`
- `run_field_prediction_current_query.py`
- `run_field_prediction_workflow_command_pack.py`
- `run_field_prediction_product_default_audit.py`

## Next defensible task
Continue real-field robustness work using the release-promoted workflow: run another nearby window or dataset with the same negative-polarity joint-window recipe, or start repairing blocked transfer datasets `0704/07011`.

## Marathon status
The requested 20-hour local marathon remains active. Continue with real-data robustness rather than stopping here.
