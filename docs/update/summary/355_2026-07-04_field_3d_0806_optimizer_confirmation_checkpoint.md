# Field 3D 0806 Optimizer Confirmation Checkpoint

## What changed
- Ran a second optimizer-family confirmation for the `0806` real-field transfer candidate:
  - `309_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_adamw_iter8`
- Synthesized `0806` sample-window/optimizer confirmation across:
  - sample start `38`, source 10 MHz, Adamax 8 iterations,
  - sample start `42`, source 10 MHz, Adamax 8 iterations,
  - sample start `42`, source 10 MHz, AdamW 8 iterations.
- Regenerated the product transfer leaderboard:
  - `077_field_prediction_transfer_leaderboard_with_0806_optimizer_confirmation`
- Updated the current product pointer:
  - `078_field_prediction_current_product_pointer_with_0806_optimizer_confirmation`

## Key numbers
- AdamW confirmation run:
  - initial loss `0.7915197015`
  - best loss `0.7912911177`
  - best field L1 `0.7912877798`
  - improvement `0.0002285838`
  - best length `0.080975 m`
  - best diameter `8.000378 mm`
  - best local center x/depth `0.61165 m / 1.80433 m`
  - best background epsr `3.55747`
  - best anomaly delta epsr `0.72620`
  - mean runtime `12.18 s/iteration`
- Optimizer-confirmation synthesis:
  - decision `finite_length_joint_xz_material_stability_supports_010m_length_not_diameter`
  - best label `0806_sample42_source10_adamw_iter8`
  - best field L1 `0.7912877798`
  - near-best length range `0.08098-0.08514 m`
  - near-best center x range `0.58421-0.61165 m`
  - near-best depth range `1.79299-1.82341 m`
  - near-best epsr range `3.50665-3.55747`
  - diameter status remains `diameter_not_identified_gradient_negligible`
- Current pointer:
  - shipped 3D dataset remains `external_2025_pipe_0701`
  - transfer candidate is `external_2025_pipe_0806`
  - optimizer-blocked transfer stacks remain `external_2025_pipe_07011` and `external_2025_pipe_0704`

## Current decision
`0806` is stronger than before because the finite-length candidate is now supported by both Adamax and AdamW under the same field window/source/objective. It is still a transfer candidate, not a release promotion, because diameter is not identified and conductivity is not yet reported for this transfer candidate.

## What remains blocked
- Diameter is still effectively pinned to the lower bound with negligible radius gradient.
- Conductivity is not yet part of the `0806` transfer candidate output.
- `0704` and `07011` remain blocked by no optimizer descent from their current seed/window setups.

## Validation/resource checks
- `python -m py_compile run_field_prediction_current_product_pointer.py`: passed.
- `python -m py_compile run_field_3d_0701_finite_length_optimizer_seed_stability.py`: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_current_product_pointer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`: `13 passed`.
- `git diff --check` on touched field/product scripts: passed.
- Figures:
  - `309` optimizer figure is `1957 x 767` PNG.
  - `310` synthesis figure is `2364 x 767` PNG.
  - `077` leaderboard figure is `2399 x 767` PNG.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/309_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_adamw_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/310_field_3d_0806_transfer_sample42_optimizer_confirmation`
- `outputs/validation_exp_on_field_data/product_leaderboard/077_field_prediction_transfer_leaderboard_with_0806_optimizer_confirmation`
- `outputs/validation_exp_on_field_data/product_leaderboard/078_field_prediction_current_product_pointer_with_0806_optimizer_confirmation`

## Next defensible task
Add a bounded transfer-candidate material-reporting layer for `0806` so the product row can expose a conductivity estimate or explicitly state why conductivity is not identifiable in the current Fast-GPR objective.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
