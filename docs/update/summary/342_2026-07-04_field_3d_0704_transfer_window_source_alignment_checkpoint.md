# Field 3D 0704 Transfer Window/Source Alignment Checkpoint

## What changed
- Generated alternate real-stack `0704` transfer seeds:
  - `270_field_3d_0704_transfer_seed_mid_window_profile_axis_y`
  - `271_field_3d_0704_transfer_seed_late_window_profile_axis_y`
  - `272_field_3d_0704_transfer_seed_shallow_window_profile_axis_y`
- Ran bounded Fast-GPR checks on real `0704` windows:
  - `273_field_3d_0704_fastgpr_transfer_seed_shallow_adamw_iter1`
  - `274_field_3d_0704_fastgpr_transfer_seed_mid_adamw_iter1`
  - `275_field_3d_0704_fastgpr_transfer_seed_mid_adamw_iter3`
  - `276_field_3d_0704_fastgpr_transfer_seed_mid_source35_adamw_iter1`
  - `277_field_3d_0704_fastgpr_transfer_seed_mid_source10_adamw_iter1`
- Regenerated synthesis with source-frequency values:
  - `279_field_3d_0704_transfer_window_source_alignment_synthesis_with_frequency`

## Key numbers
- Shallow seed:
  - x `4.3008 m`, y `0.35 m`, z `1.8050 m`, sample start `40`
  - one-step loss `0.801392`
- Mid seed:
  - x `1.9456 m`, y `0.55 m`, z `2.4497 m`, sample start `60`
  - 20 MHz one-step loss `0.788791`
  - 20 MHz three-step best loss `0.788791`
  - 35 MHz one-step loss `0.789639`
  - 10 MHz one-step loss `0.788790`
- Late seed:
  - x `2.6624 m`, y `0.75 m`, z `3.4166 m`, sample start `90`
  - not yet promoted to Fast-GPR because the mid seed already improved initial alignment and late is more expensive/deeper.
- Synthesis best:
  - best label `mid10`
  - best loss `0.7887895107`
  - source frequencies tested: `10, 20, 35 MHz`
  - max loss improvement after optimizer steps: `0.0`

## Current decision
`finite_length_transfer_optimizer_no_loss_decrease_from_seed`.

The mid-window seed is a better `0704` starting condition than the shallow seed, and 10-20 MHz is better than 35 MHz for this objective. However, the optimizer still does not improve after the seed, so `0704` is not a shippable 3D prediction yet.

## What remains blocked
- Need source/time alignment that produces optimizer loss decrease, not only a better seed loss.
- Diameter remains flat.
- Depth/epsr changes move during steps, but not in a direction that reduces the objective yet.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`: `7 passed`.
- `python -m py_compile run_field_3d_0701_finite_length_optimizer_seed_stability.py`: passed.
- `git diff --check` on touched files: passed.
- Seed and synthesis figures exist as PNGs with nonzero dimensions.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/270_field_3d_0704_transfer_seed_mid_window_profile_axis_y`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/273_field_3d_0704_fastgpr_transfer_seed_shallow_adamw_iter1`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/274_field_3d_0704_fastgpr_transfer_seed_mid_adamw_iter1`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/275_field_3d_0704_fastgpr_transfer_seed_mid_adamw_iter3`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/276_field_3d_0704_fastgpr_transfer_seed_mid_source35_adamw_iter1`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/277_field_3d_0704_fastgpr_transfer_seed_mid_source10_adamw_iter1`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/279_field_3d_0704_transfer_window_source_alignment_synthesis_with_frequency`

## Next defensible task
Either:
1. test the same transfer-seed path on `07011`, which is smaller and may reveal whether the transfer issue is `0704`-specific; or
2. add a differentiable amplitude/scale/polarity nuisance parameter to the transfer objective before geometry/material updates, because the current geometry/material gradients are finite but do not reduce the field objective.

The second option is more likely to improve shipping fitness because it attacks the source/amplitude mismatch directly.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
