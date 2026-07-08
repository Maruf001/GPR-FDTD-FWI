# Field Prediction Workflow Range-Release Wiring Checkpoint

## What changed
- Updated `run_field_prediction_workflow_command_pack.py` so the workflow command pack now includes:
  - strict unique-diameter release checklist refresh
  - bounded diameter-range release policy refresh
  - policy-conditional range-release card refresh
  - explicit query of `external_2025_pipe_0806` from the range-release card
- Updated `run_field_prediction_product_default_audit.py` so the product audit checks the release checklist, range policy, and range card defaults.
- Updated `run_field_prediction_current_query.py` so range-card queries expose `diameter_width_mm` and `range_release_policy_decision`.
- Updated focused tests for workflow, audit, and query behavior.
- Generated:
  - `094_field_prediction_workflow_command_pack_with_range_release_path`
  - `095_field_prediction_product_default_audit_with_range_release_path`

## Key numbers
- Workflow command pack `094`:
  - decision `workflow_command_pack_ready`
  - step count `11`
  - includes strict release and range-release paths
- Product default audit `095`:
  - decision `product_defaults_ready`
  - missing defaults `0`
  - transfer alignment `true`
  - range-policy alignment `true`
  - strict release decision `release_promotion_blocked`
  - range policy decision `range_release_policy_candidate`
  - range card decision `range_release_candidate_card_ready`
  - range-release candidate dataset `external_2025_pipe_0806`
- Range query now reports:
  - tier `policy_conditional_range_release_candidate`
  - diameter range `8.00037-13.9201 mm`
  - diameter width `5.9197 mm`
  - epsr `3.54531`
  - conductivity `0.00620269 S/m`

## Current decision
The current product path is now explicit: strict unique-diameter release still blocks `0806`, while range-release can expose `0806` as a bounded-uncertainty candidate.

## What remains blocked
- `0806` is not yet a unique-diameter release.
- Blocked transfer datasets still need source/window/geometry repair.
- The next accuracy work should target the real 3D fit ambiguity rather than making more product wrappers.

## Validation/resource checks
- `python -m py_compile run_field_prediction_workflow_command_pack.py run_field_prediction_product_default_audit.py run_field_prediction_current_query.py`: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_workflow_command_pack.py tests/test_field_prediction_product_default_audit.py tests/test_field_prediction_current_query.py tests/test_field_prediction_range_release_candidate_card.py tests/test_field_prediction_release_policy_variant.py -q`: `12 passed`.
- `git diff --check` on touched product workflow files: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/product_leaderboard/094_field_prediction_workflow_command_pack_with_range_release_path`
- `outputs/validation_exp_on_field_data/product_leaderboard/095_field_prediction_product_default_audit_with_range_release_path`
- `run_field_prediction_workflow_command_pack.py`
- `run_field_prediction_product_default_audit.py`
- `run_field_prediction_current_query.py`

## Next defensible task
Return to real 3D predictor improvement: run a bounded branch that can reduce ambiguity, preferably by adding source/time/polarity alignment or a multi-window objective to the current `0806` Fast-GPR/FWI path and comparing optimizer behavior.

## Marathon status
The requested 20-hour local marathon remains active. Continue with the next real-data predictor branch rather than stopping at this product checkpoint.
