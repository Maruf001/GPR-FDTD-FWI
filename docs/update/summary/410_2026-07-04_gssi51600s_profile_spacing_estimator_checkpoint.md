# 2026-07-04 GSSI 51600S Profile-Spacing Estimator Checkpoint

## What changed

- Added a lightweight profile-spacing estimator card derived from the explicit offset scan rows.
- This is not another FDTD run; it turns the scan into a product-facing uncertainty map.
- New script and test:
  - `run_gssi51600s_profile_spacing_estimator_card.py`
  - `tests/test_gssi51600s_profile_spacing_estimator_card.py`
- New artifact:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/108_gssi51600s_profile_spacing_estimator_card_current`

## Key numbers

- Decision: `spacing_objective_flat_keep_geometry_conditioned_prediction`
- Field-L1 best spacing: `0.22 m`
- Best field L1: `0.961135685`
- Best length at field-L1 optimum: `0.183524072 m`
- Near-flat spacing interval using `2.5e-4` field-L1 tolerance:
  - `0.16-0.28 m`
- Near-flat length interval:
  - `0.183524072-0.217333928 m`
- Branch transition over all scan rows:
  - `0.20-0.22 m`
- Flat interval width:
  - `0.12 m`

## Current decision

The spacing scan does not identify a unique crossline spacing. It provides a useful uncertainty map: the compressed `0.10 m` case is poor, but the `0.16-0.28 m` interval is flat enough that finite length remains geometry-conditioned. This supports reporting a range rather than one finite length.

## What remains blocked

- The product still needs measured crossline profile coordinates or an explicit position optimizer before claiming a unique finite length.
- The spacing estimator and release-style prediction card are now ready as confirmation-needed deliverables.

## Next defensible task

Prepare the current GSSI prediction package for review: current-query output, release-style card, spacing-estimator card, and claim-boundary language. Continue only with additional computation if it directly reduces the crossline-coordinate uncertainty.

## Validation/resource checks

- `python run_gssi51600s_profile_spacing_estimator_card.py --run-name gssi51600s_profile_spacing_estimator_card_current` generated artifact `108`.
- `python -m py_compile run_gssi51600s_profile_spacing_estimator_card.py` passed.
- `python -m pytest tests/test_gssi51600s_profile_spacing_estimator_card.py -q` passed: `2 passed`.
- Figure `108/.../figures/gssi51600s_profile_spacing_estimator_card.png` was visually inspected.
- Marathon request remains active; continue toward review packaging or crossline-coordinate reduction.
