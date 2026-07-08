# Field 3D 0701 Joint Window Sensitivity Checkpoint

## What Changed

- Ran the current best joint x/z/material/source-time optimizer on neighboring real-data time windows.
- Added a window-sensitivity synthesis artifact.
- Updated the shipping snapshot with multi-window evidence.

## Key Numbers

- Window optimizer runs:
  - `247...window_start40`
  - `251...window_start30`
  - `252...window_start50`
- Synthesis artifact:
  - `253_field_3d_0701_joint_window_sensitivity`
- Shipping snapshot:
  - `059_field_prediction_shipping_snapshot`
- Synthesis decision:
  - `joint_window_sensitivity_radius_gradient_negligible`
- Best window:
  - label `window_start50`
  - target start `19.531248093 ns`
  - field L1 loss `0.668602407`
- Loss range:
  - `0.668602407-0.793126464`
- Length range:
  - `0.096883565-0.096884780 m`
- Diameter range in this same-seed window sensitivity:
  - `8.000397123-8.000397123 mm`
- Max gradients:
  - radius `1.113725112e-09`
  - length `2.726360435e-05`
  - source-time shift `2.647856623e-02`
  - background epsr `3.293803893e-04`

## What Remains Blocked

- The late window improves fit, but radius gradient remains negligible.
- This confirms that simply moving the time window does not make diameter identifiable.
- Diameter remains a near-best range from the seed/joint stress runs, not a scalar claim.

## Current Decision

The multi-window branch strengthens the finite-length result and weakens the diameter claim:

- finite length is stable near `0.097 m` across tested windows;
- best fit occurs in the later window;
- radius is still not an active gradient direction.

## Next Defensible Task

The next radius-focused work should change the information content, not just rerun the same objective:

- add antenna/source-shape parameters;
- test a multi-window combined loss instead of separate windows;
- or use independent labeled/caliper data if available.

## Validation And Resources

- Window-sensitivity tests:
  - `3 passed`
- Product/window tests:
  - `15 passed`
- Expanded focused suite:
  - `56 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile ...`
  - passed for changed scripts/tests
- touched-file `git diff --check`
  - passed
- Figure checks:
  - `253.../figures/field_3d_0701_joint_window_sensitivity.png`: size `(2263, 750)`, stddev `68.676`
  - `059.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, stddev `64.402`

## Artifact Paths

- Window sensitivity:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/253_field_3d_0701_joint_window_sensitivity`
- Updated shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/059_field_prediction_shipping_snapshot`
- Checkpoint:
  - `docs/update/summary/329_2026-07-04_field_3d_0701_joint_window_sensitivity_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
