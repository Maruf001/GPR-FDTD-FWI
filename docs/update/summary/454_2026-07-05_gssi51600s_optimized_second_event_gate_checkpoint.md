# 454 - 2026-07-05 - GSSI 51600S Optimized Second-Event Gate Checkpoint

## Purpose

Test whether the current GSSI 51600S full-four-profile fit improves when the second event is not fixed manually, but instead optimized directly inside the AdamW field objective.

## Implementation

- Extended `run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py` with `--optimize-second-event`.
- When enabled, AdamW updates:
  - second-event x position,
  - second-event cover depth,
  - second-event crossline center,
  - second-event strength.
- The existing fixed-second-event behavior remains the default.
- The optimizer summary now records optimized second-event gradients, best values, and final values.
- The two-event gate card now reports fixed, strength-scaled, and optimized second-event candidates in one comparison.

## Field Runs

- Smoke run:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/525_gssi51600s_finite_length_3d_full4profiles_y016_domainz070_adamw_prior_two_event_mid_p13_opt_second_smoke_iter2`
  - Finite gradients: `True`
  - Final second-event x: `0.5033367793047132` m
  - Final second-event cover depth: `0.13584675377957045` m
  - Final second-event crossline center: `0.4341160888208236` m
  - Final second-event strength: `0.8421787782912856`
- Interrupted full run:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/526_gssi51600s_finite_length_3d_full4profiles_y016_domainz070_adamw_prior_two_event_mid_p13_opt_second_windows50_54_58_62_66_iter24`
  - No summary or manifest; left untouched for provenance.
- Clean full rerun:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/527_gssi51600s_finite_length_3d_full4profiles_y016_domainz070_adamw_prior_two_event_mid_p13_opt_second_windows50_54_58_62_66_iter24_rerun`
  - Best field L1: `0.9738926291465759`
  - Best objective: `0.987990140914917`
  - Best main-event x: `0.5015993118286133` m
  - Best main-event cover depth: `0.12442204356193542` m
  - Best main-event diameter: `17.19588041305542` mm
  - Best main-event length: `0.1663692593574524` m
  - Best background epsr: `2.1888628005981445`
  - Best conductivity: `0.0028797071427106857` S/m
  - Final optimized second-event x: `0.49404993674364067` m
  - Final optimized second-event cover depth: `0.12356718424625479` m
  - Final optimized second-event crossline center: `0.44034244671618916` m
  - Final optimized second-event strength: `0.7644892442975081`

## Comparison

- Single-target full-four-profile baseline:
  - Field L1: `0.9726306796073914`
  - Objective: `0.9825726747512817`
- Optimized second-event candidate:
  - Field L1 delta vs single: `0.0012619495391845703`
  - Objective delta vs single: `0.005417466163635254`
- Best fixed middle second-event candidate:
  - Field L1 delta vs single: `-0.0019099712371826172`
  - Objective delta vs single: `0.002204000949859619`

## Current Decision

Do not promote a two-event product claim. Full-strength fixed placement gives only a tiny field-L1 gain with worse regularized objective; attenuated fixed strengths do not improve the objective; and the tested optimized second-event placement is also worse than the single-target baseline.

Current gate decision:

`fixed_two_event_candidate_tiny_field_gain_not_promoted`

## Product Integration

- Optimized two-event gate card:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/191_gssi51600s_two_event_optimized_gate_card_current`
- Current GSSI prediction bundle:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/192_gssi51600s_current_prediction_bundle_with_two_event_optimized_gate`
- Latest pointer:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- User-facing query:
  - `python run_field_prediction_current_query.py --dataset gssi51600s --format pretty`

## Dataset Boundary

The current deliverable source remains `data/2026-06-09_GSSI_model_51600S`. The separate `data/2025-01-13_GPR_Dataset` archive remains out of the trusted GSSI rebar claim unless a future run explicitly targets and verifies one of its rebar branches.

## Validation

- Compile checks passed under `/home/lam002/miniforge3/bin/python`.
- Focused tests passed: `7 passed`.
- Broader GSSI/card suite passed: `160 passed`.
- `git diff --check` passed on touched files.
- Figure sanity:
  - Optimized second-event run: `(1957, 767)`, nonblank grayscale range `0-255`.
  - Gate figure: `(1751, 1175)`, nonblank grayscale range `0-255`.
  - Bundle figure copy: `(1751, 1175)`, nonblank grayscale range `0-255`.

## Next Defensible Task

Move away from local two-event placement tests. The next product-relevant branch is source/time alignment or a y-dependent target model that can explain the shallow, middle, and deeper adjacent-profile depth progression without adding a second reflector that worsens the regularized objective.

The marathon request remains active.
