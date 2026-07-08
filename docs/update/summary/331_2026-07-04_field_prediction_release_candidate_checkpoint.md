# Field Prediction Release Candidate Checkpoint

## What Changed

- Added a compact release-candidate exporter:
  - `run_field_prediction_release_candidate.py`
- Generated a product-facing release candidate from shipping snapshot `060`.
- The release candidate distills the optimizer evidence into one row per dataset with prediction fields, ranges, fit score, and claim boundary.

## Key Numbers

- Release artifact:
  - `061_field_prediction_release_candidate`
- Decision:
  - `release_candidate_export_ready`
- Current best 0701 real-field 3D candidate:
  - x `9.819386151981593 m`
  - y `1.5 m`
  - z/depth `1.493994951248169 m`
  - local optimizer x `0.5935147404670715 m`
  - finite length range `0.096881479-0.096881971 m`
  - diameter range `8.000393398-11.999592185 mm`
  - background epsr `3.329753875732422`
  - anomaly delta epsr `0.9551147818565369`
  - background conductivity `0.00377632980234921 S/m`
  - source-frequency proxy `20 MHz`
  - field L1 fit `0.600213468`
  - max radius gradient `3.032321505e-09`
- GSSI51600S row:
  - exported as `limited_surface_bscan_candidate`
  - x/z/material candidate retained
  - no y/finite-length/3D claim

## What Remains Blocked

- The release candidate still does not claim unique diameter.
- Diameter is reported as a near-best range because all optimizer stresses still show negligible radius gradient.
- GSSI remains surface-B-scan limited without crossline y/length support.

## Current Decision

This is the current product-facing deliverable:

- Use `061_field_prediction_release_candidate` for the clean prediction table.
- Use `060_field_prediction_shipping_snapshot` for full evidence and claim-boundary trace.
- Use `257_field_3d_0701_joint_source_frequency_sensitivity` as the current best optimizer benchmark backing the 0701 row.

## Next Defensible Task

Continue product hardening by either:

- adding a deterministic CLI around the release candidate for one-command prediction export;
- building a combined multi-window/source-shape objective;
- or bringing in labeled/caliper data to calibrate the diameter range.

## Validation And Resources

- Release-candidate tests:
  - `2 passed`
- Product-focused suite:
  - `62 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile ...`
  - passed for changed scripts/tests
- touched-file `git diff --check`
  - passed
- Figure check:
  - `061.../figures/field_prediction_release_candidate.png`: size `(2263, 750)`, stddev `62.954`

## Artifact Paths

- Release candidate:
  - `outputs/validation_exp_on_field_data/product_leaderboard/061_field_prediction_release_candidate`
- Source-frequency benchmark:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/257_field_3d_0701_joint_source_frequency_sensitivity`
- Shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/060_field_prediction_shipping_snapshot`
- Checkpoint:
  - `docs/update/summary/331_2026-07-04_field_prediction_release_candidate_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
