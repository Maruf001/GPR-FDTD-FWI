# 452 - 2026-07-05 - GSSI 51600S Two-Event Tiny-Gain Gate Checkpoint

## Purpose

Supersede the first fixed two-event gate by testing a second fixed placement from the middle profile-pair candidate, then integrate the result into the current GSSI 51600S prediction bundle.

## Implementation

- Reused the fixed second-event support in `run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py`.
- Compared two fixed second-event placements against the full-four-profile single-target baseline.
- Kept the main event optimized for x, cover depth, diameter, finite length, material, conductivity, and time shift.
- Kept the second event fixed for this gate; this is a placement/contrast diagnostic, not yet an optimized two-event product model.

## Field Runs

- Single-target full-four-profile baseline:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/519_gssi51600s_finite_length_3d_full4profiles_uniform_y016_domainz070_adamw_prior_windows50_54_58_62_66_iter24`
  - Best field L1: `0.9726306796073914`
  - Best objective: `0.9825726747512817`
- Fixed deep second event:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/520_gssi51600s_finite_length_3d_full4profiles_y016_domainz070_adamw_prior_two_event_deep_p23_windows50_54_58_62_66_iter24`
  - Field L1 delta vs single target: `0.0397607684135437`
  - Objective delta vs single target: `0.042269110679626465`
- Fixed middle second event:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/521_gssi51600s_finite_length_3d_full4profiles_y016_domainz070_adamw_prior_two_event_mid_p13_windows50_54_58_62_66_iter24`
  - Fixed second-event x: `0.501308` m
  - Fixed second-event cover depth: `0.138297` m
  - Fixed second-event crossline center: `0.43` m
  - Fixed second-event diameter: `17.418` mm
  - Fixed second-event length: `0.185664` m
  - Best field L1: `0.9707207083702087`
  - Best objective: `0.9847766757011414`
  - Field L1 delta vs single target: `-0.0019099712371826172`
  - Objective delta vs single target: `0.002204000949859619`

## Current Decision

The fixed middle second-event candidate gives a tiny field-L1 improvement but a slightly worse regularized objective. The fixed deep candidate is clearly worse. The current decision is:

`fixed_two_event_candidate_tiny_field_gain_not_promoted`

This keeps the full-four-profile single-target run as the baseline and keeps the two-event interpretation unpromoted until the second event has optimized placement or contrast.

## Product Integration

- Updated two-event gate card:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/184_gssi51600s_two_event_gate_card_current`
- Updated current GSSI prediction bundle:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/185_gssi51600s_current_prediction_bundle_with_two_event_tiny_gain_gate`
- Latest pointer:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- User-facing query:
  - `python run_field_prediction_current_query.py --dataset gssi51600s --format pretty`
- Query now reports:
  - `two_event_gate_decision: fixed_two_event_candidate_tiny_field_gain_not_promoted`
  - `two_event_field_l1_delta_vs_single: -0.0019099712371826172`
  - `two_event_objective_delta_vs_single: 0.002204000949859619`

## Dataset Boundary

The current deliverable source remains `data/2026-06-09_GSSI_model_51600S`. The separate `data/2025-01-13_GPR_Dataset` archive is treated as a mixed external archive and is not used as trusted GSSI rebar evidence unless a run explicitly targets a verified rebar branch.

## Validation

- Compile check passed under `conda run -n gpr-fdtd-fwi`.
- Focused tests passed: `20 passed, 1 skipped`.
- Broader GSSI/card suite passed: `155 passed, 1 skipped`.
- `git diff --check` passed on touched files.
- Two-event gate figure sanity:
  - `(1753, 1175)`, nonblank grayscale range `0-255`.

## Next Defensible Task

Add an optimized or at least contrast-scaled second-event branch. The current fixed second-event model is too rigid: one fixed placement worsens the fit, and the other gives only a tiny field-L1 gain with a worse total objective.

The marathon request remains active.
