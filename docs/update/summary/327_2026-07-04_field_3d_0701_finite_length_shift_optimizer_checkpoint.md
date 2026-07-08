# Field 3D 0701 Finite-Length Shift Optimizer Checkpoint

## What Changed

- Extended the finite-length scattered optimizer with optional bounded source-time shift optimization.
- Ran three real 0701 shift-enabled optimizer stresses.
- Added shift-aware synthesis fields for best field loss, time-shift range, shift gradient, and loss-key tracking.
- Updated the shipping snapshot so the product row reports the shift-enabled fit improvement while keeping diameter as a range.

## Key Numbers

- Shift-enabled optimizer runs:
  - `242...seed_len010_diam08_adamw_iter3`
  - `243...seed_len010_diam12_adamw_iter3`
  - `244...seed_len020_diam08_adamw_iter3`
- Shift-stability synthesis:
  - `246_field_3d_0701_finite_length_shift_optimizer_seed_stability`
- Shipping snapshot:
  - `057_field_prediction_shipping_snapshot`
- Synthesis decision:
  - `finite_length_shift_stability_supports_010m_length_not_diameter`
- Best shift-enabled run:
  - label `len010_diam08_adamw_shift`
  - objective loss `0.729932129`
  - field L1 loss `0.729852617`
  - best finite length `0.093914755 m`
  - best diameter `8.000394329 mm`
  - best time shift `2.507375240 ns`
  - best improvement vs infinite reference `0.192401826`
- Near-best shift runs:
  - `len010_diam08_adamw_shift`
  - `len010_diam12_adamw_shift`
- Near-best ranges:
  - length `0.093914755-0.093917228 m`
  - diameter `8.000394329-11.999594048 mm`
  - time shift `2.507375240-2.507606030 ns`
- Gradients:
  - max raw radius gradient `1.566602181e-09`
  - max raw length gradient `1.197250094e-04`
  - max raw shift gradient `2.479810268e-02`
- Runtime:
  - mean iteration runtime range `5.264-5.727 s`

## What Remains Blocked

- Time-shift optimization improves fit quality, but it does not make diameter identifiable.
- Radius gradient remains near zero; the active gradients are time shift and finite length.
- The `0.2 m` length seed remains in a worse local basin at about `0.19 m`, so length should remain a provisional candidate plus seed-sensitivity note.
- Full-field L1 was already shown flat in the finite-length forward branch, so the claim remains receiver-mean scattered-objective-specific.

## Current Decision

The best current product statement for 0701 is:

- x/y/z/material row remains the promoted real-field row;
- finite length has a seed-stable receiver-mean scattered candidate near `0.094 m`;
- bounded source-time shift improves field fit substantially, with best shift near `2.51 ns`;
- diameter remains `8-12 mm` near-best range, not a unique prediction.

## Next Defensible Task

Do not spend more time on length/diameter-only or shift-only loops. The next branch should target the missing radius gradient directly:

- add bounded x/z/material co-optimization around the promoted row, or
- add source/antenna shape parameters, then
- report whether radius gradient becomes non-negligible and whether the near-best diameter range narrows.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `18 passed`
- Expanded focused suite:
  - `49 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile ...`
  - passed for changed scripts/tests
- touched-file `git diff --check`
  - passed
- Figure checks:
  - `246.../figures/field_3d_0701_finite_length_optimizer_seed_stability.png`: size `(2361, 767)`, stddev `62.344`
  - `057.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, stddev `64.402`

## Artifact Paths

- Shift-stability synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/246_field_3d_0701_finite_length_shift_optimizer_seed_stability`
- Updated shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/057_field_prediction_shipping_snapshot`
- Checkpoint:
  - `docs/update/summary/327_2026-07-04_field_3d_0701_finite_length_shift_optimizer_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
