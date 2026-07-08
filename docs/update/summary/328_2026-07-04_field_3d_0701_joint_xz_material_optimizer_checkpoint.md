# Field 3D 0701 Joint X/Z/Material Optimizer Checkpoint

## What Changed

- Extended the finite-length optimizer to optionally optimize:
  - local x center,
  - depth,
  - background epsr,
  - anomaly delta epsr,
  - source-time shift,
  - finite length and diameter.
- Ran real 0701 joint x/z/material/source-time optimizer stresses.
- Added joint stability synthesis fields and shipped them into the product snapshot.

## Key Numbers

- Joint optimizer runs:
  - `247...seed_len010_diam08_adamw_iter3`
  - `248...seed_len010_diam12_adamw_iter3`
  - `249...seed_len020_diam08_adamw_iter3`
- Joint synthesis:
  - `250_field_3d_0701_finite_length_joint_xz_material_optimizer_seed_stability`
- Shipping snapshot:
  - `058_field_prediction_shipping_snapshot`
- Synthesis decision:
  - `finite_length_joint_xz_material_stability_supports_010m_length_not_diameter`
- Best joint fit:
  - objective loss `0.726089180`
  - field L1 loss `0.726069331`
  - length `0.096883804 m`
  - diameter `8.000397123 mm`
  - local center x `0.593514740 m`
  - center depth `1.493994951 m`
  - background epsr `3.329753876`
  - anomaly delta epsr `0.955114782`
  - time shift `2.407616138 ns`
- Near-best ranges:
  - length `0.096883804-0.096884944 m`
  - diameter `8.000397123-11.999597773 mm`
  - local center x `0.593512177-0.593514740 m`
  - center depth `1.493994951-1.494006634 m`
  - background epsr `3.329753876-3.329767466`
  - anomaly delta epsr `0.955063879-0.955114782`
- Gradients:
  - radius `1.568614794e-09`
  - length `1.156706057e-04`
  - time shift `2.647856623e-02`
  - local x `9.463938113e-06`
  - depth `1.164953646e-04`
  - background epsr `4.925021203e-04`
  - anomaly delta epsr `1.047068872e-04`
- Runtime:
  - mean iteration runtime range `10.708-10.890 s`

## What Remains Blocked

- Diameter is still not identified: the near-best range spans `8-12 mm`, and the radius gradient remains negligible.
- The best fit improved mostly through source-time shift, background/material, depth, and length, not radius.
- The `0.2 m` length seed remains a worse local basin near `0.195 m`.
- The claim remains receiver-mean scattered-objective-specific; full-field L1 was flat in the forward contrast branch.

## Current Decision

This is the current best real-field 0701 optimizer benchmark:

- finite length candidate near `0.097 m`;
- local depth near `1.494 m`;
- background epsr near `3.33`;
- source time shift near `2.41 ns`;
- diameter stays a near-best range of about `8-12 mm`.

## Next Defensible Task

The next radius-focused branch should add information that radius can actually affect:

- antenna/source-shape parameters,
- multiple event windows,
- or a multi-profile/multi-window objective that includes additional waveform regions.

Do not keep repeating length/diameter-only loops; they have repeatedly shown negligible radius gradient.

## Validation And Resources

- Product/synthesis/optimizer tests:
  - `21 passed`
- Expanded focused suite:
  - `52 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile ...`
  - passed for changed scripts/tests
- touched-file `git diff --check`
  - passed
- Figure checks:
  - `250.../figures/field_3d_0701_finite_length_optimizer_seed_stability.png`: size `(2365, 767)`, stddev `64.108`
  - `058.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, stddev `64.402`

## Artifact Paths

- Joint stability synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/250_field_3d_0701_finite_length_joint_xz_material_optimizer_seed_stability`
- Updated shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/058_field_prediction_shipping_snapshot`
- Checkpoint:
  - `docs/update/summary/328_2026-07-04_field_3d_0701_joint_xz_material_optimizer_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
