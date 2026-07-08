# 2026-07-04 GSSI 51600S Release-Style Prediction Card Checkpoint

## What changed

- Added a release-style GSSI prediction card that packages the current candidate prediction and the geometry-conditioned finite-length map in one artifact.
- New script and test:
  - `run_gssi51600s_release_style_prediction_card.py`
  - `tests/test_gssi51600s_release_style_prediction_card.py`
- Initial card `106` exposed an all-row branch-transition issue; corrected card `107` uses the near-best offset rows for the transition interval.
- Current artifact:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/107_gssi51600s_release_style_prediction_card_current`

## Key numbers

- Decision: `gssi51600s_prediction_card_confirmation_needed`
- Candidate location:
  - x: `0.413941 m`
  - y: `0.160000 m` assumed
  - cover depth z: `0.120349 m`
- Current conservative finite-length range:
  - `0.183165550-0.216162652 m`
- Current conservative diameter range:
  - `17.295353-17.812613 mm`
- Material estimates from the current product default:
  - relative permittivity: `1.979135`
  - conductivity: `0.00266249 S/m`
- Refined profile-offset near-best spacing range:
  - `0.16-0.28 m`
- Near-best branch transition interval:
  - `0.20-0.22 m`
- Offset-conditioned near-best length range:
  - `0.183524072-0.217333928 m`

## Current decision

The predictor now has a product-style output card, but the claim remains confirmation-needed. The card reports a candidate location, diameter, permittivity, conductivity, and finite-length range while explicitly stating that a single finite length should not be promoted until crossline profile coordinates are measured or optimized.

## What remains blocked

- No measured crossline profile coordinates are available in the trusted GSSI metadata inspected so far.
- The offset-conditioned loss curve is nearly flat across `0.16-0.28 m`, so the spacing estimate is not unique.
- The next release step is not more window/shift diagnostics; it is crossline coordinate confirmation or an explicit profile-position optimizer.

## Next defensible task

Implement a small profile-position optimization/scan layer that treats crossline offsets as parameters and reports uncertainty directly, or prepare the prediction card as the advisor-facing current deliverable while clearly labeling it as confirmation-needed.

## Validation/resource checks

- `python run_gssi51600s_release_style_prediction_card.py --run-name gssi51600s_release_style_prediction_card_current` generated artifact `107`.
- `python -m py_compile run_gssi51600s_release_style_prediction_card.py` passed.
- `python -m pytest tests/test_gssi51600s_release_style_prediction_card.py -q` passed: `2 passed`.
- Figure `107/.../figures/gssi51600s_release_style_prediction_card.png` was visually inspected.
- Marathon request remains active; continue toward explicit profile-position estimation or advisor-facing packaging.
