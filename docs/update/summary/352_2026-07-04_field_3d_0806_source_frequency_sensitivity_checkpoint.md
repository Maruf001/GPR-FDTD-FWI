# Field 3D 0806 Source Frequency Sensitivity Checkpoint

## What changed
- Ran `0806` Adamax transfer optimizer at source `20 MHz`:
  - `304_field_3d_0806_fastgpr_transfer_seed_profile_mean_source20_adamax_iter8`
- Synthesized source-frequency sensitivity:
  - `305_field_3d_0806_transfer_source_frequency_sensitivity`

## Key numbers
- `10 MHz`:
  - best loss `0.7937642932`
  - best length `0.08458 m`
  - best diameter `8.00037 mm`
- `20 MHz`:
  - best loss `0.7956532836`
  - best length `0.08498 m`
  - best diameter `8.00040 mm`
- Synthesis:
  - best label `0806_source10_adamax_iter8`
  - 10 MHz remains the better fit
  - both source settings descend, but 20 MHz lands at a worse loss

## Current decision
The `0806` threshold descent is not exclusive to 10 MHz, but 10 MHz is the current best source setting for this transfer seed/window.

## What remains blocked
- Need sample-window sensitivity.
- Need stronger repeatability before release.
- Diameter remains a range, not a scalar.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`: `7 passed`.
- `git diff --check` on touched files: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/304_field_3d_0806_fastgpr_transfer_seed_profile_mean_source20_adamax_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/305_field_3d_0806_transfer_source_frequency_sensitivity`

## Next defensible task
Run a nearby sample-window check for `0806` at sample start `42`, source `10 MHz`, Adamax. This tests whether the threshold descent is robust to the event-window start.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
