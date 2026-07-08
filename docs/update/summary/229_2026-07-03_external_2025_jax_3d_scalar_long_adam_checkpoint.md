# External 2025 JAX 3D Scalar Long-Adam Checkpoint

## What changed
- Increased the JAX scalar parameter recovery run from `80` to `220` Adam iterations.
- Regenerated the recovery artifact and leaderboard row.

## Key numbers
- Artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/272_external_2025_jax_3d_scalar_parameter_recovery`
- Initial normalized loss: `6585.9033203125`
- Final normalized loss: `0.3424553871154785`
- Loss reduction: `0.9999480017591422`
- Runtime: `2.342746997019276 s`
- True length: `18.0` cells
- Final length: `13.856732854262244` cells
- True epsr proxy: `80.0`
- Final epsr proxy: `58.64934414483593`
- Figure validation: `ok`, `100644` bytes

## What remains blocked
- Longer Adam reduced waveform loss but did not improve the physical length estimate versus the 80-iteration run.
- This confirms a geometry/material tradeoff in the scalar objective.
- Still not field-data fitting, not Maxwell-complete, and not a rebar prediction.

## Current decision
`external_2025_jax_3d_scalar_parameter_recovery_loss_reduced_length_improved`

The optimizer is useful, but waveform-only longer Adam is not enough to identify length/epsr accurately.

## Next defensible task
Run staged or regularized scalar recovery so geometry and material do not trade off unchecked.

## Validation/resource checks
- `python -m py_compile run_external_2025_jax_3d_scalar_parameter_recovery.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_external_2025_jax_3d_scalar_parameter_recovery.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `33 passed`
- Leaderboard regenerated at `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Artifact paths
- Summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/272_external_2025_jax_3d_scalar_parameter_recovery/data/external_2025_jax_3d_scalar_parameter_recovery_summary.json`
- Rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/272_external_2025_jax_3d_scalar_parameter_recovery/data/external_2025_jax_3d_scalar_parameter_recovery_rows.csv`
- Convergence figure: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/272_external_2025_jax_3d_scalar_parameter_recovery/figures/external_2025_jax_3d_scalar_parameter_recovery.png`

## Marathon status
The marathon request is still active; continue with staged/regularized scalar recovery.
