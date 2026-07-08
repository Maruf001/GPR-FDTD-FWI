# Field 3D 0701 Finite-Length Seed Stability Checkpoint

## What Changed

- Ran finite-length optimizer seed and optimizer-family stresses on the real 0701 field stack.
- Added a synthesis script and product artifact for the finite-length stability decision.
- Updated the shipping snapshot so the product row now reports the seed-stable length candidate and the diameter-not-identified boundary.

## Key Numbers

- Stress runs:
  - `237...seed_len010_diam08_adamax_iter3`
  - `238...seed_len020_diam08_adamax_iter3`
  - `239...seed_len010_diam12_adamax_iter3`
  - `240...seed_len010_diam08_adamw_iter3`
- Synthesis artifact:
  - `241_field_3d_0701_finite_length_optimizer_seed_stability`
- Synthesis decision:
  - `finite_length_seed_stability_supports_010m_length_not_diameter`
- Best run:
  - label `len010_diam08_adamw`
  - optimizer `adamw`
  - best loss `0.7659777999`
  - best finite length `0.0939193368 m`
  - best diameter `8.000395261 mm`
- Near-best runs:
  - `len010_diam08_adamax`
  - `len010_diam12_adamax`
  - `len010_diam08_adamw`
- Near-best ranges:
  - length `0.0939193368-0.0940583721 m`
  - diameter `8.000395261-11.999594979 mm`
- All-run length range:
  - `0.0939193368-0.1903205961 m`
- Gradient diagnostics:
  - max raw length gradient `1.535193151e-04`
  - max raw radius gradient `1.399438898e-09`
- Runtime:
  - mean iteration runtime range `5.453-5.720 s`

## What Remains Blocked

- The `0.2 m` length seed stayed in a worse local basin at about `0.19 m`, so the shipped length must remain provisional and seed-scoped.
- Diameter still cannot be claimed from this objective: near-best diameter spans the tested `8-12 mm`, and the radius gradient is negligible.
- The finite-length evidence is still based on the receiver-mean scattered objective; full-field L1 remained flat in the preceding forward contrast.

## Current Decision

The real-field 0701 product can now report a stronger provisional finite-length candidate:

- finite-length candidate near `0.094 m`;
- x/y/z/epsr inherited from the promoted 0701 row;
- diameter retained as a range/top-candidate, not an identified scalar;
- conductivity/epsr still product fields from the existing promoted adaptive row.

## Next Defensible Task

Attack the diameter failure directly by adding richer fit dimensions:

- keep the seed-stable finite-length candidate as a product guard;
- add bounded source/time-shift or x/z/material updates into the finite-length scattered objective;
- measure whether radius gradient becomes non-negligible;
- compare AdamW/Adamax behavior and runtime;
- only promote diameter if the near-best diameter range narrows under these stresses.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`
  - `4 passed`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_shipping_snapshot.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`
  - `13 passed`
- Expanded focused suite:
  - `46 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile ...`
  - passed for changed scripts/tests
- touched-file `git diff --check`
  - passed
- Figure checks:
  - `241.../figures/field_3d_0701_finite_length_optimizer_seed_stability.png`: size `(2363, 767)`, stddev `62.969`
  - `055.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, stddev `64.402`

## Artifact Paths

- Seed-stability synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/241_field_3d_0701_finite_length_optimizer_seed_stability`
- Updated shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/055_field_prediction_shipping_snapshot`
- Checkpoint:
  - `docs/update/summary/326_2026-07-04_field_3d_0701_finite_length_seed_stability_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
