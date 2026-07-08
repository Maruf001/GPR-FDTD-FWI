# External 2025 JAX 3D Scalar Fixed-Material Recovery Checkpoint

## What changed
- Added per-parameter trainable weights to the JAX scalar recovery runner.
- Added a fixed-material/radius recovery diagnostic:
  - trainable: `cx`, `cy`, `cz`, `length_y`
  - frozen: `radius`, `epsr_proxy`
- Added the result to the field-method validation leaderboard.

## Key numbers
- Artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/273_external_2025_jax_3d_scalar_fixed_material_recovery`
- Runtime: `1.8449724558740854 s`
- Initial normalized loss: `1788.699462890625`
- Final normalized loss: `0.010942996479570866`
- Loss reduction: `0.9999938821491778`
- True length: `18.0` cells
- Initial length: `8.0` cells
- Final length: `16.55443780412135` cells
- Final length error: `1.4455621958786509` cells
- Radius fixed at: `2.0` cells
- epsr proxy fixed at: `80.0`
- Figure validation: `ok`, `105124` bytes
- Leaderboard evidence score: `1` diagnostic

## What remains blocked
- This is still synthetic scalar-reference recovery.
- This is not Maxwell-complete.
- This is not field-data fitting.
- It does show that free radius/material proxy was a major cause of length ambiguity in the scalar optimizer.

## Current decision
`external_2025_jax_3d_scalar_parameter_recovery_loss_reduced_length_improved`

Constrain known scatterer material/radius first; geometry and length become much more recoverable.

## Next defensible task
Before real field use, create a field-facing policy that separates:
- known or tightly bounded rebar material/radius priors;
- concrete/background epsr estimation;
- geometry/length inversion.

## Validation/resource checks
- `python -m py_compile run_external_2025_jax_3d_scalar_fixed_material_recovery.py run_external_2025_jax_3d_scalar_parameter_recovery.py run_field_method_validation_leaderboard.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_external_2025_jax_3d_scalar_fixed_material_recovery.py tests/test_external_2025_jax_3d_scalar_parameter_recovery.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `35 passed`
- Leaderboard regenerated at `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Artifact paths
- Summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/273_external_2025_jax_3d_scalar_fixed_material_recovery/data/external_2025_jax_3d_scalar_fixed_material_recovery_summary.json`
- Rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/273_external_2025_jax_3d_scalar_fixed_material_recovery/data/external_2025_jax_3d_scalar_fixed_material_recovery_rows.csv`
- Convergence figure: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/273_external_2025_jax_3d_scalar_fixed_material_recovery/figures/external_2025_jax_3d_scalar_fixed_material_recovery.png`

## Marathon status
The marathon request is still active; continue by translating this into a real-field inversion policy rather than claiming scalar synthetic success.
