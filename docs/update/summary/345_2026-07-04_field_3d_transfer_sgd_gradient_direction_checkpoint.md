# Field 3D Transfer SGD Gradient-Direction Checkpoint

## What changed
- Added `sgd` support to the shared Torch optimizer factory as a diagnostic option.
- Exposed `sgd` through the finite-length transfer optimizer CLI.
- Ran a controlled `0704` profile-mean/10 MHz transfer diagnostic:
  - `290_field_3d_0704_fastgpr_transfer_seed_mid_source10_profile_mean_sgd_lr1_iter3`
- Synthesized AdamW vs SGD:
  - `291_field_3d_0704_transfer_adamw_sgd_gradient_direction_synthesis`

## Key numbers
- AdamW profile-mean/10 MHz:
  - best loss `0.7859343290`
  - best iteration `0`
  - max loss improvement `0.0`
- SGD profile-mean/10 MHz:
  - best loss `0.7859343290`
  - best iteration `0`
  - max loss improvement `0.0`
- Synthesis:
  - decision `finite_length_transfer_optimizer_no_loss_decrease_from_seed`
  - optimizer values include `adamw` and `sgd`
  - x/y/z seed `1.9456 m / 0.55 m / 2.4497 m`

## Current decision
The transfer no-descent pattern is not specific to AdamW/Adamax moment estimates. Plain SGD also does not improve the profile-mean transfer objective from the seed, even though gradients are finite.

## What remains blocked
- Geometry/material parameter updates are not yet product-useful on transfer stacks.
- Source/objective formulation still needs work before transfer predictions can ship.
- Diameter/radius remains flat.

## Validation/resource checks
- `python -m pytest tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py -q`: `11 passed`.
- `python -m py_compile` on changed scripts: passed.
- `git diff --check` on touched files: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/290_field_3d_0704_fastgpr_transfer_seed_mid_source10_profile_mean_sgd_lr1_iter3`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/291_field_3d_0704_transfer_adamw_sgd_gradient_direction_synthesis`

## Next defensible task
Build a product-facing transfer leaderboard that separates:
- shippable `0701` release candidate;
- intake-ready but optimizer-blocked transfer stacks (`0704`, `07011`);
- current best transfer seeds and fit losses;
- explicit no-claim boundaries.

This will keep the deliverable coherent while the next modeling improvement targets source/objective formulation.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
