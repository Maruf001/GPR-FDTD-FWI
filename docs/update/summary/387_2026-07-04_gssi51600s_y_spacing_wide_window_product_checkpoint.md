# GSSI51600S Y-Spacing Wide-Window Product Checkpoint

## What Changed

- Added a wider adjacent-window run for the current GSSI `0.16 m` assumed y-spacing candidate using sample windows `50`, `54`, `58`, `62`, and `66`.
- Combined the y-spacing ladder, the three-window check, and the five-window check into one current product synthesis.
- Regenerated and rewired the product transfer leaderboard, current pointer, predictor card, strict release checklist, release card, range policy, range card, workflow command pack, and default audit.

## Key Numbers

- Current trusted candidate: `gssi51600s`.
- Combined sensitivity run count: `8`.
- Best objective label: `y016`; best field-L1 label: `y015`.
- x position: `0.413941 m`.
- best tested assumed y center: `0.240000 m`.
- cover depth: `0.120389 m`.
- all-best length range: `0.183144-0.183513 m`.
- all-best diameter range: `17.293125-17.296124 mm`.
- top-margin diameter range: `17.294351-17.294552 mm`.
- top-margin relative permittivity range: `2.012263-2.012795`.
- top-margin background conductivity range: `0.002658729-0.002659715 S/m`.
- current query status: `next_transfer_candidate`.
- release checklist failure: `crossline_y_geometry_confirmed` only.

## Current Decision

The current GSSI field-data candidate is stable across optimizer family, crossline-spacing sensitivity, and widened event-window sensitivity for diameter and finite length. The only release block remains the unconfirmed crossline profile spacing, so the y coordinate is still assumption-conditioned.

## Validation

- `python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_gssi51600s_finite_length_seed.py tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_current_predictor_card.py tests/test_field_prediction_current_query.py tests/test_field_prediction_release_promotion_checklist.py tests/test_field_prediction_release_policy_variant.py tests/test_field_prediction_release_promotion_card.py tests/test_field_prediction_range_release_candidate_card.py tests/test_field_prediction_fit_recipe.py tests/test_field_prediction_workflow_command_pack.py tests/test_field_prediction_product_default_audit.py -q` passed with `65 passed`.
- `python -m py_compile` passed for the changed product, GSSI seed, optimizer, and synthesis scripts.
- `git diff --check` passed.

## Artifact Paths

- Wide-window synthesis: `outputs/validation_exp_on_field_data/3d_geometry_inventory/397_gssi51600s_finite_length_3d_surface075_y_spacing_and_window_sensitivity_adamw_wide/`.
- Current transfer leaderboard: `outputs/validation_exp_on_field_data/product_leaderboard/211_field_prediction_transfer_leaderboard_gssi51600s_y_spacing_wide_window_sensitivity_candidate_with_pipe_context/`.
- Current predictor card: `outputs/validation_exp_on_field_data/product_leaderboard/213_field_prediction_current_predictor_card_gssi51600s_y_spacing_wide_window_sensitivity_candidate/`.
- Current release block: `outputs/validation_exp_on_field_data/product_leaderboard/214_field_prediction_release_promotion_checklist_gssi51600s_y_spacing_wide_window_sensitivity_crossline_assumption_blocked/`.
- Current workflow command pack: `outputs/validation_exp_on_field_data/product_leaderboard/218_field_prediction_workflow_command_pack_gssi51600s_y_spacing_wide_window_sensitivity_candidate/`.
- Current default audit: `outputs/validation_exp_on_field_data/product_leaderboard/219_field_prediction_product_default_audit_gssi51600s_y_spacing_wide_window_sensitivity_candidate/`.

## Next Defensible Task

Extend the same wide-window product recipe to additional detector/event ranks from the GSSI surface detector so the current diameter and length estimate is not tied to one detector-ranked event.

The local marathon request remains active.
