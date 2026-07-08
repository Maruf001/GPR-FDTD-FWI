# Field 3D 0806 Optimizer Family NAdam/RAdam Checkpoint

## What changed
- Added NAdam and RAdam support to the shared PyTorch optimizer factory:
  - `make_torch_optimizer(...)`
- Added NAdam/RAdam parser support to the finite-length Fast-GPR optimizer.
- Expanded optimizer factory tests to cover:
  - Adam
  - AdamW
  - Adamax
  - NAdam
  - RAdam
  - SGD
- Ran direct `0806` optimizer-family comparisons on the current conductivity-enabled 12 mm recipe:
  - `322_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_nadam_conductivity_diam12_iter8`
  - `323_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_radam_conductivity_diam12_iter8`
- Synthesized optimizer-family evidence:
  - `324_field_3d_0806_transfer_conductivity_optimizer_family_nadam_radam`

## Key Numbers
- AdamW reference:
  - best loss `0.7909555435`
  - best diameter `10.6360 mm`
  - best length `0.08136 m`
- NAdam run `322`:
  - best loss `0.7910084128`
  - best field L1 `0.7909806371`
  - best diameter `10.9985 mm`
  - best length `0.08610 m`
  - best epsr `3.47193`
  - background conductivity `0.005481 S/m`
- RAdam run `323`:
  - best loss `0.7915852070`
  - no loss decrease
  - best diameter remains `12.0 mm`
  - best length remains `0.10 m`
- Optimizer-family synthesis `324`:
  - best optimizer `adamw`
  - near-best optimizer values `adamw`, `nadam`, `radam`
  - near-best diameter range `10.6360-12.0000 mm`
  - near-best field L1 range `0.7909555-0.7915852`
  - runtime range `12.37-12.77 s/iteration`

## Current decision
AdamW remains the current optimizer for the `0806` transfer-candidate recipe. NAdam is close but does not beat AdamW. RAdam at the current learning rate does not move enough to be useful.

## What remains blocked
- The product pointer does not change because the best row is still the AdamW 12 mm conductivity run already captured in `086`.
- RAdam may need a different learning rate to be meaningful, but that is lower priority than release-risk checks.
- Diameter remains a range, not a unique claim.

## Validation/resource checks
- `python -m py_compile run_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py`: passed.
- Conda torch-specific tests failed because `gpr-fdtd-fwi` lacks torch; reran with base Python.
- `python -m pytest tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py -q`: `11 passed`.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py -q`: `6 passed`.
- `git diff --check` on touched optimizer/recipe files: passed.
- Figures:
  - `322` optimizer figure is `1957 x 767` PNG.
  - `323` optimizer figure is `1957 x 767` PNG.
  - `324` synthesis figure is `2389 x 767` PNG.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/322_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_nadam_conductivity_diam12_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/323_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_radam_conductivity_diam12_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/324_field_3d_0806_transfer_conductivity_optimizer_family_nadam_radam`

## Next defensible task
Use the new fit-recipe entry point to run a short execute-mode smoke with `iterations=1`, verifying that the recipe can launch the actual optimizer end-to-end without manually writing the long command.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
