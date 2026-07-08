# Field 3D 0701 Joint Source-Frequency Sensitivity Checkpoint

## What Changed

- Added source-frequency tracking to finite-length joint optimizer summaries.
- Ran source-frequency proxy stresses on the best late-window joint objective.
- Added a source-frequency sensitivity synthesis artifact.
- Updated the shipping snapshot with the current best source-frequency benchmark.

## Key Numbers

- Source-frequency runs:
  - `252...source25_diam08` (implicit/default `25 MHz`)
  - `254...source20_diam08`
  - `255...source35_diam08`
  - `256...source20_diam12`
- Synthesis artifact:
  - `257_field_3d_0701_joint_source_frequency_sensitivity`
- Shipping snapshot:
  - `060_field_prediction_shipping_snapshot`
- Synthesis decision:
  - `source_frequency_improves_fit_but_diameter_range_persists`
- Best source-frequency proxy:
  - `20 MHz`
  - best field L1 loss `0.600213468`
- Field L1 loss range:
  - `0.600213468-0.741837442`
- Near-best rows:
  - `source20_diam08`
  - `source20_diam12`
- Near-best ranges:
  - diameter `8.000393398-11.999592185 mm`
  - length `0.096881479-0.096881971 m`
- Max gradients:
  - radius `3.032321505e-09`
  - length `4.968798748e-05`
  - source-time shift `1.951476932e-02`
  - background epsr `7.952183951e-04`

## What Remains Blocked

- The 20 MHz source proxy improves fit substantially, but it still does not identify diameter.
- Both `8 mm` and `12 mm` diameter seeds remain near-best at 20 MHz.
- Radius gradient remains negligible relative to material/shift gradients.

## Current Decision

The current best real-field 0701 benchmark is:

- late window;
- joint x/z/material/source-time optimizer;
- 20 MHz source-frequency proxy;
- finite length near `0.0969 m`;
- diameter reported as `8-12 mm` near-best range, not a scalar.

## Next Defensible Task

To make progress on diameter, the next branch needs different information content:

- richer antenna/source-shape parameters beyond only Ricker center frequency;
- combined multi-window objective with source-shape parameters;
- or external labeled/caliper data to calibrate diameter.

## Validation And Resources

- Source-frequency tests:
  - `3 passed`
- Source-frequency shipping tests:
  - `16 passed`
- Expanded focused suite:
  - `60 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile ...`
  - passed for changed scripts/tests
- touched-file `git diff --check`
  - passed
- Figure checks:
  - `257.../figures/field_3d_0701_joint_source_frequency_sensitivity.png`: size `(2331, 750)`, stddev `63.574`
  - `060.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, stddev `64.402`

## Artifact Paths

- Source-frequency sensitivity:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/257_field_3d_0701_joint_source_frequency_sensitivity`
- Updated shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/060_field_prediction_shipping_snapshot`
- Checkpoint:
  - `docs/update/summary/330_2026-07-04_field_3d_0701_joint_source_frequency_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
