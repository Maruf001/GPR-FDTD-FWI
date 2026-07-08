# GSSI51600S Detector-Window Sensitivity Product Checkpoint

## What Changed

- Built an alternate finite-length 3D seed from the earlier GSSI rank-3 surface product report (`047`) at the same assumed `0.16 m` crossline spacing.
- Ran the same five-window AdamW finite-length optimizer on that alternate seed.
- Combined the y-spacing ladder, current wide-window checks, and alternate detector-window seed into one product synthesis.
- Regenerated and rewired the product leaderboard, current pointer, predictor card, release checklist, release card, range policy, range card, workflow command pack, and product default audit.

## Key Numbers

- Current trusted candidate: `gssi51600s`.
- Combined sensitivity run count: `9`.
- Best objective label: `surface047_rank3_y016_windows50_54_58_62_66`.
- Best field-L1 label: `y015`.
- x position reported by current query: `0.414366 m`.
- assumed y center: `0.240000 m`.
- cover depth from field-L1 best: `0.120389 m`.
- all-best length range: `0.183144-0.183513 m`.
- all-best diameter range: `17.293125-17.296124 mm`.
- top-margin diameter range: `17.293379-17.296124 mm`.
- top-margin relative permittivity range: `2.011180-2.046360`.
- top-margin background conductivity range: `0.002658729-0.007476822 S/m`.
- current query status: `next_transfer_candidate`.
- release checklist failure: `crossline_y_geometry_confirmed` only.

## Current Decision

The current field-data geometry prediction is stable across optimizer family, assumed crossline spacing, nearby time windows, and a neighboring rank-3 detector-window seed. Diameter and finite length remain tightly bounded. Material parameters are more sensitive to the alternate detector-window seed, so relative permittivity and conductivity should be reported with the wider near-best range rather than as a single locked value.

## Validation

- `python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_gssi51600s_finite_length_seed.py tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_current_predictor_card.py tests/test_field_prediction_current_query.py tests/test_field_prediction_release_promotion_checklist.py tests/test_field_prediction_release_policy_variant.py tests/test_field_prediction_release_promotion_card.py tests/test_field_prediction_range_release_candidate_card.py tests/test_field_prediction_fit_recipe.py tests/test_field_prediction_workflow_command_pack.py tests/test_field_prediction_product_default_audit.py -q` passed with `65 passed`.
- `python -m py_compile` passed for the changed product, GSSI seed, optimizer, and synthesis scripts.
- `git diff --check` passed.

## Artifact Paths

- Detector-window synthesis: `outputs/validation_exp_on_field_data/3d_geometry_inventory/399_gssi51600s_finite_length_3d_surface075_surface047_y_spacing_window_sensitivity_adamw/`.
- Current transfer leaderboard: `outputs/validation_exp_on_field_data/product_leaderboard/220_field_prediction_transfer_leaderboard_gssi51600s_detector_window_sensitivity_candidate_with_pipe_context/`.
- Current predictor card: `outputs/validation_exp_on_field_data/product_leaderboard/222_field_prediction_current_predictor_card_gssi51600s_detector_window_sensitivity_candidate/`.
- Current release block: `outputs/validation_exp_on_field_data/product_leaderboard/223_field_prediction_release_promotion_checklist_gssi51600s_detector_window_sensitivity_crossline_assumption_blocked/`.
- Current workflow command pack: `outputs/validation_exp_on_field_data/product_leaderboard/227_field_prediction_workflow_command_pack_gssi51600s_detector_window_sensitivity_candidate/`.
- Current default audit: `outputs/validation_exp_on_field_data/product_leaderboard/228_field_prediction_product_default_audit_gssi51600s_detector_window_sensitivity_candidate/`.

## Next Defensible Task

Either resolve the GSSI crossline profile spacing from external acquisition notes or add a formal y-geometry policy that reports the y coordinate as an estimated/acquisition-calibrated parameter instead of metadata-confirmed geometry.

The local marathon request remains active.
