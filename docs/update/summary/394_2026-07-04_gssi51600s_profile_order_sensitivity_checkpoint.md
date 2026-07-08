# GSSI51600S Profile-Order Sensitivity Checkpoint

## What Changed

- Added `run_gssi51600s_profile_subset_stack_adapter.py`.
- Added unit tests for profile-index parsing and stack/manifest reordering.
- Built a reordered trusted GSSI stack using original profiles `3,2,1`.
- Ran the same five-window AdamW joint optimizer on the reordered stack.
- Synthesized the original `1-3` profile subset against the reversed `3,2,1` stack.

## Key Numbers

- Reordered stack artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/093_gssi51600s_profile_subset_stack_original3_2_1/`.
- Reordered optimizer artifact: `outputs/validation_exp_on_field_data/3d_geometry_inventory/418_gssi51600s_finite_length_3d_surface075_reordered3_2_1_seed094_y016_adamw_windows50_54_58_62_66_iter6/`.
- Order-sensitivity synthesis: `outputs/validation_exp_on_field_data/3d_geometry_inventory/419_gssi51600s_finite_length_3d_profile_order_sensitivity_1_3_vs_reversed3_2_1_adamw_y016/`.
- Original `1-3`: length `0.216162652 m`, diameter `17.315585 mm`, objective loss `0.979076803`.
- Reversed `3,2,1`: length `0.216160715 m`, diameter `17.315581 mm`, objective loss `0.979075968`.
- Near-best length range: `0.216160715-0.216162652 m`.
- Near-best diameter range: `17.315581-17.315585 mm`.

## Current Decision

Simple profile-order reversal does not explain the longer-length branch. The `1-3` subset remains internally stable after reversal, so the discrepancy between the shorter `0-2` branch and longer `1-3` branch is more likely tied to crossline geometry, profile content, or acquisition layout than to reversed file ordering.

## Validation

- `python -m pytest tests/test_gssi51600s_profile_subset_stack_adapter.py tests/test_gssi51600s_finite_length_seed.py tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q` passed with `28 passed`.
- `python -m py_compile run_gssi51600s_profile_subset_stack_adapter.py` passed.
- `git diff --check` passed.

## Next Defensible Task

Inspect profile content and acquisition layout around profiles `0-2` and `1-3`, especially whether profile amplitudes, event timing, or original trace extents differ enough to support two distinct finite-length fits.

The local marathon request remains active.
