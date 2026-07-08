# 449 - 2026-07-05 - GSSI 51600S Adjacent Middle-Depth Checkpoint

## Purpose

Fill the missing adjacent profile subset `profiles1_2` in the trusted GSSI 51600S 3D predictor so the current shallow/deep depth split can be interpreted as a profile-wise progression rather than only two overlapping three-profile branches.

## Field Run

- New run:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/517_gssi51600s_finite_length_3d_profiles1_2_uniform_y022_domainz070_adamw_prior_windows50_54_58_62_66_iter24`
- Result:
  - Best field L1: `1.0093930959701538`
  - Best objective: `1.0135642290115356`
  - Best x: `0.48996058106422424` m
  - Best cover depth: `0.14144419133663177` m
  - Best diameter: `17.30671152472496` mm
  - Best length: `0.18300974369049072` m
  - Best background epsr: `2.0441641807556152`
  - Best conductivity: `0.0026231405790895224` S/m

## Interpretation

- The new profiles 1-2 branch lands between the shallow and deep adjacent branches:
  - Shallow: `profiles0_1`, `profiles0_2`, depth about `0.0963-0.0977` m.
  - Middle/transition: `profiles1_2`, `profiles1_3`, depth about `0.1383-0.1414` m.
  - Deep: `profiles2_3`, depth about `0.1602` m.
- This supports keeping the GSSI 3D depth output conditioned on crossline geometry, transition-zone event content, or multiple nearby events.
- It does not overturn the depth-slope result: the slope test still does not justify a single tilted-bar release claim.

## Product Integration

- Updated `run_gssi51600s_adjacent_profile_depth_progression_card.py` to include `profiles1_2` and report middle-depth labels.
- New adjacent-depth card:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/178_gssi51600s_adjacent_profile_depth_progression_card_current`
  - Decision: `adjacent_profile_depth_progression_keep_3d_depth_conditioned`
- Updated current bundle:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/179_gssi51600s_current_prediction_bundle_with_adjacent_middle_depth_and_slope_gate`
  - Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- Current query now reports:
  - `adjacent_profile_middle_subset_labels: ['profiles1_2', 'profiles1_3']`
  - `adjacent_profile_middle_depth_range_m: [0.138297438621521, 0.14144419133663177]`
  - `depth_slope_candidate_decision: depth_slope_does_not_resolve_branch_ambiguity`

## Validation

- `python -m py_compile ...` passed for the touched scripts.
- Focused pytest suite: `67 passed`.
- `git diff --check` passed on the touched files.
- Figure sanity:
  - Adjacent profile depth progression: `(1804, 1175)`, nonblank RGBA.
  - Depth-slope candidate: `(1719, 1192)`, nonblank RGBA.

## Next Defensible Task

Use the transition-zone evidence to test a bounded multi-event or per-profile target model on the trusted GSSI scans. The immediate goal is to determine whether the middle/deep behavior is better explained by one target with y-dependent event content or by multiple nearby events.
