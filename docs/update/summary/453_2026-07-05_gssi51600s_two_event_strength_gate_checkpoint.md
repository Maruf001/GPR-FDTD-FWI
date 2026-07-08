# 453 - 2026-07-05 - GSSI 51600S Two-Event Strength Gate Checkpoint

## Purpose

Test whether the fixed middle second event from the GSSI 51600S full-four-profile stack becomes useful when its contrast is attenuated instead of forced to the same full material contrast as the main event.

## Implementation

- Added `--second-event-strength` to `run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py`.
- Strength is fixed per run and bounded to `[0, 1]`.
- The previous behavior is preserved as strength `1.0`.
- The two-event gate card now accepts additional labeled two-event summaries and records `second_event_strength`.
- Older two-event summaries without the field are interpreted as strength `1.0` when `use_second_event` is true.

## Field Runs

- Baseline single-target full-four-profile run:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/519_gssi51600s_finite_length_3d_full4profiles_uniform_y016_domainz070_adamw_prior_windows50_54_58_62_66_iter24`
  - Best field L1: `0.9726306796073914`
  - Best objective: `0.9825726747512817`
- Full-strength fixed middle second event:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/521_gssi51600s_finite_length_3d_full4profiles_y016_domainz070_adamw_prior_two_event_mid_p13_windows50_54_58_62_66_iter24`
  - Strength: `1.0`
  - Field L1 delta vs single: `-0.0019099712371826172`
  - Objective delta vs single: `0.002204000949859619`
- Attenuated fixed middle second event:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/524_gssi51600s_finite_length_3d_full4profiles_y016_domainz070_adamw_prior_two_event_mid_p13_strength075_windows50_54_58_62_66_iter24`
  - Strength: `0.75`
  - Best field L1: `0.9731767773628235`
  - Best objective: `0.9847609400749207`
  - Field L1 delta vs single: `0.0005460977554321289`
  - Objective delta vs single: `0.002188265323638916`
- Attenuated fixed middle second event:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/523_gssi51600s_finite_length_3d_full4profiles_y016_domainz070_adamw_prior_two_event_mid_p13_strength050_windows50_54_58_62_66_iter24`
  - Strength: `0.5`
  - Best field L1: `0.9756097197532654`
  - Best objective: `0.9854748249053955`
  - Field L1 delta vs single: `0.0029790401458740234`
  - Objective delta vs single: `0.0029021501541137695`

## Current Decision

The fixed-strength scan does not promote a two-event product claim. Full strength gives a tiny field-L1 gain but a worse regularized objective, while attenuated strengths `0.75` and `0.5` do not improve the objective or field fit relative to the single-target baseline.

Current decision:

`fixed_two_event_candidate_tiny_field_gain_not_promoted`

## Product Integration

- Strength-aware two-event gate:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/189_gssi51600s_two_event_strength_gate_card_current`
- Current GSSI prediction bundle:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/190_gssi51600s_current_prediction_bundle_with_two_event_strength_gate`
- Latest pointer:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- User-facing query:
  - `python run_field_prediction_current_query.py --dataset gssi51600s --format pretty`
- Query now reports the fixed-strength scan boundary and keeps the fixed two-event geometry unpromoted.

## Dataset Boundary

The current deliverable source remains `data/2026-06-09_GSSI_model_51600S`. The separate `data/2025-01-13_GPR_Dataset` archive remains out of the trusted GSSI rebar claim unless a future run explicitly targets and verifies one of its rebar branches.

## Validation

- Compile checks passed under `/home/lam002/miniforge3/bin/python`.
- Focused tests passed: `6 passed`.
- Broader GSSI/card suite passed: `159 passed`.
- `git diff --check` passed on touched files.
- Figure sanity:
  - Strength gate figure: `(1753, 1175)`, nonblank grayscale range `0-255`.
  - Bundle figure copy: `(1753, 1175)`, nonblank grayscale range `0-255`.
- Resource note:
  - `conda run -n gpr-fdtd-fwi` does not currently provide `torch`; successful Fast-GPR field runs use `/home/lam002/miniforge3/bin/python`, matching the earlier GSSI optimizer runs.

## Next Defensible Task

Move away from fixed second-event strength scans. The next useful branch is either optimized second-event placement, improved source/time-window alignment, or a y-dependent target model that can explain the shallow, middle, and deeper adjacent-profile depth progression.

The marathon request remains active.
