# Field 3D 0704 Transfer Objective/Nuisance Checkpoint

## What changed
- Added fixed prediction polarity support to the finite-length Fast-GPR optimizer:
  - `--prediction-polarity`
- Tested `0704` mid-window/10 MHz transfer objective variants:
  - `280_field_3d_0704_fastgpr_transfer_seed_mid_source10_polarity_neg_adamw_iter1`
  - `281_field_3d_0704_fastgpr_transfer_seed_mid_source10_adamw_lr001_iter3`
  - `282_field_3d_0704_fastgpr_transfer_seed_mid_source10_profile_mean_adamw_iter1`
  - `283_field_3d_0704_fastgpr_transfer_seed_mid_source10_profile_mean_adamw_iter3`
- Synthesized the nuisance/objective comparison:
  - `284_field_3d_0704_transfer_objective_nuisance_synthesis`

## Key numbers
- Best prior receiver-mean mid-window condition:
  - label `receiver_mid10`
  - loss `0.7887895107`
- Inverted polarity:
  - loss `0.7887899280`
  - no improvement over positive polarity.
- Lower learning rate:
  - best loss `0.7887895107`
  - no optimizer decrease.
- Profile-mean residualization:
  - one-step loss `0.7859343290`
  - three-step best loss `0.7859343290`
  - best label in synthesis: `profile_mid10`
- Synthesis:
  - decision `finite_length_transfer_optimizer_no_loss_decrease_from_seed`
  - max optimizer loss improvement after seed: `0.0`
  - best seed x/y/z: `1.9456 m / 0.55 m / 2.4497 m`

## Current decision
Profile-mean residualization is the current best `0704` transfer objective variant, but it still does not produce post-seed optimizer improvement. This is not yet a shippable `0704` prediction.

## What remains blocked
- The current Fast-GPR transfer objective can choose a better field window/objective, but geometry/material updates still do not reduce the loss.
- Fixed polarity is not the missing nuisance parameter.
- Lower AdamW learning rate is not enough.
- Diameter remains flat.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`: `13 passed`.
- `python -m py_compile run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py run_field_3d_0701_finite_length_optimizer_seed_stability.py`: passed.
- `git diff --check` on touched files: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/280_field_3d_0704_fastgpr_transfer_seed_mid_source10_polarity_neg_adamw_iter1`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/281_field_3d_0704_fastgpr_transfer_seed_mid_source10_adamw_lr001_iter3`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/282_field_3d_0704_fastgpr_transfer_seed_mid_source10_profile_mean_adamw_iter1`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/283_field_3d_0704_fastgpr_transfer_seed_mid_source10_profile_mean_adamw_iter3`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/284_field_3d_0704_transfer_objective_nuisance_synthesis`

## Next defensible task
Run the smaller `07011` stack through the same transfer seed and bounded optimizer path. If `07011` also has no post-seed optimizer decrease, the blocker is likely objective/source modeling shared across transfer stacks; if it improves, `0704` is a dataset/window-specific issue.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
