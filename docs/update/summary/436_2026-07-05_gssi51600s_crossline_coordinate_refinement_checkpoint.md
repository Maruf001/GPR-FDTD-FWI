# GSSI 51600S Crossline Coordinate Refinement Checkpoint

## What Changed

- Ran a bounded crossline-coordinate refinement around the current nonuniform coordinate seed for the trusted GSSI 51600S 3D field predictor.
- Tested nearby profile-coordinate candidates around:
  - profile 0-to-1 and profile 1-to-2 spacing: `0.19-0.21 m`
  - profile 2-to-3 spacing: `0.13-0.15 m`
- Added a refinement card that compares the joint mean objective loss across the profiles 0-2 and profiles 1-3 optimizer runs.
- Regenerated the latest prediction bundle and live query so they report the refinement decision and the best coordinate seed.
- Updated the Sunday daily update with the bounded refinement result.

## Key Numbers

- Refinement decision: `crossline_coordinate_refinement_seed_remains_best_keep_geometry_conditioned`.
- Best label: `seed_a020_b020_c014`.
- Best profile spacings: `0.20 m`, `0.20 m`, `0.14 m`.
- Best joint mean objective loss: `0.978122354`.
- Best joint length range: `0.183222517-0.184444651 m`.
- Best joint diameter range: `17.295185-17.317055 mm`.
- Near-best labels at tolerance `2.5e-05`:
  - `seed_a020_b020_c014`
  - `c015_a020_b020`
  - `a019_b019_c014`
  - `a021_b021_c014`
- `c013_a020_b020` was outside the near-best tolerance with mean loss delta `8.5324e-05`.

## Current Decision

The bounded refinement keeps the `0.20 m`, `0.20 m`, `0.14 m` nonuniform coordinate pattern as the current best optimizer-estimated seed. Nearby `0.19 m`, `0.21 m`, and `0.15 m` variants are close, so the product should still report y geometry as conditioned rather than measured.

## What Remains Blocked

- Crossline profile coordinates are still not measured metadata.
- The refinement is an outer coordinate search around the full AdamW geometry/material optimizer; it is not a differentiable y-coordinate inversion inside the Fast-GPR CUDA kernel.
- The public finite-length range should remain geometry-conditioned until measured coordinates or a stronger continuous-coordinate method confirms the y geometry.

## Next Defensible Task

Use the current best coordinate seed for a material/geometry robustness branch: rerun the best nonuniform coordinate candidate with a slightly longer optimizer budget or a second optimizer family only if it changes x, cover depth, diameter, relative permittivity, conductivity, or runtime enough to affect the product claim.

## Validation And Resource Checks

- `python -m pytest tests/test_field_prediction_current_query.py tests/test_gssi51600s_optimizer_family_card.py tests/test_gssi51600s_crossline_spacing_release_gate.py tests/test_gssi51600s_profile_position_ladder_card.py tests/test_gssi51600s_nonuniform_coordinate_synthesis_card.py tests/test_gssi51600s_nonuniform_coordinate_window_stability_card.py tests/test_gssi51600s_crossline_coordinate_estimator_card.py tests/test_gssi51600s_crossline_coordinate_refinement_card.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_runtime_benchmark_card.py tests/test_gssi51600s_nonuniform_geometry_run_planner.py -q`
- Result: 38 passed.
- `python -m py_compile run_field_prediction_current_query.py run_gssi51600s_optimizer_family_card.py run_gssi51600s_crossline_spacing_release_gate.py run_gssi51600s_profile_position_ladder_card.py run_gssi51600s_nonuniform_coordinate_synthesis_card.py run_gssi51600s_nonuniform_coordinate_window_stability_card.py run_gssi51600s_crossline_coordinate_estimator_card.py run_gssi51600s_crossline_coordinate_refinement_card.py run_gssi51600s_current_prediction_bundle.py`
- Result: passed.
- Figure sanity check for the refinement figure and bundle copy: both images are `1974 x 1243` pixels with grayscale extrema `(0, 255)`.
- `git diff --check` on touched scripts, tests, checkpoints, and daily update.
- Result: passed.

## Artifact Paths

- Refinement runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/488_gssi51600s_finite_length_3d_profiles1_3_refine_b020_c013_offsets_m020_0_013_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/489_gssi51600s_finite_length_3d_profiles1_3_refine_b020_c015_offsets_m020_0_015_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/490_gssi51600s_finite_length_3d_profiles0_2_refine_a019_b019_offsets_m019_0_019_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/491_gssi51600s_finite_length_3d_profiles1_3_refine_b019_c014_offsets_m019_0_014_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/492_gssi51600s_finite_length_3d_profiles0_2_refine_a021_b021_offsets_m021_0_021_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/493_gssi51600s_finite_length_3d_profiles1_3_refine_b021_c014_offsets_m021_0_014_domainz070_adamw_windows50_54_58_62_66_iter6`
- Refinement card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/153_gssi51600s_crossline_coordinate_refinement_card_current`
- Latest bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/154_gssi51600s_current_prediction_bundle_with_crossline_coordinate_refinement`
- Stable latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- Daily update: `docs/update/daily_update/2026-06-29_to_2026-07-05_daily_update.md`

## Marathon Status

The marathon request is still active. Continue with the next product-improving GSSI field-data branch rather than stopping at this checkpoint.
