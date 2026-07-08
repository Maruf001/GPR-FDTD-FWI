# Field 3D 0704 Transfer Seed Optimizer Checkpoint

## What changed
- Added a real-stack transfer seed generator:
  - `run_field_3d_stack_transfer_seed.py`
  - Output: `266_field_3d_0704_transfer_seed_energy_window_profile_axis_y`
- Corrected the seed y coordinate to use the optimizer's sequential profile-axis spacing, while retaining `grid_row_y_center_m_assumed` for auditability.
- Made the finite-length optimizer accept transfer seeds without requiring `0701` stability/finite-forward summaries.
- Added transfer-aware optimizer comparison behavior so no-loss-decrease runs are explicitly blocked from product promotion.
- Ran `0704` transfer optimizer tests on the real stack:
  - `267_field_3d_0704_fastgpr_transfer_seed_adamw_iter3`
  - `268_field_3d_0704_fastgpr_transfer_seed_adamax_iter3`
  - `269_field_3d_0704_transfer_optimizer_adamw_adamax_synthesis`

## Key numbers
- `0704` transfer seed:
  - x: `4.3008 m`
  - profile-axis y: `0.35 m`
  - grid-row y: `0.0 m`
  - z seed: `1.869484 m`
  - profile window: `2-5`
  - sample start: `42`
  - trace window: `160-175`
- `0704` AdamW:
  - best loss: `0.7988616228`
  - loss improvement: `0.0`
  - final length: `0.110755 m`
  - final epsr: `3.216189`
  - mean runtime: `12.33 s/iter`
- `0704` Adamax:
  - best loss: `0.7988616228`
  - loss improvement: `0.0`
  - final length: `0.108886 m`
  - final epsr: `3.227973`
  - mean runtime: `12.16 s/iter`
- Shared gradient finding:
  - max radius raw gradient: `4.71e-11`
  - max length raw gradient: `4.05e-06`
  - max shift raw gradient: `8.76e-03`
  - max background epsr raw gradient: `1.11e-04`

## Current decision
`finite_length_transfer_optimizer_no_loss_decrease_from_seed`.

The `0704` stack is intake-ready and the optimizer runs with finite gradients, but this seed/window/source setup should not be shipped as a `0704` prediction because neither AdamW nor Adamax improved the objective.

## What remains blocked
- `0704` needs better source/time/window alignment before geometry/material claims are defensible.
- Radius/diameter is still effectively flat in this transfer run.
- Y spacing remains an assumption, not measured survey geometry.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_stack_transfer_seed.py tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`: passed.
- Transfer/intake focused tests also passed during this branch.
- `python -m py_compile` on changed scripts: passed.
- `git diff --check` on touched files: passed.
- Figure dimensions/dynamic ranges checked for the seed and optimizer synthesis figures.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/266_field_3d_0704_transfer_seed_energy_window_profile_axis_y`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/267_field_3d_0704_fastgpr_transfer_seed_adamw_iter3`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/268_field_3d_0704_fastgpr_transfer_seed_adamax_iter3`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/269_field_3d_0704_transfer_optimizer_adamw_adamax_synthesis`

## Next defensible task
Improve transfer source/window alignment before trying more iterations:
1. Generate alternate `0704` seeds over several sample windows and residual modes.
2. Run a cheap source-frequency/sample-start scan against the transfer objective.
3. Only rerun AdamW/Adamax after a seed/window combination shows lower initial field loss.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
