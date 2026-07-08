# GSSI51600S Explicit Profile-Offset Checkpoint

## What Changed

- Added optional explicit profile offsets to the Fast-GPR acquisition helper and finite-length optimizer CLI.
- Preserved the existing uniform-spacing default behavior.
- Added unit tests for explicit profile offsets and parser validation.
- Ran two GSSI noncontiguous-profile diagnostics with explicit offsets derived from the assumed `0.16 m` original profile spacing:
  - profiles `0,1,3`: offsets `[-0.2133333333, -0.0533333333, 0.2666666667] m`.
  - profiles `0,2,3`: offsets `[-0.2666666667, 0.0533333333, 0.2133333333] m`.

## Key Numbers

- Explicit-offset optimizer support:
  - `run_field_3d_0701_fastgpr_finite_length_forward_contrast.py`
  - `run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py`
- `0,1,3` explicit-offset run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/423_gssi51600s_finite_length_3d_surface075_profiles0_1_3_explicit_offsets_y016_adamw_windows50_54_58_62_66_iter6/`.
  - best length `0.183537334 m`.
  - best diameter `17.298099 mm`.
  - best objective loss `0.983752072`.
  - best field L1 loss `0.961503029`.
- `0,2,3` explicit-offset run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/424_gssi51600s_finite_length_3d_surface075_profiles0_2_3_explicit_offsets_y016_adamw_windows50_54_58_62_66_iter6/`.
  - best length `0.183232129 m`.
  - best diameter `17.308654 mm`.
  - best objective loss `0.981314421`.
  - best field L1 loss `0.963452637`.
- Explicit-offset synthesis: `outputs/validation_exp_on_field_data/3d_geometry_inventory/425_gssi51600s_finite_length_3d_noncontiguous_explicit_offset_synthesis_adamw_y016/`.
  - decision `finite_length_joint_xz_material_stability_supports_length_and_diameter`.
  - near-best length range `0.183232129-0.183684886 m`.
  - near-best diameter range `17.297987-17.308654 mm`.

## Current Decision

For the noncontiguous stacks that include profile `0`, explicit profile offsets do not move the optimizer to the longer `0.216 m` branch. The short branch remains stable around `0.183 m` under both uniform and explicit offset assumptions. This strengthens the current interpretation that the long branch is tied to the contiguous `1-3` profile content after profile `0` is omitted, rather than just to the presence of profile `3` or to the noncontiguous stacks being forced onto uniform spacing.

The explicit-offset runs are still assumption-conditioned because the true GSSI crossline profile spacing is not metadata-confirmed. They should be used as diagnostic evidence, not as a product-default replacement.

## Validation

- `python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_forward_contrast.py tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py -q` passed with `19 passed`.
- `python -m py_compile run_field_3d_0701_fastgpr_finite_length_forward_contrast.py run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py` passed.
- `git diff --check` passed for the explicit-offset code and tests.
- The explicit-offset synthesis figure was visually inspected.

## Next Defensible Task

Rerun the broader GSSI/product focused suite after the new offset support, then add a compact profile-0 influence card or a product-query note that distinguishes product defaults from these diagnostic offset runs.

The local marathon request remains active.
