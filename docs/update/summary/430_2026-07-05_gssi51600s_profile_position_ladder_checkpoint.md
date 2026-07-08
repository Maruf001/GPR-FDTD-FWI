# GSSI 51600S Profile-Position Ladder Checkpoint

## What Changed

- Ran four new profiles 1-3 nonuniform profile-offset optimizer checks on the trusted GSSI 51600S field objective:
  - profile 3 outward: offsets `[-0.16, 0.00, 0.20]`
  - profile 3 inward: offsets `[-0.16, 0.00, 0.12]`
  - profile 1 outward: offsets `[-0.20, 0.00, 0.16]`
  - profile 1 inward: offsets `[-0.12, 0.00, 0.16]`
- Added a profile-position ladder card that compares those nonuniform runs against the existing uniform profiles 1-3 spacing runs.
- Regenerated the latest GSSI prediction bundle so the stable latest pointer includes the profile-position ladder decision.
- Updated the live current-prediction query so the GSSI output reports the best nonuniform profile-position candidate directly.
- Updated the Sunday daily note with the profile-position ladder result.

## Key Numbers

- Profile-position ladder decision: `nonuniform_profile_position_matches_short_branch_near_best_uniform_still_best`.
- Best overall run in this ladder: uniform `0.28 m` spacing, loss `0.9786202908`, length `0.183611 m`.
- Best nonuniform run: `profile1_outward`, loss delta `7.8678e-06`, length `0.184807 m`.
- `profile3_outward` stayed on the long branch with length `0.217030 m` and loss `0.979216`.
- `profile3_inward` moved short with length `0.183958 m` but worse loss `0.980894`.
- `profile1_inward` was much worse, with loss `0.994401` and length `0.197398 m`.

## Current Decision

The sparse nonuniform ladder supports the next geometry task: a bounded individual-profile-position optimizer. It does not justify collapsing the finite-length range yet, but it shows that nonuniform endpoint movement can reproduce the short branch with near-best loss.

## What Remains Blocked

- The profile y coordinates are still not measured metadata.
- The ladder only perturbs endpoint offsets by a few hand-selected cases; it is not a full profile-position inversion.
- Finite length should remain geometry-conditioned until either measured profile positions or a denser bounded profile-position optimizer confirms a stable solution.

## Next Defensible Task

Implement or run a bounded individual-profile-position optimizer over profiles 1-3, initialized around the `profile1_outward` near-best case, while keeping profile ordering and physically plausible spacing bounds.

## Validation And Resource Checks

- `python -m pytest tests/test_field_prediction_current_query.py tests/test_gssi51600s_optimizer_family_card.py tests/test_gssi51600s_crossline_spacing_release_gate.py tests/test_gssi51600s_profile_position_ladder_card.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_runtime_benchmark_card.py tests/test_gssi51600s_nonuniform_geometry_run_planner.py -q`
- Result: 28 passed.
- `python -m py_compile run_field_prediction_current_query.py run_gssi51600s_optimizer_family_card.py run_gssi51600s_crossline_spacing_release_gate.py run_gssi51600s_profile_position_ladder_card.py run_gssi51600s_current_prediction_bundle.py`
- Result: passed.
- `git diff --check` on touched scripts, tests, checkpoints, and daily update.
- Result: passed.

## Artifact Paths

- Nonuniform optimizer runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/467_gssi51600s_finite_length_3d_profiles1_3_profile3_outward_offsets_m016_0_020_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/468_gssi51600s_finite_length_3d_profiles1_3_profile3_inward_offsets_m016_0_012_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/469_gssi51600s_finite_length_3d_profiles1_3_profile1_outward_offsets_m020_0_016_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/470_gssi51600s_finite_length_3d_profiles1_3_profile1_inward_offsets_m012_0_016_domainz070_adamw_windows50_54_58_62_66_iter6`
- Profile-position ladder card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/141_gssi51600s_profile_position_ladder_card_current`
- Latest bundle with profile-position ladder: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/142_gssi51600s_current_prediction_bundle_with_profile_position_ladder`
- Stable latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`

## Marathon Status

The marathon request is still active. Continue with the next product-improving GSSI field-data branch rather than stopping at this checkpoint.
