# External 2025 Surface-Weight Policy Checkpoint

## What Changed

- Generated real-field surface-weight policy synthesis artifact `253_external_2025_surface_weight_policy_synthesis`.
- Added focused tests for the policy synthesis decision logic.
- Added a diagnostic leaderboard row for the policy-only oracle boundary.
- Refreshed the field-method validation leaderboard.

## Key Numbers

- Profiles summarized: `6`.
- Internal holdout threshold: `0.95`.
- Profiles passing the threshold with their best known variant: `3`.
- Profiles failing the threshold with their best known variant: `3`.
- Best-variant counts: `surface_prune_w030=4`, `baseline_no_surface_prune=2`.
- Validated profiles: `190424AA_LID10002_rank2_right_shift`, `LS1_LID10001_rank2`, `LS1_LID10002`.
- Failed profiles: `190424AA_LID10001_rank1`, `190424AA_LID10003_rank1`, `LDH1_LID10001_rank2`.
- Mean best known holdout: `1.2479663888613384`.
- Worst best known holdout: `1.8293899297714233`.
- Mean best delta versus baseline: `-0.035575216015179954`.
- Leaderboard evidence score for this policy-only row: `1`.

## Current Decision

Decision string:

`external_2025_surface_weight_policy_profile_adaptive_oracle_only`

Interpretation: surface-prune weight is profile-dependent on the current real-field evidence. The best choice can be found after measuring holdout losses, but this does not yet provide an autonomous pre-run selector. This artifact is policy-only and does not itself report radius, diameter, or permittivity candidates.

## What Remains Blocked

- No universal surface-prune weight is supported across the tested real profiles.
- This artifact does not answer the user's requested diameter/permittivity deliverable; it only closes the optimizer-weight boundary.
- The next branch must report best-fit radius/diameter and epsr candidates plus ranges on real field data rather than only saying those values are non-unique.

## Validation

- `python -m py_compile run_ggae2025_external_2025_surface_weight_policy_synthesis.py run_field_method_validation_leaderboard.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_ggae2025_external_2025_surface_weight_policy_synthesis.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `22 passed in 0.42s`.
- `git diff --check -- run_ggae2025_external_2025_surface_weight_policy_synthesis.py tests/test_ggae2025_external_2025_surface_weight_policy_synthesis.py run_field_method_validation_leaderboard.py tests/test_field_method_validation_leaderboard.py`
- Surface-weight policy figure: `1974x869`, nonblank RGB channel extrema.
- Leaderboard figure: `1575x720`, nonblank RGB channel extrema; figure validation status `ok`.

## Artifact Paths

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/253_external_2025_surface_weight_policy_synthesis`
- `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Next Defensible Task

Build a real-field radius/epsr candidate report that outputs the best-fit diameter/radius and concrete permittivity candidate plus a loss-ranked range. This should use existing real-field optimizer artifacts first, then run additional trainable-radius/epsr fits only where the current artifact set does not contain enough information.

## Marathon Status

The requested real-field-data marathon is still active.
