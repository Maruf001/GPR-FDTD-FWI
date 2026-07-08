# Field 3D 0806 Negative-Polarity Top-Margin Checkpoint

## What changed
- Ran a corrected-polarity 3D Fast-GPR/FWI branch on real `external_2025_pipe_0806` field data.
- Runs generated:
  - `330_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_adamw_conductivity_diam12_polarity_neg_iter8`
  - `331_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_adamw_conductivity_diam08_polarity_neg_iter8`
  - `332_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_adamw_conductivity_diam16_polarity_neg_iter8`
- Added top-margin fields to `run_field_3d_0701_finite_length_optimizer_seed_stability.py`.
- Propagated top-margin fields through:
  - `run_field_prediction_transfer_leaderboard.py`
  - `run_field_prediction_current_product_pointer.py`
  - `run_field_prediction_current_predictor_card.py`
  - `run_field_prediction_current_query.py`
- Generated:
  - `334_field_3d_0806_transfer_polarity_neg_diameter_seed_family_top_margin`
  - `100_field_prediction_transfer_leaderboard_with_0806_polarity_neg_top_margin`
  - `101_field_prediction_current_product_pointer_with_0806_polarity_neg_top_margin`
  - `103_field_prediction_current_predictor_card_0806_polarity_neg_top_margin_width_readable`
  - `104_field_prediction_release_promotion_checklist_0806_polarity_neg_top_margin_current`

## Key numbers
- Previous best positive-polarity `0806` field L1: `0.7909555`.
- New best negative-polarity `0806` field L1: `0.7886795`.
- Best negative-polarity candidate:
  - label `0806_sample42_source10_adamw_conductivity_diam12_polarity_neg_iter8`
  - x/y/z `2.4576 / 0.35 / 1.93583 m`
  - broad tested length range `0.111206-0.129327 m`
  - broad tested diameter range `8.00174-18.19655 mm`
  - broad tested diameter width `10.19481 mm`
  - top-margin diameter range `13.91165-18.19655 mm`
  - top-margin diameter width `4.28490 mm`
  - top-margin length range `0.129307-0.129327 m`
  - top-margin status `top_margin_diameter_range_bounded`
  - background epsr `3.07325`
  - background conductivity `0.00224136 S/m`
- Negative-polarity seed losses:
  - diam08: `0.7896613` field L1
  - diam12: `0.7886795` field L1
  - diam16: `0.7887261` field L1

## Current decision
Negative polarity is a real improvement for the `0806` real-field objective. The product candidate should prefer the negative-polarity family over the previous positive-polarity family. The honest product output now reports both the broad tested diameter range and the tighter top-loss diameter range.

## What remains blocked
- Strict release promotion for `0806` remains blocked.
- `104` failed required checks:
  - `sample_window_confirmation_available`
  - `diameter_unique_enough_for_release`
  - `synthesis_decision_release_ready`
- The top-margin range is useful for a predictor output, but it is not yet a strict unique-diameter release claim.

## Validation/resource checks
- `python -m py_compile run_field_3d_0701_finite_length_optimizer_seed_stability.py run_field_prediction_transfer_leaderboard.py run_field_prediction_current_product_pointer.py run_field_prediction_current_predictor_card.py run_field_prediction_current_query.py`: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_current_predictor_card.py tests/test_field_prediction_current_query.py -q`: `21 passed`.
- Follow-up after width derivation:
  - focused py_compile passed.
  - focused pytest slice passed: `18 passed`.
- `git diff --check` on touched field/product files: passed.
- Generated figures for `330` and `334` opened successfully with nonzero dimensions.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/334_field_3d_0806_transfer_polarity_neg_diameter_seed_family_top_margin`
- `outputs/validation_exp_on_field_data/product_leaderboard/100_field_prediction_transfer_leaderboard_with_0806_polarity_neg_top_margin`
- `outputs/validation_exp_on_field_data/product_leaderboard/101_field_prediction_current_product_pointer_with_0806_polarity_neg_top_margin`
- `outputs/validation_exp_on_field_data/product_leaderboard/103_field_prediction_current_predictor_card_0806_polarity_neg_top_margin_width_readable`
- `outputs/validation_exp_on_field_data/product_leaderboard/104_field_prediction_release_promotion_checklist_0806_polarity_neg_top_margin_current`

## Next defensible task
Run negative-polarity sample-window confirmation on real `0806` data. Start with `sample38` using the same AdamW/conductivity/xz/material setup and then synthesize with `sample42`; if it holds, promote the negative-polarity candidate over the previous positive-polarity `0806` path.

## Marathon status
The requested 20-hour local marathon remains active. Continue with real-data predictor improvement rather than stopping here.
