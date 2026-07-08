# Field 0704 Optimizer-Family Guardrail Checkpoint

## What changed
- Ran an Adamax confirmation on the strongest 0704 `sample68_72` raw-amplitude setup to test whether the AdamW result is optimizer-family robust.
- Found that Adamax did not reproduce the AdamW descent.
- Patched the finite-length synthesis logic so mixed optimizer-family checks cannot be promoted when any included optimizer fails the meaningful-descent threshold.
- Added focused tests for the optimizer-family inconclusive path and product leaderboard mapping.
- Regenerated the guarded optimizer-family artifact after the patch.

## Key numbers
- AdamW, 0704 `sample68_72`, raw-amplitude weight `0.01`:
  - decision `finite_length_scattered_optimizer_decreased_loss`
  - objective improvement `0.008793`
  - best field L1 `0.928403`
  - best diameter `12.351951 mm`
  - best length `0.111031 m`
  - best depth `2.407379 m`
  - best epsr `3.385505`
  - best conductivity `0.00381756 S/m`
- Adamax, same window/setup:
  - decision `finite_length_scattered_optimizer_no_material_loss_decrease`
  - objective improvement `0.000280`
  - best field L1 `0.937812`
  - best diameter `12.032982 mm`
  - best length `0.101976 m`
  - best depth `2.438681 m`
  - best epsr `3.335640`
  - best conductivity `0.00391421 S/m`
- Guarded optimizer-family synthesis:
  - decision `finite_length_optimizer_family_inconclusive`
  - max improvement `0.008793`
  - min improvement `0.000280`
  - `all_meaningful_loss_improvement`: `false`
  - `optimizer_family_status`: `optimizer_family_descent_not_reproduced`

## Current decision
0704 remains product-visible as a confirmation-needed transfer result, not a release-promoted prediction. The four-window AdamW/raw-amplitude result is useful, but optimizer-family robustness is not yet established.

0806 remains the current release-promoted real-field 3D prediction.

## What remains blocked
- 0704 cannot be promoted on the basis of AdamW alone.
- The next bounded optimizer-family check should test Adam or RAdam/NAdam under the same four-window raw-amplitude setup, or explicitly define a product policy that accepts AdamW-only transfer estimates as provisional.

## Validation/resource checks
- `python -m py_compile` on patched synthesis and leaderboard scripts: passed.
- Focused tests for synthesis and transfer leaderboard: `17 passed`.
- Guarded synthesis rerun: decision corrected to `finite_length_optimizer_family_inconclusive`.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/373_field_3d_0704_fastgpr_transfer_seed_sample68_72_profile_mean_source20_amp1e8_adamax_conductivity_diam12_polarity_neg_shift16_ampraw001_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/375_field_3d_0704_sample68_72_rawamp001_adamw_adamax_optimizer_family_check_guarded`
- `run_field_3d_0701_finite_length_optimizer_seed_stability.py`
- `run_field_prediction_transfer_leaderboard.py`

## Next defensible task
Run one additional optimizer-family confirmation for 0704 using the same raw-amplitude setup, preferably Adam or RAdam. If a second optimizer reproduces the AdamW descent, rebuild the optimizer-family synthesis; otherwise keep 0704 confirmation-needed and move to another real field stack.

## Marathon status
The requested local marathon remains active. Continue with real-field prediction improvement focused on shippable 3D rebar geometry/material outputs.
