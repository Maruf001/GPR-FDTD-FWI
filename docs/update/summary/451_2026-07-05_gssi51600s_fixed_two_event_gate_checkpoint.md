# 451 - 2026-07-05 - GSSI 51600S Fixed Two-Event Gate Checkpoint

## Purpose

Test the first bounded multi-event candidate on the trusted GSSI 51600S full-four-profile stack by adding a fixed deeper second event to the existing optimized single-event model.

## Implementation

- Added an optional fixed second-event mask to `run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py`.
- The main event still optimizes radius, length, x, cover depth, material, conductivity, and time shift.
- The second event is fixed for this first gate and shares the same material contrast as the main event.
- New CLI controls:
  - `--use-second-event`
  - `--second-center-x-m`
  - `--second-depth-m`
  - `--second-center-z-m`
  - `--second-diameter-mm`
  - `--second-length-m`

## Field Run

- Two-event run:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/520_gssi51600s_finite_length_3d_full4profiles_y016_domainz070_adamw_prior_two_event_deep_p23_windows50_54_58_62_66_iter24`
- Fixed second-event geometry:
  - x: `0.472456` m
  - cover depth: `0.160209` m
  - crossline center: `0.51` m
  - diameter: `17.559` mm
  - length: `0.186438` m
- Two-event result:
  - Best field L1: `1.012391448020935`
  - Best objective: `1.0248417854309082`
  - Best optimized main-event x: `0.4956232011318207` m
  - Best optimized main-event cover depth: `0.13360850512981415` m
  - Best optimized main-event diameter: `17.328161746263504` mm
  - Best optimized main-event length: `0.1779794991016388` m
  - Best background epsr: `2.00390887260437`
  - Best conductivity: `0.002449906198307872` S/m

## Comparison To Single-Target Baseline

- Full-four single-target baseline field L1: `0.9726306796073914`
- Fixed two-event field L1: `1.012391448020935`
- Field L1 delta, two-event minus single-target: `0.0397607684135437`
- Objective delta, two-event minus single-target: `0.042269110679626465`
- Decision: `fixed_two_event_candidate_worse_than_single_target`

## Product Integration

- Added `run_gssi51600s_two_event_gate_card.py`.
- Added `tests/test_gssi51600s_two_event_gate_card.py`.
- New two-event gate card:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/182_gssi51600s_two_event_gate_card_current`
- Updated current bundle:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/183_gssi51600s_current_prediction_bundle_with_two_event_gate_full4_baseline_adjacent_middle_depth`
  - Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- Current query now reports:
  - `two_event_gate_decision: fixed_two_event_candidate_worse_than_single_target`
  - `two_event_field_l1_delta_vs_single: 0.0397608`

## Validation

- `python -m py_compile ...` passed for touched scripts.
- Focused pytest suite: `71 passed`.
- `git diff --check` passed on touched files.
- Figure sanity:
  - Two-event gate: `(1753, 1175)`, nonblank RGBA.

## Next Defensible Task

Do not promote the fixed deep second-event geometry. If continuing multi-event work, optimize the second-event placement or test a y-dependent event model instead of fixing the second reflector at the profiles 2-3 candidate position.
