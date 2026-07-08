# GSSI51600S 3D Candidate Default Product Checkpoint

## What Changed

- Confirmed the 2025 public dataset runs used the `pipe` subset, so those rows are now treated as pipe/cylindrical-target optimizer context, not rebar product evidence.
- Promoted the trusted GSSI 51600S finite-length 3D fit into the current product default chain while keeping release promotion blocked until crossline y geometry is confirmed.
- Updated default product pointers, the current fit recipe, workflow command pack, product default audit, release checklist defaults, release card defaults, range-policy defaults, and query defaults to use the GSSI candidate path.
- Added a current GSSI fit recipe for the seed-078 finite-length 3D AdamW optimizer run.
- Updated the weekly daily note with the corrected field-data provenance and GSSI result.

## Key Numbers

- Current trusted candidate: `gssi51600s`.
- x position: `0.413941 m`.
- assumed y center: `0.150000 m`; y spacing assumption: `0.100000 m`.
- cover depth: `0.120391 m`.
- finite length range: `0.183083-0.184512 m`.
- diameter range: `17.291531-17.346017 mm`.
- relative permittivity range: `2.009856-2.015488`.
- background conductivity range: `0.002640786-0.002660886 S/m`.
- optimizer family: AdamW, Adam, and Adamax stable for the same 0.10 m assumed y spacing.
- default product audit: `product_defaults_ready`.
- release checklist: blocked only by `crossline_y_geometry_confirmed`.

## Current Decision

The real-data product path is now GSSI-first. The 2025 pipe-subset experiments remain useful for optimizer benchmarking, but they are explicitly excluded from rebar product claims. The GSSI 3D candidate is the strongest current predictor output, but it is not release-promoted until the crossline y geometry assumption is resolved.

## Validation

- `python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_gssi51600s_finite_length_seed.py tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_current_predictor_card.py tests/test_field_prediction_current_query.py tests/test_field_prediction_release_promotion_checklist.py tests/test_field_prediction_release_policy_variant.py tests/test_field_prediction_release_promotion_card.py tests/test_field_prediction_range_release_candidate_card.py tests/test_field_prediction_fit_recipe.py tests/test_field_prediction_workflow_command_pack.py tests/test_field_prediction_product_default_audit.py -q` passed with `65 passed`.
- `python -m py_compile` passed for the changed product and GSSI scripts.
- `git diff --check` passed.

## Artifact Paths

- Current synthesis: `outputs/validation_exp_on_field_data/3d_geometry_inventory/385_gssi51600s_finite_length_3d_surface075_seed078_y010_optimizer_family_synthesis/`.
- Current transfer leaderboard: `outputs/validation_exp_on_field_data/product_leaderboard/184_field_prediction_transfer_leaderboard_gssi51600s_3d_y010_candidate_with_pipe_context/`.
- Current predictor card: `outputs/validation_exp_on_field_data/product_leaderboard/186_field_prediction_current_predictor_card_gssi51600s_3d_y010_candidate_with_pipe_context/`.
- Current release block: `outputs/validation_exp_on_field_data/product_leaderboard/187_field_prediction_release_promotion_checklist_gssi51600s_3d_y010_crossline_assumption_blocked/`.
- Current workflow command pack: `outputs/validation_exp_on_field_data/product_leaderboard/191_field_prediction_workflow_command_pack_gssi51600s_3d_y010_candidate/`.
- Current default audit: `outputs/validation_exp_on_field_data/product_leaderboard/192_field_prediction_product_default_audit_gssi51600s_3d_y010_candidate/`.

## Next Defensible Task

Resolve the assumed GSSI crossline profile spacing by checking metadata and data layout, then rerun or re-score the finite-length 3D candidate with confirmed y geometry so the release checklist can move beyond the current y-geometry block.

The local marathon request remains active.
