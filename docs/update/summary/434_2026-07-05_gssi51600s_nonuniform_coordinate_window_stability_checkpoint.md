# GSSI 51600S Nonuniform Coordinate Window-Stability Checkpoint

## What Changed

- Continued the trusted GSSI 51600S 3D field-data predictor path.
- Tested the current nonuniform crossline coordinate hypothesis against the uniform `0.22 m` reference under shifted B-scan event windows.
- Ran the same AdamW inner 3D optimizer on:
  - center windows `50,54,58,62,66`
  - early windows `46,50,54,58,62`
  - late windows `54,58,62,66,70`
- Added a window-stability card that compares the nonuniform coordinate hypothesis with the uniform reference by window set and profile subset.
- Regenerated the latest current prediction bundle and live query so they report the window-stability result.
- Updated the Sunday daily update with the window-shift result.

## Key Numbers

- Window-stability decision: `nonuniform_coordinate_window_stability_mixed_keep_geometry_conditioned`.
- Nonuniform loss wins: `2/3` window comparisons.
- Center-window nonuniform minus uniform mean objective loss: `-1.5765e-05`.
- Early-window nonuniform minus uniform mean objective loss: `-7.2241e-05`.
- Late-window nonuniform minus uniform mean objective loss: `4.0025e-05`.
- All nonuniform tested windows remain on the short finite-length branch.
- Nonuniform length range across all tested windows: `0.183199838-0.184696078 m`.
- Nonuniform mean length across all tested windows: `0.184030583 m`.
- Nonuniform diameter range across all tested windows: `17.294310-17.324077 mm`.
- Nonuniform mean diameter across all tested windows: `17.306554 mm`.

## Current Decision

The nonuniform coordinate hypothesis remains a strong optimizer-estimated y-geometry seed because it wins two of three event-window comparisons and keeps every tested subset on the short branch. It is not promoted as measured y geometry because the late-window objective slightly favors the uniform `0.22 m` reference.

## What Remains Blocked

- Crossline profile coordinates are still optimizer-estimated rather than measured survey metadata.
- The Fast-GPR CUDA bridge samples source and receiver coordinates at integer grid indices, so the current profile-position search is a bounded outer coordinate search around a full AdamW inner fit, not a differentiable y-coordinate adjoint update.
- The product should keep the finite-length range geometry-conditioned until measured crossline coordinates or a stronger profile-coordinate optimizer confirms the y geometry.

## Next Defensible Task

Move from local profile-position checks to a product-facing coordinate estimator: build a compact y-coordinate candidate table that combines the profile-position ladder, window-stability comparison, and current uniform-spacing posterior, then use it to choose the next bounded profile-coordinate refinement or measured-coordinate intake path.

## Validation And Resource Checks

- `python -m pytest tests/test_field_prediction_current_query.py tests/test_gssi51600s_optimizer_family_card.py tests/test_gssi51600s_crossline_spacing_release_gate.py tests/test_gssi51600s_profile_position_ladder_card.py tests/test_gssi51600s_nonuniform_coordinate_synthesis_card.py tests/test_gssi51600s_nonuniform_coordinate_window_stability_card.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_runtime_benchmark_card.py tests/test_gssi51600s_nonuniform_geometry_run_planner.py -q`
- Result: 32 passed.
- `python -m py_compile run_field_prediction_current_query.py run_gssi51600s_optimizer_family_card.py run_gssi51600s_crossline_spacing_release_gate.py run_gssi51600s_profile_position_ladder_card.py run_gssi51600s_nonuniform_coordinate_synthesis_card.py run_gssi51600s_nonuniform_coordinate_window_stability_card.py run_gssi51600s_current_prediction_bundle.py`
- Result: passed.
- Figure sanity check for the regenerated window-stability figure and bundle copy: both images are `1855 x 1209` pixels with grayscale extrema `(0, 255)`.
- `git diff --check` on touched scripts, tests, prior checkpoint, and daily update.
- Result: passed.

## Artifact Paths

- Early-window runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/479_gssi51600s_finite_length_3d_profiles0_2_nonuniform_coord_candidate_offsets_m020_0_020_domainz070_adamw_windows46_50_54_58_62_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/480_gssi51600s_finite_length_3d_profiles1_3_nonuniform_coord_candidate_offsets_m020_0_014_domainz070_adamw_windows46_50_54_58_62_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/481_gssi51600s_finite_length_3d_profiles0_2_uniform_y022_domainz070_adamw_windows46_50_54_58_62_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/482_gssi51600s_finite_length_3d_profiles1_3_uniform_y022_domainz070_adamw_windows46_50_54_58_62_iter6`
- Late-window runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/483_gssi51600s_finite_length_3d_profiles0_2_nonuniform_coord_candidate_offsets_m020_0_020_domainz070_adamw_windows54_58_62_66_70_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/484_gssi51600s_finite_length_3d_profiles1_3_nonuniform_coord_candidate_offsets_m020_0_014_domainz070_adamw_windows54_58_62_66_70_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/485_gssi51600s_finite_length_3d_profiles0_2_uniform_y022_domainz070_adamw_windows54_58_62_66_70_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/486_gssi51600s_finite_length_3d_profiles1_3_uniform_y022_domainz070_adamw_windows54_58_62_66_70_iter6`
- Window-stability card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/149_gssi51600s_nonuniform_coordinate_window_stability_card_current`
- Latest bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/150_gssi51600s_current_prediction_bundle_with_nonuniform_window_stability`
- Stable latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- Daily update: `docs/update/daily_update/2026-06-29_to_2026-07-05_daily_update.md`

## Marathon Status

The marathon request is still active. Continue with the next product-improving GSSI field-data branch rather than stopping at this checkpoint.
