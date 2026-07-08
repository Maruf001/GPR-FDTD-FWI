# GSSI51600S Profile 0 Influence Card Checkpoint

## What Changed

- Added `run_gssi51600s_profile0_influence_card.py`.
- Added unit tests for profile-0 label grouping and summary logic.
- Generated a compact diagnostic card that combines:
  - current conservative GSSI product synthesis,
  - leave-one-profile content diagnostics,
  - explicit profile-offset diagnostics,
  - profile event-content audit.

## Key Numbers

- Profile-0 influence card artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/100_gssi51600s_profile0_influence_card_current/`.
- Decision: `profile0_influence_requires_crossline_confirmation`.
- Current product default decision: `finite_length_seed_stability_inconclusive`.
- Current product default length range: `0.183165550-0.216162652 m`.
- Current product default diameter range: `17.295353-17.812613 mm`.
- With profile `0` included across the diagnostics:
  - length range `0.183171824-0.183684886 m`.
  - diameter range `17.295390-17.308654 mm`.
- Without profile `0` in the current diagnostic rows:
  - length `0.216162652 m`.
  - diameter `17.315585 mm`.
- Event-content audit:
  - highest-energy profile `3`.
  - latest time-center profile `3`.
  - earliest time-center profile `2`.

## Current Decision

The product default remains conservative and unchanged. The profile-0 influence card explains why: profile `0` appears to anchor the shorter finite-length branch, while the three-profile `1-3` subset that omits profile `0` supports the longer branch. The diagnostic offset runs show that this is not simply a uniform-spacing artifact for the noncontiguous stacks.

This is now the clearest next product blocker: confirm the acquisition position/crossline spacing of profile `0`, or repeat the local event with measured crossline coordinates, then rerun the finite-length 3D optimizer.

## Validation

- `python -m pytest tests/test_gssi51600s_profile0_influence_card.py -q` passed with `3 passed`.
- `python -m py_compile run_gssi51600s_profile0_influence_card.py` passed.
- `git diff --check` passed for the new card generator and tests.
- The generated profile-0 influence figure was visually inspected.

## Next Defensible Task

Run the broader focused validation with the new profile-0 card included, then continue with either a profile-0 geometry-assumption ladder or a product-facing current-status refresh that includes this diagnostic blocker.

The local marathon request remains active.
