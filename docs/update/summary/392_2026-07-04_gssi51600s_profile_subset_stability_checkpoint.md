# GSSI51600S Profile-Window Subset Stability Checkpoint

## What Changed

- Built two additional trusted GSSI finite-length seeds from the same surface candidate:
  - profiles `0-2` at assumed crossline spacing `0.16 m`.
  - profiles `1-3` at assumed crossline spacing `0.16 m`.
- Built three adjacent pair seeds:
  - profiles `0-1`, `1-2`, and `2-3` at assumed crossline spacing `0.16 m`.
- Ran the same five-window AdamW joint optimizer used by the current GSSI product path on all five profile subsets.
- Synthesized the full four-profile run plus the two three-profile subset runs and three adjacent pair runs.
- Added single-window and three-window runs for the two near-best three-profile subsets, `0-2` and `1-3`.
- Synthesized the two near-best profile subsets across single, three-window, and five-window objectives.
- Regenerated the product chain so default queries now reflect the stricter profile-subset stability result.

## Key Numbers

- Active profile-window subset synthesis: `outputs/validation_exp_on_field_data/3d_geometry_inventory/414_gssi51600s_finite_length_3d_profiles0_2_vs1_3_window_subset_stability_adamw_y016/`.
- Decision: `finite_length_seed_stability_inconclusive`.
- Diameter range across near-best profile-window subsets: `17.295353-17.812613 mm`.
- Length range across near-best profile-window subsets: `0.183166-0.216163 m`.
- Diameter status: `diameter_gradient_available`.
- Length status: `finite_length_seed_sensitive`.
- Best subset label: `profiles0_2_single58`.
- Best subset fit field L1: `0.952720`.
- Best subset x/y/z: `0.413941 / 0.160000 / 0.120349 m`.
- Best subset epsr/conductivity: `1.979127 / 0.002662489 S/m`.
- Adjacent profile pairs all stayed near the shorter length:
  - `0-1`: length `0.183148 m`, diameter `17.299611 mm`.
  - `1-2`: length `0.183151 m`, diameter `17.298203 mm`.
  - `2-3`: length `0.183172 m`, diameter `17.306559 mm`.
- Profile `0-2` is window-stable around length `0.183166-0.183175 m` and diameter `17.295353-17.295782 mm`.
- Profile `1-3` is window-stable around length `0.209991-0.216163 m`; its single-window fit raises the conservative diameter range to `17.812613 mm`.

## Current Decision

The current GSSI product state is now `transfer_needs_confirmation`, not release-ready. The best local profile-window fit remains stable near a 17.3 mm diameter and 0.183 m length, but the conservative range is wider because the profile `1-3` subset is internally stable at a longer length and one single-window fit prefers a larger diameter. Finite length and y position remain assumption-conditioned because profile spacing is not metadata-confirmed.

## Product Artifacts

- Transfer leaderboard: `outputs/validation_exp_on_field_data/product_leaderboard/254_field_prediction_transfer_leaderboard_gssi51600s_profile_window_subset_stability_candidate_with_pipe_context/`.
- Product pointer: `outputs/validation_exp_on_field_data/product_leaderboard/255_field_prediction_current_product_pointer_gssi51600s_profile_window_subset_stability_needs_confirmation/`.
- Predictor card: `outputs/validation_exp_on_field_data/product_leaderboard/256_field_prediction_current_predictor_card_gssi51600s_profile_window_subset_stability_needs_confirmation/`.
- Strict checklist: `outputs/validation_exp_on_field_data/product_leaderboard/257_field_prediction_release_promotion_checklist_gssi51600s_profile_window_subset_stability_blocked/`.
- Release card: `outputs/validation_exp_on_field_data/product_leaderboard/258_field_prediction_release_promotion_card_gssi51600s_profile_window_subset_stability_blocked/`.
- Assumption-conditioned range policy/card: `260` and `261`, both blocked under the stricter evidence.
- Advisor table: `outputs/validation_exp_on_field_data/product_leaderboard/262_field_prediction_advisor_prediction_table_gssi51600s_profile_window_subset_stability_blocked/`.
- Workflow/default audit: `263` and `264`.

## Validation

- `python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_gssi51600s_finite_length_seed.py tests/test_gssi51600s_crossline_spacing_provenance_audit.py tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_current_predictor_card.py tests/test_field_prediction_current_query.py tests/test_field_prediction_release_promotion_checklist.py tests/test_field_prediction_release_policy_variant.py tests/test_field_prediction_release_promotion_card.py tests/test_field_prediction_range_release_candidate_card.py tests/test_field_prediction_fit_recipe.py tests/test_field_prediction_workflow_command_pack.py tests/test_field_prediction_product_default_audit.py tests/test_field_prediction_advisor_prediction_table.py -q` passed with `71 passed`.
- `python -m py_compile ...` passed for the touched product and optimizer scripts.
- `git diff --check` passed.

## Next Defensible Task

Run additional acquisition-geometry checks to explain the two stable profile-window explanations, and keep searching for acquisition information that confirms or replaces the assumed crossline spacing.

The local marathon request remains active.
