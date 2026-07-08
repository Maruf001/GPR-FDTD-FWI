# Field 3D 0806 Conductivity Confirmation Checkpoint

## What changed
- Added optional bounded conductivity optimization to `run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py`:
  - `--optimize-conductivity`
  - background/anomaly conductivity bounds
  - per-iteration conductivity values and gradients
  - best/final conductivity fields in the optimizer summary
- Propagated conductivity through:
  - `run_field_3d_0701_finite_length_optimizer_seed_stability.py`
  - `run_field_prediction_transfer_leaderboard.py`
  - `run_field_prediction_current_product_pointer.py`
- Ran the real `0806` conductivity-enabled optimizer:
  - `311_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_adamw_conductivity_iter8`
- Synthesized conductivity-confirmed `0806` evidence:
  - `312_field_3d_0806_transfer_conductivity_confirmation`
- Refreshed product-facing artifacts:
  - `079_field_prediction_transfer_leaderboard_with_0806_conductivity_confirmation`
  - `080_field_prediction_current_product_pointer_with_0806_conductivity_confirmation`

## Key numbers
- Conductivity optimizer run `311`:
  - initial loss `0.7915187478`
  - best objective loss `0.7912659645`
  - best field L1 `0.7912156582`
  - best length `0.093568 m`
  - best diameter `8.000392 mm`
  - best local center x/depth `0.60722 m / 1.84962 m`
  - best epsr/delta epsr `3.37157 / 0.91224`
  - best background conductivity `0.004398 S/m`
  - best anomaly conductivity `0.041526 S/m`
  - conductivity gradients finite:
    - background max raw grad `4.25e-6`
    - anomaly max raw grad `3.75e-6`
  - mean runtime `12.61 s/iteration`
- Conductivity synthesis `312`:
  - decision `finite_length_joint_xz_material_stability_supports_010m_length_not_diameter`
  - best label `0806_sample42_source10_adamw_conductivity_iter8`
  - near-best length range `0.08098-0.09357 m`
  - near-best diameter range `8.00037-8.00039 mm`
  - near-best background epsr range `3.37157-3.55747`
  - conductivity status `optimized_bounded_fastgpr_parameter`
- Current pointer `080`:
  - shipped 3D dataset remains `external_2025_pipe_0701`
  - transfer candidate remains `external_2025_pipe_0806`
  - `0806` now reports background conductivity `0.004398 S/m`

## Current decision
`0806` now has a real optimized conductivity estimate in the finite-length Fast-GPR transfer objective. It remains a transfer candidate rather than a release promotion because diameter is still effectively pinned to the lower bound and not independently identified.

## What remains blocked
- Diameter/radius remains the main blocker: the radius gradient is still negligible and the best diameter is at the lower bound.
- `0704` and `07011` still do not decrease loss from the current seed/window setup.
- Conductivity has only one optimized confirmation run so far; it should be repeated under a neighboring seed/objective before release promotion.

## Validation/resource checks
- `python -m py_compile run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py run_field_3d_0701_finite_length_optimizer_seed_stability.py run_field_prediction_transfer_leaderboard.py run_field_prediction_current_product_pointer.py`: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_current_product_pointer.py -q`: `19 passed`.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_current_product_pointer.py -q`: `6 passed`.
- `git diff --check` on touched scripts/tests/checkpoint: passed.
- Figures:
  - `311` optimizer figure is `1957 x 767` PNG.
  - `312` synthesis figure is `2372 x 767` PNG.
  - `079` leaderboard figure is `2399 x 767` PNG.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/311_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_adamw_conductivity_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/312_field_3d_0806_transfer_conductivity_confirmation`
- `outputs/validation_exp_on_field_data/product_leaderboard/079_field_prediction_transfer_leaderboard_with_0806_conductivity_confirmation`
- `outputs/validation_exp_on_field_data/product_leaderboard/080_field_prediction_current_product_pointer_with_0806_conductivity_confirmation`

## Next defensible task
Run a bounded diameter-identifiability stress on `0806` with the conductivity-enabled objective: repeat the same setup from a 12 mm diameter seed and synthesize whether the best field fit truly distinguishes 8 mm from 12 mm.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
