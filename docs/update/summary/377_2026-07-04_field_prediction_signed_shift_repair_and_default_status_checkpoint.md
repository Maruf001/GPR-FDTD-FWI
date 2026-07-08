# Field Prediction Signed-Shift Repair And Default Status Checkpoint

## What changed
- Added transfer-seed summary support to the local Fast-GPR window parser:
  - `x_m` is accepted as `x0_m`
  - `epsr_fastgpr` is accepted as `epsr`
- Added signed time-shift support to the finite-length Fast-GPR optimizer loss.
- Added `--shift-seed-ns` so field-data repair runs can use ladder-derived time-zero estimates instead of only the transfer seed default.
- Tightened finite-length synthesis decisions:
  - meaningful improvement threshold is now `1.0e-3`
  - tiny decreases are labeled `finite_length_transfer_optimizer_tiny_decrease_needs_confirmation`, not as stability support
- Ran repair diagnostics for blocked transfer datasets `0704` and `07011`.
- Refreshed product defaults so the current query exposes:
  - promoted `0806`
  - `0704` as tiny-decrease-needs-confirmation
  - `07011` as blocked

## Key numbers
- 0704 time/polarity ladder `346`:
  - best shift `+0.2 ns`
  - best polarity `-1`
  - best local ladder loss `0.832048`
  - improvement vs positive zero-shift baseline `0.004491`
- 0704 shift-seeded optimizer `347`:
  - decision `finite_length_scattered_optimizer_no_material_loss_decrease`
  - best loss `0.7871618866920471`
  - initial loss `0.7872289419174194`
  - improvement `0.00006705522537231445`
  - best diameter `11.959163 mm`
  - best length-y `0.097784 m`
  - best shift `0.187507 ns`
- 0704 thresholded synthesis `352`:
  - decision `finite_length_transfer_optimizer_tiny_decrease_needs_confirmation`
  - meaningful improvement `false`
  - near-best diameter range `11.959163-12.000000 mm`
  - near-best length-y range `0.097784-0.100000 m`
- 07011 time/polarity ladder `348`:
  - best shift `-2.2 ns`
  - best polarity `-1`
  - best local ladder loss `0.830864`
  - improvement vs positive zero-shift baseline `0.049320`
- 07011 signed-shift optimizer `349`:
  - decision `finite_length_scattered_optimizer_no_material_loss_decrease`
  - best loss `0.7809956669807434`
  - improvement `0.0`
  - best diameter `12.000000 mm`
  - best length-y `0.100000 m`
  - best shift `-2.200000 ns`
- 07011 thresholded synthesis `353`:
  - decision `finite_length_transfer_optimizer_no_loss_decrease_from_seed`
  - meaningful improvement `false`

## Product default status
- Refreshed product artifacts:
  - transfer leaderboard `129`
  - product pointer `130`
  - predictor card `131`
  - release checklist `132`
  - release card `133`
  - range policy `134`
  - range card `135`
  - workflow pack `136`
  - default audit `137`
- Default query now reports:
  - `external_2025_pipe_0806`: `release_promoted_candidate`
  - `external_2025_pipe_0704`: `transfer_needs_confirmation`
  - `external_2025_pipe_07011`: `blocked_transfer`
- Product default audit `137`:
  - decision `product_defaults_ready`
  - missing count `0`
  - transfer alignment `true`
  - release-card alignment `true`
  - range-policy alignment `true`

## Current decision
The signed-shift repair fixed a real optimizer limitation, but it did not make `0704` or `07011` shippable. `0806` remains the promoted real-field 3D prediction. `0704` now has a small but sub-threshold optimizer decrease and should be repeated or repaired further before any geometry/material claim. `07011` remains blocked by no loss decrease.

## What remains blocked
- `0704` needs stronger objective/source/window repair before it can become a product candidate.
- `07011` needs source/window/objective repair; signed negative shift alone was insufficient.
- The local ladders show very small Fast-GPR homogeneous prediction amplitude relative to observed field windows, so amplitude/source modeling remains a likely blocker for transfer generalization.

## Validation/resource checks
- `python -m py_compile` on touched optimizer/product scripts: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py tests/test_field_prediction_workflow_command_pack.py tests/test_field_prediction_product_default_audit.py tests/test_field_prediction_current_query.py tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_current_predictor_card.py tests/test_field_prediction_release_promotion_checklist.py tests/test_field_prediction_release_promotion_card.py tests/test_field_prediction_release_policy_variant.py tests/test_field_prediction_range_release_candidate_card.py tests/test_field_prediction_transfer_leaderboard.py -q`: `47 passed, 2 skipped`.
- Base Python torch test slice for signed shift: `8 passed`.
- `git diff --check` on touched files and checkpoints: passed.
- Figures for `348`, `349`, `352`, and `353` opened with nonzero dimensions.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/346_field_3d_0704_fastgpr_time_polarity_ladder_transfer_seed_mid_profile4_sample60`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/347_field_3d_0704_fastgpr_transfer_seed_sample56_60_profile_mean_source20_adamw_conductivity_diam12_polarity_neg_shift02_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/348_field_3d_07011_fastgpr_time_polarity_ladder_transfer_seed_profile0_sample66`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/349_field_3d_07011_fastgpr_transfer_seed_sample62_66_profile_mean_source10_adamw_conductivity_diam12_polarity_neg_shiftm22_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/352_field_3d_0704_signed_shift_repair_attempt_synthesis_thresholded`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/353_field_3d_07011_signed_shift_repair_attempt_synthesis_thresholded`
- `outputs/validation_exp_on_field_data/product_leaderboard/133_field_prediction_release_promotion_card_0806_three_window_with_0704_07011_repair_status_ready`
- `outputs/validation_exp_on_field_data/product_leaderboard/137_field_prediction_product_default_audit_0806_three_window_with_0704_07011_repair_status_default`

## Next defensible task
Update the daily update file, then continue field-data product work by improving source/amplitude modeling or applying the promoted workflow to another real field profile without changing the claim boundary.

## Marathon status
The requested local marathon remains active. This block is complete enough to document before continuing.
