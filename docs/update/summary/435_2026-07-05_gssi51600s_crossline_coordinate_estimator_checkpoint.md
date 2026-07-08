# GSSI 51600S Crossline Coordinate Estimator Checkpoint

## What Changed

- Added a product-facing crossline coordinate estimator for the trusted GSSI 51600S field-data predictor.
- Combined the current evidence from:
  - nonuniform coordinate synthesis
  - nonuniform coordinate window-stability comparison
  - profile-position local-search ladder
  - joint uniform-spacing posterior
  - crossline spacing release gate
- Ranked the nonuniform coordinate candidate against the uniform `0.22 m` reference using the window-stability optimizer rows.
- Regenerated the latest prediction bundle and live query so they report the estimator decision, recommended y-coordinate seed, seed length range, seed diameter range, and release-geometry status.
- Updated the Sunday daily update with the estimator result.

## Key Numbers

- Coordinate estimator decision: `crossline_coordinate_estimator_prefers_nonuniform_seed_keep_geometry_conditioned`.
- Recommended seed label: `nonuniform_candidate`.
- Release geometry label: `null`.
- Nonuniform mean objective loss across tested windows: `0.978732139`.
- Uniform `0.22 m` reference mean objective loss across tested windows: `0.978748133`.
- Nonuniform loss delta vs uniform across tested windows: `-1.5994e-05`.
- Window-stability loss wins: `2/3`.
- Recommended seed profile coordinates, relative to profile 1:
  - profile 0: `-0.20 m`
  - profile 1: `0.00 m`
  - profile 2: `0.20 m`
  - profile 3: `0.34 m`
- Recommended seed profile spacings: `0.20 m`, `0.20 m`, `0.14 m`.
- Recommended seed length range: `0.183199838-0.184696078 m`.
- Recommended seed diameter range: `17.294310-17.324077 mm`.

## Current Decision

The estimator recommends the nonuniform coordinate pattern as the next seed for profile-coordinate refinement because it has the best aggregate objective loss across the current window-stability rows. It does not promote a single release y geometry because the late-window comparison slightly favors the uniform reference and the crossline profile coordinates are still not measured.

## What Remains Blocked

- Measured crossline profile coordinates are still unavailable in the GSSI metadata inspected so far.
- The current coordinate estimator is an evidence-combining product layer; it does not make Fast-GPR source/receiver y positions differentiable.
- The public finite-length range remains geometry-conditioned until measured profile coordinates or a stronger profile-coordinate optimizer confirms the y geometry.

## Next Defensible Task

Use the estimator output as the seed for the next bounded profile-coordinate refinement. A practical next branch is to run a small candidate set around profile 2-to-3 spacing `0.13-0.15 m` and profile 0-to-1/profile 1-to-2 spacing `0.19-0.21 m`, while keeping the same AdamW inner optimizer and reporting runtime.

## Validation And Resource Checks

- `python -m pytest tests/test_field_prediction_current_query.py tests/test_gssi51600s_optimizer_family_card.py tests/test_gssi51600s_crossline_spacing_release_gate.py tests/test_gssi51600s_profile_position_ladder_card.py tests/test_gssi51600s_nonuniform_coordinate_synthesis_card.py tests/test_gssi51600s_nonuniform_coordinate_window_stability_card.py tests/test_gssi51600s_crossline_coordinate_estimator_card.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_runtime_benchmark_card.py tests/test_gssi51600s_nonuniform_geometry_run_planner.py -q`
- Result: 35 passed.
- `python -m py_compile run_field_prediction_current_query.py run_gssi51600s_optimizer_family_card.py run_gssi51600s_crossline_spacing_release_gate.py run_gssi51600s_profile_position_ladder_card.py run_gssi51600s_nonuniform_coordinate_synthesis_card.py run_gssi51600s_nonuniform_coordinate_window_stability_card.py run_gssi51600s_crossline_coordinate_estimator_card.py run_gssi51600s_current_prediction_bundle.py`
- Result: passed.
- Figure sanity check for the estimator figure and bundle copy: both images are `1889 x 801` pixels with grayscale extrema `(0, 255)`.
- `git diff --check` on touched scripts, tests, checkpoints, and daily update.
- Result: passed.

## Artifact Paths

- Crossline coordinate estimator card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/151_gssi51600s_crossline_coordinate_estimator_card_current`
- Latest bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/152_gssi51600s_current_prediction_bundle_with_crossline_coordinate_estimator`
- Stable latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- Daily update: `docs/update/daily_update/2026-06-29_to_2026-07-05_daily_update.md`

## Marathon Status

The marathon request is still active. Continue with the next product-improving GSSI field-data branch rather than stopping at this checkpoint.
