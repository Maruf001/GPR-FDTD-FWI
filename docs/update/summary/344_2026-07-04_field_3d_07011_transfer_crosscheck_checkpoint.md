# Field 3D 07011 Transfer Cross-Check Checkpoint

## What changed
- Generated a real-stack `07011` transfer seed:
  - `285_field_3d_07011_transfer_seed_energy_window_profile_axis_y`
- Ran bounded Fast-GPR optimizer checks on `07011`:
  - `286_field_3d_07011_fastgpr_transfer_seed_profile_mean_source10_adamw_iter1`
  - `287_field_3d_07011_fastgpr_transfer_seed_profile_mean_source10_adamw_iter3`
  - `288_field_3d_07011_fastgpr_transfer_seed_receiver_mean_source10_adamw_iter1`
- Synthesized the `07011` transfer objective result:
  - `289_field_3d_07011_transfer_objective_synthesis`

## Key numbers
- `07011` seed:
  - x `0.2048 m`
  - profile-axis y `0.15 m`
  - z `2.6431 m`
  - profile window `0-3`
  - sample start `66`
  - trace window `0-15`
- Profile-mean residualization:
  - one-step loss `0.7787904143`
  - three-step best loss `0.7787904143`
  - no optimizer loss decrease.
- Receiver-mean residualization:
  - one-step loss `0.8170036077`
  - worse than profile mean.
- Synthesis:
  - decision `finite_length_transfer_optimizer_no_loss_decrease_from_seed`
  - best label `07011_profile_iter1`
  - max optimizer loss improvement `0.0`

## Current decision
`07011` confirms the `0704` pattern: profile-mean residualization gives a lower initial field loss, but finite-length geometry/material/source-time AdamW updates still do not reduce the objective after the seed.

## What remains blocked
- This is now likely a shared transfer-objective/source-model issue, not only a `0704` dataset issue.
- The seed fit is improving across stacks, but post-seed descent is not.
- Diameter/radius remains flat.
- The `07011` seed is edge-dominated, so its x/trace location should not be promoted as a final prediction.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_stack_transfer_seed.py tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`: `19 passed`.
- `python -m py_compile` on changed scripts: passed.
- `git diff --check` on touched files: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/285_field_3d_07011_transfer_seed_energy_window_profile_axis_y`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/286_field_3d_07011_fastgpr_transfer_seed_profile_mean_source10_adamw_iter1`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/287_field_3d_07011_fastgpr_transfer_seed_profile_mean_source10_adamw_iter3`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/288_field_3d_07011_fastgpr_transfer_seed_receiver_mean_source10_adamw_iter1`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/289_field_3d_07011_transfer_objective_synthesis`

## Next defensible task
Audit the transfer objective gradient signs and step response. The optimizer has finite gradients, but every first step worsens or leaves loss unchanged, so the next product-improving change should compare:
- gradient direction vs opposite-gradient direction for the active parameters;
- fixed parameter perturbation around the seed;
- whether the normalized L1 objective is non-smooth enough that Adam updates are not a good first optimizer on transfer stacks.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
