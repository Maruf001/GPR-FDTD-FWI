# GSSI 51600S Optimizer Budget Stability Checkpoint

## What Changed

- Tested optimizer-budget sensitivity for the current trusted GSSI 51600S nonuniform coordinate seed.
- Ran paired profiles 0-2 and profiles 1-3 AdamW checks at `12` and `24` iterations, using the same best nonuniform coordinate pattern and field windows as the 6-iteration reference.
- Added an optimizer-budget stability card comparing 6-, 12-, and 24-iteration results.
- Regenerated the latest prediction bundle and live query so the product output reports the budget sensitivity before anyone promotes the smaller 24-iteration diameter/material values.
- Updated the Sunday daily update with the budget-stability finding.

## Key Numbers

- Budget-stability decision: `optimizer_budget_not_stable_keep_size_material_unpromoted`.
- Iteration budgets compared: `6`, `12`, `24`.
- Highest-budget best iteration status: both 24-iteration subset runs had their best loss at the final iteration.
- Mean objective-loss shift from 6 to 24 iterations: `-0.0270171`.
- Mean diameter shift from 6 to 24 iterations: `-3.9741 mm`.
- Mean length shift from 6 to 24 iterations: `-0.0415359 m`.
- Mean relative-permittivity shift from 6 to 24 iterations: `+0.0723312`.
- Mean background-conductivity shift from 6 to 24 iterations: `+0.00256784 S/m`.
- 24-iteration diameter range: `13.097299-13.566651 mm`.
- 24-iteration length range: `0.127579674-0.157015681 m`.
- 24-iteration relative-permittivity range: `1.939991-2.285640`.
- 24-iteration background-conductivity range: `0.00513203-0.00532355 S/m`.

## Current Decision

The longer optimizer budget improves waveform fit but keeps moving geometry and material parameters at the final iteration. The 24-iteration values are useful optimizer-conditioned diagnostics, but they should not replace the current public diameter/material estimate until a convergence or regularization rule stabilizes them.

## What Remains Blocked

- Diameter, length, relative permittivity, and conductivity are budget-sensitive under the current objective.
- The optimizer currently has weak priors on diameter/material tradeoffs, so longer AdamW runs can keep shrinking diameter and changing conductivity while improving the loss.
- The public product should keep the conservative range and clearly report budget sensitivity until a regularized or plateaued optimizer result is available.

## Next Defensible Task

Add a regularized or early-stopped optimizer branch for the best nonuniform coordinate seed. A good bounded next run is a diameter/length/material prior check that penalizes drift from the stable 6-iteration seed while measuring whether the field loss remains close to the 24-iteration fit.

## Validation And Resource Checks

- `python -m pytest tests/test_field_prediction_current_query.py tests/test_gssi51600s_optimizer_family_card.py tests/test_gssi51600s_crossline_spacing_release_gate.py tests/test_gssi51600s_profile_position_ladder_card.py tests/test_gssi51600s_nonuniform_coordinate_synthesis_card.py tests/test_gssi51600s_nonuniform_coordinate_window_stability_card.py tests/test_gssi51600s_crossline_coordinate_estimator_card.py tests/test_gssi51600s_crossline_coordinate_refinement_card.py tests/test_gssi51600s_optimizer_budget_stability_card.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_runtime_benchmark_card.py tests/test_gssi51600s_nonuniform_geometry_run_planner.py -q`
- Result: 41 passed.
- `python -m py_compile run_field_prediction_current_query.py run_gssi51600s_optimizer_family_card.py run_gssi51600s_crossline_spacing_release_gate.py run_gssi51600s_profile_position_ladder_card.py run_gssi51600s_nonuniform_coordinate_synthesis_card.py run_gssi51600s_nonuniform_coordinate_window_stability_card.py run_gssi51600s_crossline_coordinate_estimator_card.py run_gssi51600s_crossline_coordinate_refinement_card.py run_gssi51600s_optimizer_budget_stability_card.py run_gssi51600s_current_prediction_bundle.py`
- Result: passed.
- Figure sanity check for the budget-stability figure and bundle copy: both images are `1634 x 1515` pixels with grayscale extrema `(0, 255)`.
- `git diff --check` on touched scripts, tests, checkpoints, and daily update.
- Result: passed.

## Artifact Paths

- 12-iteration runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/494_gssi51600s_finite_length_3d_profiles0_2_best_nonuniform_a020_b020_domainz070_adamw_windows50_54_58_62_66_iter12`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/495_gssi51600s_finite_length_3d_profiles1_3_best_nonuniform_b020_c014_domainz070_adamw_windows50_54_58_62_66_iter12`
- 24-iteration runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/496_gssi51600s_finite_length_3d_profiles0_2_best_nonuniform_a020_b020_domainz070_adamw_windows50_54_58_62_66_iter24`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/497_gssi51600s_finite_length_3d_profiles1_3_best_nonuniform_b020_c014_domainz070_adamw_windows50_54_58_62_66_iter24`
- Optimizer-budget stability card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/155_gssi51600s_optimizer_budget_stability_card_current`
- Latest bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/156_gssi51600s_current_prediction_bundle_with_optimizer_budget_stability`
- Stable latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- Daily update: `docs/update/daily_update/2026-06-29_to_2026-07-05_daily_update.md`

## Marathon Status

The marathon request is still active. Continue with the next product-improving GSSI field-data branch rather than stopping at this checkpoint.
