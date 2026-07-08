# 450 - 2026-07-05 - GSSI 51600S Full-Four Single-Target Baseline Checkpoint

## Purpose

Run and package a full-four-profile single-target GSSI baseline so the next multi-event or y-dependent target branch has a clear comparison point.

## Field Run

- Initial full-four attempt:
  - `518_gssi51600s_finite_length_3d_full4profiles_uniform_y022_domainz100_adamw_prior_windows50_54_58_62_66_iter24`
  - Status: failed before producing optimizer rows due to a Fast-GPR CUDA illegal-memory error with the enlarged 1.0 m crossline domain.
  - Action: do not treat as a result.
- Completed full-four baseline:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/519_gssi51600s_finite_length_3d_full4profiles_uniform_y016_domainz070_adamw_prior_windows50_54_58_62_66_iter24`
  - Best field L1: `0.9726306796073914`
  - Best objective: `0.9825726747512817`
  - Best x: `0.49967342615127563` m
  - Best cover depth: `0.13005343079566956` m
  - Best diameter: `17.280016094446182` mm
  - Best length: `0.1737007051706314` m
  - Best background epsr: `2.125948429107666`
  - Best conductivity: `0.0026609692722558975` S/m

## Interpretation

- The full-four single-target fit lands at an intermediate cover depth of about `0.130` m.
- It does not collapse the profile-subset depth progression:
  - Subset reference depth span: `0.041949562728405` m.
  - Full-four field L1 minus mean subset field L1: `0.03998550772666931`.
- Product action: use the all-profile single-target result as a baseline for multi-event or y-dependent target tests, not as a release claim.

## Product Integration

- Added `run_gssi51600s_full4_single_target_baseline_card.py`.
- Added `tests/test_gssi51600s_full4_single_target_baseline_card.py`.
- New card:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/180_gssi51600s_full4_single_target_baseline_card_current`
  - Decision: `full4_single_target_baseline_does_not_resolve_depth_progression`
- Updated current bundle:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/181_gssi51600s_current_prediction_bundle_with_full4_baseline_adjacent_middle_depth_and_slope_gate`
  - Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- Current query now reports:
  - `full4_single_target_baseline_decision: full4_single_target_baseline_does_not_resolve_depth_progression`
  - `full4_single_target_field_l1_delta_vs_subset_mean: 0.0399855`

## Validation

- `python -m py_compile ...` passed for touched scripts.
- Focused pytest suite: `18 passed`.
- `git diff --check` passed on touched files.
- Figure sanity:
  - Full-four single-target baseline: `(1787, 1175)`, nonblank RGBA.

## Next Defensible Task

Build a bounded two-event or y-dependent target test against the full-four-profile baseline. The new baseline gives a concrete single-target comparison for deciding whether a multi-event model actually improves the GSSI fit enough to report as a product candidate.
