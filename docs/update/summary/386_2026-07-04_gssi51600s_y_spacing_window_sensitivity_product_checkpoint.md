# GSSI51600S Y-Spacing And Window Sensitivity Product Checkpoint

## What Changed

- Added an adjacent-window GSSI check for the current `0.16 m` assumed y-spacing candidate using sample windows `54`, `58`, and `62`.
- Combined the earlier y-spacing ladder with the adjacent-window run into one current synthesis.
- Regenerated the product transfer leaderboard, current pointer, predictor card, strict release checklist, release card, range policy, range card, workflow command pack, and default audit from the combined sensitivity synthesis.
- Updated script defaults so the current query and workflow now resolve to this combined sensitivity candidate.

## Key Numbers

- Current trusted candidate: `gssi51600s`.
- Combined sensitivity run count: `7`.
- Tested assumed y spacings: `0.05`, `0.075`, `0.10`, `0.125`, `0.15`, `0.16 m`.
- Adjacent-window run: `0.16 m` assumed spacing with sample windows `54`, `58`, and `62`.
- Best objective label: `y016`; best field-L1 label: `y015`.
- x position: `0.413941 m`.
- best tested assumed y center: `0.240000 m`.
- cover depth: `0.120389 m`.
- all-best length range: `0.183144-0.183513 m`.
- all-best diameter range: `17.293125-17.295070 mm`.
- top-margin relative permittivity range: `2.012263-2.012795`.
- top-margin background conductivity range: `0.002658729-0.002659715 S/m`.
- current query status: `next_transfer_candidate`.
- release checklist failure: `crossline_y_geometry_confirmed` only.

## Current Decision

The GSSI candidate is now stable across optimizer family, assumed crossline spacing, and a nearby time-window check for the fitted diameter and finite length. The product claim remains release-blocked only because the absolute crossline y coordinate depends on unconfirmed profile spacing metadata.

## Validation

- `python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_gssi51600s_finite_length_seed.py tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_current_predictor_card.py tests/test_field_prediction_current_query.py tests/test_field_prediction_release_promotion_checklist.py tests/test_field_prediction_release_policy_variant.py tests/test_field_prediction_release_promotion_card.py tests/test_field_prediction_range_release_candidate_card.py tests/test_field_prediction_fit_recipe.py tests/test_field_prediction_workflow_command_pack.py tests/test_field_prediction_product_default_audit.py -q` passed with `65 passed`.
- `python -m py_compile` passed for the changed product, GSSI seed, optimizer, and synthesis scripts.
- `git diff --check` passed.

## Artifact Paths

- Combined sensitivity synthesis: `outputs/validation_exp_on_field_data/3d_geometry_inventory/395_gssi51600s_finite_length_3d_surface075_y_spacing_and_window_sensitivity_adamw/`.
- Current transfer leaderboard: `outputs/validation_exp_on_field_data/product_leaderboard/202_field_prediction_transfer_leaderboard_gssi51600s_y_spacing_window_sensitivity_candidate_with_pipe_context/`.
- Current predictor card: `outputs/validation_exp_on_field_data/product_leaderboard/204_field_prediction_current_predictor_card_gssi51600s_y_spacing_window_sensitivity_candidate/`.
- Current release block: `outputs/validation_exp_on_field_data/product_leaderboard/205_field_prediction_release_promotion_checklist_gssi51600s_y_spacing_window_sensitivity_crossline_assumption_blocked/`.
- Current workflow command pack: `outputs/validation_exp_on_field_data/product_leaderboard/209_field_prediction_workflow_command_pack_gssi51600s_y_spacing_window_sensitivity_candidate/`.
- Current default audit: `outputs/validation_exp_on_field_data/product_leaderboard/210_field_prediction_product_default_audit_gssi51600s_y_spacing_window_sensitivity_candidate/`.

## Next Defensible Task

Extend the current GSSI candidate to additional detector/event windows, then decide whether the same diameter and length range remains stable enough to present as the current field-data predictor with an explicit crossline-geometry caveat.

The local marathon request remains active.
