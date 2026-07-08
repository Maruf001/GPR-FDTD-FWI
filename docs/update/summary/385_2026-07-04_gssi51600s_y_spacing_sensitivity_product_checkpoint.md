# GSSI51600S Y-Spacing Sensitivity Product Checkpoint

## What Changed

- Confirmed from the DZX metadata that the GSSI files provide along-scan spacing (`0.003333 m`) but do not provide measured crossline spacing between the four profile files.
- Generated alternate GSSI finite-length 3D seeds for assumed crossline spacings of `0.05`, `0.075`, `0.125`, `0.15`, and `0.16 m`, using the existing `0.10 m` run as the center reference.
- Ran the same AdamW finite-length 3D optimizer on each y-spacing seed and synthesized the ladder.
- Updated the product default chain to the y-spacing sensitivity candidate while preserving the release block on unconfirmed crossline geometry.

## Key Numbers

- Current trusted candidate: `gssi51600s`.
- Tested assumed y spacings: `0.05`, `0.075`, `0.10`, `0.125`, `0.15`, `0.16 m`.
- Best objective label: `y016`; best field-L1 label: `y015`.
- x position: `0.413941 m`.
- best tested assumed y center: `0.240000 m`.
- cover depth: about `0.120389 m`.
- all-best length range across the ladder: `0.183144-0.183513 m`.
- all-best diameter range across the ladder: `17.293125-17.294552 mm`.
- top-margin relative permittivity range: `2.012263-2.012795`.
- top-margin background conductivity range: `0.002658729-0.002659715 S/m`.
- current query status: `next_transfer_candidate`.
- release checklist failure: `crossline_y_geometry_confirmed` only.

## Current Decision

The y-spacing ladder strengthens the product claim for diameter, cover depth, and material estimates because those values stay stable while the assumed crossline spacing changes. It does not turn the y coordinate into metadata-confirmed geometry; the candidate remains blocked for release until crossline profile spacing is independently confirmed or a formal acquisition-geometry inversion policy is accepted.

## Validation

- `python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_gssi51600s_finite_length_seed.py tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_current_predictor_card.py tests/test_field_prediction_current_query.py tests/test_field_prediction_release_promotion_checklist.py tests/test_field_prediction_release_policy_variant.py tests/test_field_prediction_release_promotion_card.py tests/test_field_prediction_range_release_candidate_card.py tests/test_field_prediction_fit_recipe.py tests/test_field_prediction_workflow_command_pack.py tests/test_field_prediction_product_default_audit.py -q` passed with `65 passed`.
- `python -m py_compile` passed for the changed product, GSSI seed, optimizer, and synthesis scripts.
- `git diff --check` passed.

## Artifact Paths

- Y-spacing synthesis: `outputs/validation_exp_on_field_data/3d_geometry_inventory/392_gssi51600s_finite_length_3d_surface075_y_spacing_sensitivity_adamw_y016/`.
- Current transfer leaderboard: `outputs/validation_exp_on_field_data/product_leaderboard/193_field_prediction_transfer_leaderboard_gssi51600s_y_spacing_sensitivity_candidate_with_pipe_context/`.
- Current predictor card: `outputs/validation_exp_on_field_data/product_leaderboard/195_field_prediction_current_predictor_card_gssi51600s_y_spacing_sensitivity_candidate/`.
- Current release block: `outputs/validation_exp_on_field_data/product_leaderboard/196_field_prediction_release_promotion_checklist_gssi51600s_y_spacing_sensitivity_crossline_assumption_blocked/`.
- Current workflow command pack: `outputs/validation_exp_on_field_data/product_leaderboard/200_field_prediction_workflow_command_pack_gssi51600s_y_spacing_sensitivity_candidate/`.
- Current default audit: `outputs/validation_exp_on_field_data/product_leaderboard/201_field_prediction_product_default_audit_gssi51600s_y_spacing_sensitivity_candidate/`.

## Next Defensible Task

Run the same GSSI y-spacing candidate against adjacent sample windows or detector-rank windows to test whether the 17.29 mm diameter and 0.183 m length remain stable outside the current local event window.

The local marathon request remains active.
