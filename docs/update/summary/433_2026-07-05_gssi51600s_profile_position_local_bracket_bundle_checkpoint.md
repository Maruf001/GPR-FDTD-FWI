# GSSI 51600S Profile-Position Local Bracket Bundle Checkpoint

## What Changed

- Continued the trusted GSSI 51600S field-data path and kept the separate 2025 public archive out of the current rebar claim.
- Completed the narrower profiles 1-3 nonuniform profile-position bracket around the previous best `[-0.20, 0.00, 0.14]` candidate.
- Added four local-search rows to the profile-position ladder card:
  - `[-0.20, 0.00, 0.12]`
  - `[-0.20, 0.00, 0.10]`
  - `[-0.22, 0.00, 0.14]`
  - `[-0.18, 0.00, 0.14]`
- Regenerated the profile-position ladder card with all 17 current rows.
- Regenerated the latest GSSI current prediction bundle so the live query points to the updated profile-position evidence.
- Updated the Sunday daily update with the tightened local-search result.

## Key Numbers

- Current best profiles 1-3 nonuniform label: `profile1_outward_right014`.
- Current best profiles 1-3 offsets: `[-0.20, 0.00, 0.14]`.
- Current best profiles 1-3 objective loss: `0.978588283`.
- Current best profiles 1-3 field-L1 loss: `0.960957825`.
- Current best profiles 1-3 finite length: `0.184444651 m`.
- Current best profiles 1-3 diameter: `17.317055 mm`.
- New `[-0.20, 0.00, 0.12]` objective loss: `0.980930865`.
- New `[-0.20, 0.00, 0.10]` objective loss: `1.014428258`.
- New `[-0.22, 0.00, 0.14]` objective loss: `0.978592396`.
- New `[-0.18, 0.00, 0.14]` objective loss: `0.978601575`.
- Near-best nonuniform short labels after the full local bracket: `profile1_outward_right014`, `nonuniform_left022_right014`.
- The nonuniform coordinate synthesis remains unchanged:
  - profile 0: `-0.20 m`
  - profile 1: `0.00 m`
  - profile 2: `0.20 m`
  - profile 3: `0.34 m`
- Live query still reports AdamW as the recommended optimizer.

## Current Decision

The tighter local bracket supports keeping `[-0.20, 0.00, 0.14]` as the current best profiles 1-3 nonuniform profile-position candidate. The nearby `[-0.22, 0.00, 0.14]` case is a near tie, so the product remains geometry-conditioned rather than promoting a single measured y geometry.

## What Remains Blocked

- The GSSI crossline profile coordinates are optimizer-estimated, not measured survey metadata.
- The current profile-position search is still a bounded local discrete search around candidate offsets, not a fully differentiable continuous profile-coordinate inversion.
- The public product range should remain geometry-conditioned until measured profile coordinates or a stronger profile-position optimizer confirms the y geometry.

## Next Defensible Task

Build the next product-improving branch around explicit crossline profile-coordinate estimation: either add a continuous/profile-coordinate optimizer layer or run a stronger window-stability check seeded from the current nonuniform coordinate hypothesis, then refresh the bundle only if the reported x, y, cover depth, length, diameter, relative permittivity, or conductivity changes.

## Validation And Resource Checks

- `python -m pytest tests/test_field_prediction_current_query.py tests/test_gssi51600s_optimizer_family_card.py tests/test_gssi51600s_crossline_spacing_release_gate.py tests/test_gssi51600s_profile_position_ladder_card.py tests/test_gssi51600s_nonuniform_coordinate_synthesis_card.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_runtime_benchmark_card.py tests/test_gssi51600s_nonuniform_geometry_run_planner.py -q`
- Result: 30 passed.
- `python -m py_compile run_field_prediction_current_query.py run_gssi51600s_optimizer_family_card.py run_gssi51600s_crossline_spacing_release_gate.py run_gssi51600s_profile_position_ladder_card.py run_gssi51600s_nonuniform_coordinate_synthesis_card.py run_gssi51600s_current_prediction_bundle.py`
- Result: passed.
- Figure sanity check for the regenerated profile-position ladder figure and bundle copy: both images are `2023 x 1243` pixels with grayscale extrema `(0, 255)`.
- `git diff --check` on touched scripts, tests, and the daily update.
- Result: passed.

## Artifact Paths

- Local bracket runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/475_gssi51600s_finite_length_3d_profiles1_3_nonuniform_left020_right012_offsets_m020_0_012_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/476_gssi51600s_finite_length_3d_profiles1_3_nonuniform_left020_right010_offsets_m020_0_010_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/477_gssi51600s_finite_length_3d_profiles1_3_nonuniform_left022_right014_offsets_m022_0_014_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/478_gssi51600s_finite_length_3d_profiles1_3_nonuniform_left018_right014_offsets_m018_0_014_domainz070_adamw_windows50_54_58_62_66_iter6`
- Updated profile-position ladder card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/147_gssi51600s_profile_position_ladder_card_current`
- Latest bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/148_gssi51600s_current_prediction_bundle_with_profile_position_local_search_475_478`
- Stable latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- Daily update: `docs/update/daily_update/2026-06-29_to_2026-07-05_daily_update.md`

## Marathon Status

The marathon request is still active. Continue with the next product-improving GSSI field-data branch rather than stopping at this checkpoint.
