# Field Prediction 0806 Three-Window Robustness Default Checkpoint

## What changed
- Completed a right-side nearby-window robustness run:
  - `343_field_3d_0806_fastgpr_transfer_seed_sample40_44_profile_mean_source10_adamw_conductivity_diam12_polarity_neg_iter8`
- Combined the left, promoted, and right window pairs into a three-window robustness synthesis:
  - `344_field_3d_0806_transfer_polarity_neg_joint_window_robustness_36_40_38_42_40_44`
- Refreshed product artifacts against `344`:
  - transfer leaderboard `120`
  - current product pointer `121`
  - predictor card `122`
  - strict release checklist `123`
  - release-promotion card `124`
  - range policy `125`
  - range card `126`
  - workflow command pack `127`
  - product default audit `128`
- Updated default script pointers so the normal current query uses release card `124`.

## Key numbers
- Right-side window optimizer `343`:
  - field L1 loss `0.7883678674697876`
  - objective loss `0.7886676788330078`
  - loss improvement `0.0030088424682617188`
  - diameter `13.903201 mm`
  - length-y `0.12922986 m`
  - depth `1.813097 m`
  - epsr `3.073339`
  - conductivity `0.00223775 S/m`
  - runtime `12.38 s`
- Three-window synthesis `344`:
  - decision `finite_length_joint_xz_material_stability_supports_length_and_diameter`
  - run count `3`
  - field-L1-best label `0806_sample38_42_source10_adamw_conductivity_diam12_polarity_neg_iter8`
  - field-L1-best loss `0.7879638671875`
  - near-best diameter range `13.893931-13.903201 mm`
  - near-best length-y range `0.129125-0.129270 m`
  - near-best depth range `1.802372-1.813097 m`
  - near-best epsr range `3.073339-3.074353`
  - near-best conductivity range `0.00223608-0.00223775 S/m`
- Default query now returns for `external_2025_pipe_0806`:
  - tier `release_promoted_candidate`
  - action `ship_as_promoted_field_prediction`
  - x/y/z `2.4576 / 0.35 / 1.80861 m`
  - length-y range `0.129125-0.129270 m`
  - diameter range `13.8939-13.9032 mm`
  - diameter width `0.00926945 mm`
  - epsr `3.07435`
  - conductivity `0.00223608 S/m`
  - field L1 loss `0.787964`

## Current decision
The product default now points at the three-window robustness release card. This keeps the same best field fit but reports a more defensible robustness-backed range for diameter, length, depth, epsr, and conductivity.

## What remains blocked
- The `0806` prediction is still one real-field event family, not a universal detector.
- `0704` and `07011` remain blocked transfer datasets.
- More product work should test the same workflow on another field profile/dataset and benchmark optimizer variants only when they improve the real prediction path.

## Validation/resource checks
- `python -m py_compile run_field_prediction_current_product_pointer.py run_field_prediction_current_predictor_card.py run_field_prediction_current_query.py run_field_prediction_release_promotion_checklist.py run_field_prediction_release_promotion_card.py run_field_prediction_release_policy_variant.py run_field_prediction_range_release_candidate_card.py run_field_prediction_workflow_command_pack.py run_field_prediction_product_default_audit.py`: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_workflow_command_pack.py tests/test_field_prediction_product_default_audit.py tests/test_field_prediction_current_query.py tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_current_predictor_card.py tests/test_field_prediction_release_promotion_checklist.py tests/test_field_prediction_release_promotion_card.py tests/test_field_prediction_release_policy_variant.py tests/test_field_prediction_range_release_candidate_card.py -q`: `23 passed`.
- `git diff --check` on touched product/default scripts and checkpoint: passed.
- Figures for `343`, `344`, and `120` opened successfully with nonzero dimensions.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/343_field_3d_0806_fastgpr_transfer_seed_sample40_44_profile_mean_source10_adamw_conductivity_diam12_polarity_neg_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/344_field_3d_0806_transfer_polarity_neg_joint_window_robustness_36_40_38_42_40_44`
- `outputs/validation_exp_on_field_data/product_leaderboard/124_field_prediction_release_promotion_card_0806_three_window_robustness_ready`
- `outputs/validation_exp_on_field_data/product_leaderboard/127_field_prediction_workflow_command_pack_0806_three_window_robustness_default`
- `outputs/validation_exp_on_field_data/product_leaderboard/128_field_prediction_product_default_audit_0806_three_window_robustness_default`

## Next defensible task
Apply the same product workflow to another real field stack/profile or repair a blocked transfer dataset, while keeping the current default query on the three-window robustness `0806` release card.

## Marathon status
The requested local marathon remains active. Continue with real-data prediction/product robustness, not synthetic detours.
