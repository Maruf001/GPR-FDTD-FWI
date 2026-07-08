# 455 - 2026-07-05 - GSSI 51600S Joint Timing-Y Local Search Checkpoint

## Purpose

Test whether the GSSI 51600S 3D predictor should promote an earlier event window when it is combined with the best current nonuniform crossline-coordinate hypothesis, or whether timing should remain a conditioned uncertainty in the product output.

## Implementation

- Added `run_gssi51600s_joint_timing_y_local_search_card.py`.
- The card compares the current nonuniform-coordinate reference against nearby event-window and y-spacing candidates.
- The current prediction bundle now ingests the joint timing-y card and copies its figure into the product bundle.
- The compact product query now reports the joint timing-y decision fields.

## Field Runs

Short GPU fill runs completed for the missing joint timing-y candidates:

- `528_gssi51600s_finite_length_3d_profiles1_3_yexplicit_nonuniform_c015_a020_b020_early_windows46_50_54_58_62_iter6`
  - Objective: `0.980789303779602`
  - Diameter: `17.323631793260574` mm
  - Length: `0.18477179110050201` m
- `529_gssi51600s_finite_length_3d_profiles0_2_yexplicit_nonuniform_a021_b021_c014_early_windows46_50_54_58_62_iter6`
  - Objective: `0.9667410850524902`
  - Diameter: `17.294296994805336` mm
  - Length: `0.18317395448684692` m
- `530_gssi51600s_finite_length_3d_profiles1_3_yexplicit_nonuniform_a021_b021_c014_early_windows46_50_54_58_62_iter6`
  - Objective: `0.9807223081588745`
  - Diameter: `17.324093729257584` mm
  - Length: `0.18452388048171997` m

## Comparison

Joint timing-y card:

- Card output:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/193_gssi51600s_joint_timing_y_local_search_card_current`
- Selected candidate:
  - `early_46_50_54_58_62__a021_b021_c014`
- Best field-fit candidate:
  - `early_46_50_54_58_62__a021_b021_c014`
- Best cover-stability candidate:
  - `mid_50_54_58_62_66__seed_a020_b020_c014`
- Selected mean objective delta vs reference:
  - `-0.0043906569480896`
- Selected mean field-L1 delta vs reference:
  - `-0.0037717223167419434`
- Selected cover-depth gap delta vs reference:
  - `0.003209024667739868` m
- Selected cover-depth gap:
  - `0.015448838472366333` m
- Selected center-x gap:
  - `0.014102965593338013` m

## Current Decision

The early-window candidate improves waveform fit, but it increases the cover-depth gap between the overlapping profile subsets. It is therefore useful timing evidence but not a release default.

Current gate decision:

`early_window_improves_fit_but_increases_depth_gap_keep_timing_conditioned`

## Product Integration

- Current GSSI prediction bundle:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/194_gssi51600s_current_prediction_bundle_with_joint_timing_y_search`
- Bundle summary:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/194_gssi51600s_current_prediction_bundle_with_joint_timing_y_search/data/gssi51600s_current_prediction_bundle_summary.json`
- Latest pointer:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- User-facing query:
  - `python run_field_prediction_current_query.py --dataset gssi51600s --format pretty`
- The bundle includes frozen script snapshots, including the new timing-y card generator.

## Dataset Boundary

The current deliverable source remains `data/2026-06-09_GSSI_model_51600S`. The separate `data/2025-01-13_GPR_Dataset` archive remains out of the trusted GSSI rebar claim unless a future run explicitly targets and verifies one of its rebar branches.

## Validation

- Compile checks passed under `/home/lam002/miniforge3/bin/python`.
- Focused tests passed: `21 passed`.
- Broader GSSI/card suite passed: `162 passed`.
- `git diff --check` passed on touched files.
- Figure sanity:
  - Timing-y card figure: `(1974, 1481)`, nonblank RGBA range `0-255`.
  - Bundle timing-y figure copy: `(1974, 1481)`, nonblank RGBA range `0-255`.

## Next Defensible Task

Move to a source/time-alignment or y-dependent target-model branch rather than promoting the early timing window. The next product-relevant question is whether a physically explicit source-time correction or a compact y-dependent geometry parameterization can reduce both waveform error and profile-subset depth disagreement at the same time.

The marathon request remains active. Resumed active-session window: `2026-07-05 10:04 UTC` to approximately `2026-07-06 06:04 UTC`.
