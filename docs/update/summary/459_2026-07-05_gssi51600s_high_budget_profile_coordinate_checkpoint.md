# 459 - GSSI 51600S High-Budget Profile-Coordinate Checkpoint

## What changed

Packaged an existing matched 24-iteration GSSI profile-coordinate comparison into a product-facing card. This compares the current nonuniform coordinate seed (`a020/b020/c014`) against the nearby `a021/b021/c014` coordinate used by the latest timing and center-y diagnostic runs.

Generated:

- `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/201_gssi51600s_high_budget_profile_coordinate_card_current`
- `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/202_gssi51600s_current_prediction_bundle_with_high_budget_profile_coordinate`

## Key numbers

Matched 24-iteration unregularized AdamW profile-coordinate comparison:

- Best label: `seed_a020_b020_c014`.
- Near-tie labels: `seed_a020_b020_c014`, `a021_b021_c014`.
- Seed mean objective: `0.9511052072048187`.
- `a021/b021/c014` mean objective: `0.9511138498783112`.
- Objective delta for `a021/b021/c014` vs seed: `+8.64267349243164e-06`.
- Field L1 delta for `a021/b021/c014` vs seed: `+5.066394805908203e-06`.
- Best spacing hypothesis: profile0-to-1 `0.20` m, profile1-to-2 `0.20` m, profile2-to-3 `0.14` m.
- Best high-budget unregularized length range: `0.1275796741247177` to `0.15701568126678467` m.
- Best high-budget unregularized diameter range: `13.097299262881279` to `13.56665138155222` mm.

## Current decision

`high_budget_profile_coordinate_seed_slightly_best_near_tie`

The existing nonuniform profile-coordinate seed remains the current default, but the nearby coordinate is effectively tied at this optimizer budget. This supports keeping profile coordinates conditioned rather than claiming a measured y geometry from optimizer evidence alone.

## What remains blocked

The release blocker remains measured crossline profile coordinates or a stronger model that can explain the y-dependent depth/length split without relying on near-tied coordinate hypotheses.

## Validation and resource checks

- Focused compile passed for the high-budget profile-coordinate card, current bundle, and current query.
- Focused tests: `14 passed`.
- Broad GSSI/card regression suite: `168 passed`.
- Figure validation passed for the high-budget coordinate card and bundle copy: `(2314, 835)` RGBA, nonblank.
- `git diff --check` passed for touched tracked paths.

## Next defensible task

Continue on source/time alignment or a y-dependent target model. The high-budget coordinate comparison is now packaged and does not justify another nearby coordinate-only sweep unless measured geometry arrives.

## Marathon status

The local 20-hour marathon request is still active. This checkpoint is a progress artifact, not a stopping point.
