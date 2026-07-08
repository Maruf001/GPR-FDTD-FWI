# External 2025 JAX 3D Scalar Parameter Recovery Checkpoint

## What changed
- Added a differentiable JAX CUDA 3D scalar parameter-recovery prototype.
- Trainable continuous parameters:
  - `cx`, `cy`, `cz`
  - `radius`
  - `length_y`
  - `epsr_proxy`
- Used the stronger `through_y_center` layout from artifact `270`.
- Added the result to the field-method validation leaderboard as optimizer-development evidence.

## Key numbers
- Artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/271_external_2025_jax_3d_scalar_parameter_recovery`
- Adam iterations: `80`
- Runtime: `1.493702044012025 s`
- Initial normalized loss: `6585.9033203125`
- Final normalized loss: `0.46354857087135315`
- Loss reduction: `0.9999296150355803`
- True length: `18.0` cells
- Initial length: `8.0` cells
- Final length: `13.982783569365042` cells
- True epsr proxy: `80.0`
- Initial epsr proxy: `30.0`
- Final epsr proxy: `58.85656255743099`
- Figure validation: `ok`, `106028` bytes
- Leaderboard evidence score: `1` diagnostic

## What remains blocked
- This is scalar-reference inversion, not full Maxwell.
- This is synthetic target recovery, not field-data fitting.
- Recovery is partial: length and epsr move in the right direction but do not recover exact truth.
- It cannot be used as a field-data rebar prediction claim.

## Current decision
`external_2025_jax_3d_scalar_parameter_recovery_loss_reduced_length_improved`

The JAX path is viable for optimizer development: gradients through a true-z-coupled 3D forward model work, and Adam can reduce waveform mismatch while moving 3D geometry/material parameters toward target values.

## Next defensible task
Improve recovery stability before field connection:
- run staged optimization or priors to separate geometry from epsr;
- add repeated random starts or local uncertainty ranges;
- only then map the real field B-scan window into this scalar reference as a provisional 3D objective.

## Validation/resource checks
- `python -m py_compile run_external_2025_jax_3d_scalar_parameter_recovery.py run_field_method_validation_leaderboard.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_external_2025_jax_3d_scalar_parameter_recovery.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `33 passed`
- Leaderboard regenerated at `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Artifact paths
- Summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/271_external_2025_jax_3d_scalar_parameter_recovery/data/external_2025_jax_3d_scalar_parameter_recovery_summary.json`
- Rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/271_external_2025_jax_3d_scalar_parameter_recovery/data/external_2025_jax_3d_scalar_parameter_recovery_rows.csv`
- Convergence figure: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/271_external_2025_jax_3d_scalar_parameter_recovery/figures/external_2025_jax_3d_scalar_parameter_recovery.png`
- Leaderboard CSV: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status
The marathon request is still active; continue with staged/regularized scalar recovery or field-window mapping next.
