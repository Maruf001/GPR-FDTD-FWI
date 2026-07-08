# GSSI 51600S Profile-Position Local Search Checkpoint

## What Changed

- Continued the profiles 1-3 profile-position branch with four denser local-search geometries around the previous `profile1_outward` near-best case:
  - `[-0.18, 0.00, 0.16]`
  - `[-0.22, 0.00, 0.16]`
  - `[-0.20, 0.00, 0.14]`
  - `[-0.20, 0.00, 0.18]`
- Regenerated the profile-position ladder card with both the sparse endpoint perturbations and the denser local-search rows.
- Regenerated the latest GSSI prediction bundle so the stable latest pointer reports the local-search profile-position result.
- Updated the live current-prediction query and Sunday daily note with the new profile-position decision.

## Key Numbers

- Updated profile-position decision: `nonuniform_profile_position_short_branch_is_best_candidate_needs_confirmation`.
- Best local-search geometry for profiles 1-3: `[-0.20, 0.00, 0.14]`.
- Best local-search objective loss: `0.9785882831`.
- Best local-search finite length: `0.184445 m`.
- Best local-search diameter: `17.317055 mm`.
- This best nonuniform case is lower loss than the previous best uniform profiles 1-3 spacing row in the ladder.

## Current Decision

The GSSI profiles 1-3 long-branch ambiguity is now better explained by individual profile-position uncertainty than by a single uniform spacing value. The current result should not be called measured geometry, but it is strong enough to make bounded profile-position optimization the next product path.

## What Remains Blocked

- Profile y coordinates remain unmeasured.
- The local search is still sparse and uses fixed candidate offsets with inner AdamW optimization, not a continuous differentiable profile-position inversion.
- The full 3D finite-length range should remain geometry-conditioned until this profile-position result is confirmed across both overlapping profile subsets.

## Next Defensible Task

Build a denser profile-position synthesis across both overlapping profile subsets, using the current best profiles 1-3 nonuniform geometry as a seed and checking whether profiles 0-2 stays stable under compatible nonuniform coordinate assumptions.

## Validation And Resource Checks

- `python -m pytest tests/test_field_prediction_current_query.py tests/test_gssi51600s_optimizer_family_card.py tests/test_gssi51600s_crossline_spacing_release_gate.py tests/test_gssi51600s_profile_position_ladder_card.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_runtime_benchmark_card.py tests/test_gssi51600s_nonuniform_geometry_run_planner.py -q`
- Result: 28 passed.
- `python -m py_compile run_field_prediction_current_query.py run_gssi51600s_optimizer_family_card.py run_gssi51600s_crossline_spacing_release_gate.py run_gssi51600s_profile_position_ladder_card.py run_gssi51600s_current_prediction_bundle.py`
- Result: passed.
- `git diff --check` on touched scripts, tests, checkpoints, and daily update.
- Result: passed.

## Artifact Paths

- New local-search optimizer runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/471_gssi51600s_finite_length_3d_profiles1_3_profile1_outward_left018_offsets_m018_0_016_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/472_gssi51600s_finite_length_3d_profiles1_3_profile1_outward_left022_offsets_m022_0_016_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/473_gssi51600s_finite_length_3d_profiles1_3_profile1_outward_right014_offsets_m020_0_014_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/474_gssi51600s_finite_length_3d_profiles1_3_profile1_outward_right018_offsets_m020_0_018_domainz070_adamw_windows50_54_58_62_66_iter6`
- Updated profile-position ladder card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/143_gssi51600s_profile_position_ladder_card_current`
- Latest bundle with local-search result: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/144_gssi51600s_current_prediction_bundle_with_profile_position_local_search`
- Stable latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`

## Marathon Status

The marathon request is still active. Continue with the next product-improving GSSI field-data branch rather than stopping at this checkpoint.
