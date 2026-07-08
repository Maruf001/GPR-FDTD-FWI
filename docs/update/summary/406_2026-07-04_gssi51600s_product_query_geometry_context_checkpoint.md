# 2026-07-04 GSSI 51600S Product Query Geometry Context Checkpoint

## What changed

- Updated `run_field_prediction_current_query.py` so the `gssi51600s` predictor output includes the latest geometry-context claim cards.
- The query still keeps the conservative product tier, but now reports:
  - crossline geometry decision
  - best offset-conditioned spacing
  - offset-conditioned near-best finite-length range
  - window-family decision
  - shift/residual decision
  - geometry product action
- Updated `tests/test_field_prediction_current_query.py` for the new fields and merge logic.

## Key numbers now shown by the product query

Current query command:

`python run_field_prediction_current_query.py --dataset gssi51600s --format pretty`

New geometry-context lines:

- `crossline_geometry_decision: crossline_geometry_controls_length_do_not_ship_single_length`
- `profile_offset_best_spacing_m: 0.24`
- `profile_offset_best_length_y_m: 0.183567`
- `profile_offset_near_best_length_y_m: 0.183567 - 0.216164`
- `window_family_decision: do_not_collapse_profile_window_range_window_family_preserves_subset_split`
- `window_family_subset_length_gap_m: 0.0264088`
- `shift_residual_decision: do_not_tighten_product_range_shift_relaxation_preserves_long_branch`

The core conservative output remains:

- tier: `transfer_needs_confirmation`
- length range: `0.183166-0.216163 m`
- diameter range: `17.2954-17.8126 mm`
- top-margin candidate: length `0.183175 m`, diameter `17.2954 mm`, relative permittivity `1.97913`, conductivity `0.00266249 S/m`

## Current decision

The query now behaves more like a product-facing predictor: it reports the best current candidate and directly states why a single finite length is not shipped yet. The product default remains conservative and assumption-conditioned.

## What remains blocked

- Crossline profile coordinates remain unconfirmed.
- The query reports geometry context but does not yet run a profile-position optimizer.
- A release-style claim still needs either measured profile positions or an explicit crossline-coordinate fit.

## Next defensible task

Implement or run a bounded profile-position optimizer/scan so the product can estimate crossline geometry instead of only conditioning on tested spacings.

## Validation/resource checks

- `python -m py_compile run_field_prediction_current_query.py` passed.
- `python -m pytest tests/test_field_prediction_current_query.py -q` passed: `5 passed`.
- `python run_field_prediction_current_query.py --dataset gssi51600s --format pretty` confirmed the new geometry-context output.
- Marathon request remains active; continue toward explicit crossline-position estimation.
