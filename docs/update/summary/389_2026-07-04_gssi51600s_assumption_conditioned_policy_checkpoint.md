# GSSI51600S Assumption-Conditioned Policy Checkpoint

## What Changed

- Added an explicit opt-in policy flag to the range-release policy script: `--allow-assumed-y-geometry`.
- Default strict policy remains blocked when crossline y geometry is not metadata-confirmed.
- The opt-in policy allows a policy-conditional range-release candidate only when the remaining required-check failure is the assumed crossline y geometry, while preserving provenance checks.
- Generated an assumption-conditioned policy artifact and matching range-release card for the current GSSI detector-window candidate.

## Key Numbers

- Strict current default audit: `product_defaults_ready`, with release blocked by `crossline_y_geometry_confirmed`.
- Opt-in policy decision: `range_release_policy_candidate`.
- Opt-in range card decision: `range_release_candidate_card_ready`.
- Opt-in tier for GSSI query: `policy_conditional_range_release_candidate`.
- Current assumption-conditioned geometry/material values:
  - x: `0.414366 m`.
  - assumed y: `0.240000 m`.
  - cover depth: `0.120389 m`.
  - length range: `0.183144-0.183513 m`.
  - diameter range: `17.293125-17.296124 mm`.
  - top-margin relative permittivity range: `2.011180-2.046360`.
  - top-margin background conductivity range: `0.002658729-0.007476822 S/m`.

## Current Decision

There are now two clean reporting modes. The strict product default is not release-promoted because crossline profile spacing is not metadata-confirmed. The optional assumption-conditioned card can be used to report the current best field-data prediction if the audience accepts the y-spacing assumption explicitly.

## Validation

- `python -m pytest tests/test_field_prediction_release_policy_variant.py tests/test_field_prediction_range_release_candidate_card.py tests/test_field_prediction_product_default_audit.py -q` passed with `10 passed`.
- `python -m py_compile run_field_prediction_release_policy_variant.py` passed.
- The assumption-conditioned query prints `policy_conditional_range_release_candidate` and carries the y-geometry caveat in the claim boundary.

## Artifact Paths

- Opt-in policy: `outputs/validation_exp_on_field_data/product_leaderboard/229_field_prediction_release_policy_variant_gssi51600s_detector_window_assumption_conditioned_candidate/`.
- Opt-in range card: `outputs/validation_exp_on_field_data/product_leaderboard/230_field_prediction_range_release_candidate_card_gssi51600s_detector_window_assumption_conditioned_candidate/`.
- Strict current default audit: `outputs/validation_exp_on_field_data/product_leaderboard/228_field_prediction_product_default_audit_gssi51600s_detector_window_sensitivity_candidate/`.

## Next Defensible Task

Use the assumption-conditioned card to prepare a compact advisor-facing prediction table while continuing to seek or reconstruct the actual crossline profile spacing.

The local marathon request remains active.
