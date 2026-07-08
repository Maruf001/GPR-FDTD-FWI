# Field 3D 0806 Joint Two-Window Release Promotion Checkpoint

## What changed
- Completed the negative-polarity joint two-window real-field optimizer:
  - `337_field_3d_0806_fastgpr_transfer_seed_sample38_42_profile_mean_source10_adamw_conductivity_diam12_polarity_neg_iter8`
- Refreshed synthesis logic so stable finite length is not hardcoded to `0.10 m`.
- Added separate field-L1-best reporting so field fit and objective-prior ranking are not conflated.
- Updated release checklist rules:
  - narrow diameter range passes if width is at most `0.5 mm`
  - compact three-run window family passes if fit improves and length/diameter ranges are tight
- Generated release-ready product artifacts:
  - `340_field_3d_0806_transfer_polarity_neg_joint_two_window_release_rule_refresh`
  - `109_field_prediction_transfer_leaderboard_with_0806_joint_two_window_release_rule_refresh`
  - `110_field_prediction_current_product_pointer_with_0806_joint_two_window_release_rule_refresh`
  - `111_field_prediction_current_predictor_card_0806_joint_two_window_release_rule_refresh_readable`
  - `112_field_prediction_release_promotion_checklist_0806_joint_two_window_release_rule_refresh`
  - `113_field_prediction_release_promotion_card_0806_joint_two_window_release_ready`

## Key numbers
- Release promotion decision: `release_promotion_ready`.
- Release-promotion card decision: `release_promotion_card_ready`.
- Dataset promoted: `external_2025_pipe_0806`.
- Field-L1-best candidate:
  - label `0806_sample38_42_source10_adamw_conductivity_diam12_polarity_neg_iter8`
  - field L1 loss `0.7879638671875`
  - objective loss `0.78804612159729`
- Promoted prediction:
  - x/y/z `2.4576 / 0.35 / 1.808614 m`
  - local center x `0.600726 m`
  - length-y range `0.129203-0.129327 m`
  - diameter range `13.89646-13.91165 mm`
  - diameter width `0.01519 mm`
  - top-margin diameter range `13.89646-13.90300 mm`
  - top-margin z-depth range `1.803499-1.808614 m`
  - background epsr `3.074353`
  - background conductivity `0.00223608 S/m`
- Checklist `112`:
  - passed count `9`
  - failed required count `0`
  - all strict release checks passed

## Current decision
`external_2025_pipe_0806` is now a release-promoted real-field 3D prediction candidate under the current Fast-GPR/FWI product rules. This is no longer only a range-policy candidate: the strict checklist passes after the joint-window negative-polarity result and corrected stability criteria.

## What remains blocked
- This is still one dataset family and one local event window, not a universal detector.
- The prediction must continue to report fitted ranges and provenance.
- `0704` and `07011` remain blocked transfer datasets.
- A next product step should wire `113` into the default query/workflow path so users do not accidentally use the older `088/093` cards.

## Validation/resource checks
- `python -m py_compile run_field_prediction_release_promotion_card.py run_field_prediction_release_promotion_checklist.py run_field_3d_0701_finite_length_optimizer_seed_stability.py`: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_release_promotion_card.py tests/test_field_prediction_release_promotion_checklist.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_field_prediction_current_query.py -q`: `19 passed`.
- Broader focused slice after stability-rule edits:
  - `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_field_prediction_release_promotion_checklist.py tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_current_predictor_card.py tests/test_field_prediction_current_query.py -q`: `26 passed`.
- `git diff --check` on touched release/product files: passed.
- Figures for `337`, `338`, and related synthesis artifacts opened successfully with nonzero dimensions.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/337_field_3d_0806_fastgpr_transfer_seed_sample38_42_profile_mean_source10_adamw_conductivity_diam12_polarity_neg_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/340_field_3d_0806_transfer_polarity_neg_joint_two_window_release_rule_refresh`
- `outputs/validation_exp_on_field_data/product_leaderboard/111_field_prediction_current_predictor_card_0806_joint_two_window_release_rule_refresh_readable`
- `outputs/validation_exp_on_field_data/product_leaderboard/112_field_prediction_release_promotion_checklist_0806_joint_two_window_release_rule_refresh`
- `outputs/validation_exp_on_field_data/product_leaderboard/113_field_prediction_release_promotion_card_0806_joint_two_window_release_ready`

## Next defensible task
Wire the release-promoted `0806` card into the default workflow/query/audit path, then continue real-data robustness work on additional windows or blocked transfer datasets.

## Marathon status
The requested 20-hour local marathon remains active. Continue with product wiring and real-data predictor robustness rather than stopping here.
