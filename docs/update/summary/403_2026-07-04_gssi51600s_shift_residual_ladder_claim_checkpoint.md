# 2026-07-04 GSSI 51600S Shift/Residual Ladder Claim Checkpoint

## What changed

- Reran the GSSI `profiles1_3` profile-mean finite-length optimizer with relaxed common time-shift bounds after the earlier bad stack-manifest path attempt.
- Preserved the failed pre-load directory as run provenance and wrote the clean rerun as:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/437_gssi51600s_finite_length_3d_profiles1_3_profile_mean_relaxed_shift_y016_adamw_windows50_54_58_62_66_iter6`
- Built a combined residual/shift ladder synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/438_gssi51600s_finite_length_3d_shift_residual_ladder_profiles0_2_1_3_adamw_y016`
- Added a GSSI-specific product claim card to avoid over-reading the generic synthesis decision:
  - `run_gssi51600s_shift_residual_ladder_claim_card.py`
  - `tests/test_gssi51600s_shift_residual_ladder_claim_card.py`
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/102_gssi51600s_shift_residual_ladder_claim_card_current`

## Key numbers

- Relaxed profile-mean `profiles1_3` rerun:
  - best length: `0.2161626518 m`
  - best diameter: `17.315585 mm`
  - best field L1 loss: `0.961354733`
  - best objective loss: `0.979076684`
  - best time shift: `1.898208857 ns`
  - max shift gradient: `0.0`
- The relaxed-shift result preserved the earlier `profiles1_3` long branch instead of collapsing toward the `profiles0_2` short branch.
- Combined diagnostic ladder:
  - profile-mean with relaxed-shift length range: `0.183171824-0.216162652 m`
  - all diagnostic length range: `0.183171824-0.216162652 m`
  - all diagnostic diameter range: `17.295390-18.586002 mm`
  - lowest single diagnostic loss: `receiver_mean profiles0_2`, field L1 `0.936113536`
  - `receiver_mean profiles1_3` field L1 was `0.050384402` worse than profile-mean `profiles1_3`
  - `global_mean profiles1_3` had no loss decrease

## Current decision

The strict GSSI claim-card decision is:

`do_not_tighten_product_range_shift_relaxation_preserves_long_branch`

The generic synthesis artifact `438` mechanically reports a supportive decision because its near-best rule selects the single lowest-loss `receiver_mean profiles0_2` row. That is not product-safe by itself. The GSSI-specific card supersedes that interpretation for product/default purposes and keeps the current conservative GSSI range active.

## What remains blocked

- Crossline spacing and exact profile coordinates remain assumption-conditioned rather than metadata-confirmed.
- The short-length branch around `0.183 m` and long-length branch around `0.216 m` both remain plausible under the current trusted GSSI field stack.
- Receiver/global residual variants are useful diagnostics but are not yet stable enough across paired profile windows to replace the profile-mean default.

## Next defensible task

Run a detector-window/source-window sensitivity focused on the `profiles1_3` long branch and compare whether event-window selection, not time-shift freedom, explains the length spread. If the branch persists, the next product step is a crossline-coordinate confirmation packet or a geometry-parameterized 3D fit that treats profile positions as explicit variables.

## Validation/resource checks

- `python run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py ... relaxed shift ...` completed in about 24 seconds.
- `python run_field_3d_0701_finite_length_optimizer_seed_stability.py ...` generated artifact `438`.
- `python run_gssi51600s_shift_residual_ladder_claim_card.py ...` generated artifact `102`.
- `python -m py_compile run_gssi51600s_shift_residual_ladder_claim_card.py` passed.
- `python -m pytest tests/test_gssi51600s_shift_residual_ladder_claim_card.py -q` passed: `2 passed`.
- Figure `102/.../figures/gssi51600s_shift_residual_ladder_claim_card.png` was visually inspected.
- Marathon request remains active; continue to the next bounded GSSI field-data prediction branch.
