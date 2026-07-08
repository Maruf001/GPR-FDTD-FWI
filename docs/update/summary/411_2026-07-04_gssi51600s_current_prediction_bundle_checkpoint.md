# 2026-07-04 GSSI 51600S Current Prediction Bundle Checkpoint

## What changed

- Added a compact current prediction bundle so the GSSI result can be reviewed without chasing separate experiment folders.
- New script and test:
  - `run_gssi51600s_current_prediction_bundle.py`
  - `tests/test_gssi51600s_current_prediction_bundle.py`
- New artifact:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/109_gssi51600s_current_prediction_bundle`

## Bundle contents

- `README.md`
- `data/gssi51600s_current_prediction_bundle_summary.json`
- `data/gssi51600s_current_prediction_pretty.txt`
- copied figures:
  - `figures/gssi51600s_release_style_prediction_card.png`
  - `figures/gssi51600s_profile_spacing_estimator_card.png`
- frozen source snapshots:
  - `run_gssi51600s_current_prediction_bundle.py`
  - `run_field_prediction_current_query.py`
  - `run_gssi51600s_release_style_prediction_card.py`
  - `run_gssi51600s_profile_spacing_estimator_card.py`

## Key product output

The bundle reports the current trusted GSSI field-data prediction as:

- tier: `transfer_needs_confirmation`
- x/y/z: `0.413941 / 0.16 assumed / 0.120349 m`
- finite length range: `0.183166-0.216163 m`
- diameter range: `17.2954-17.8126 mm`
- relative permittivity estimate: `1.97913`
- conductivity estimate: `0.00266249 S/m`
- crossline decision: `crossline_geometry_controls_length_do_not_ship_single_length`
- offset-conditioned near-best length range: `0.183524-0.217334 m`

## Current decision

The bundle decision is:

`current_gssi51600s_prediction_bundle_confirmation_needed`

This is the current product-facing deliverable state: a concrete candidate and fitted material/geometry estimates are available, but the finite-length claim remains conditioned on unconfirmed crossline profile geometry.

## What remains blocked

- Crossline profile coordinates remain the release blocker.
- The bundle is ready for review, but not as a release-promoted single-length claim.

## Next defensible task

Continue only with work that reduces or communicates crossline-coordinate uncertainty: acquisition-note search, metadata confirmation, profile-position optimizer, or advisor-facing explanation around the current bundle.

## Validation/resource checks

- `python run_gssi51600s_current_prediction_bundle.py --run-name gssi51600s_current_prediction_bundle` generated artifact `109`.
- `python -m py_compile run_gssi51600s_current_prediction_bundle.py` passed.
- `python -m pytest tests/test_gssi51600s_current_prediction_bundle.py -q` passed: `1 passed`.
- Bundle contents and pretty prediction text were inspected.
- Marathon request remains active; continue toward crossline-coordinate confirmation or review packaging.
