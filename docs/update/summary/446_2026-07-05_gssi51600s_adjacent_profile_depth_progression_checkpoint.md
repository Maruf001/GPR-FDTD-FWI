# 446 2026-07-05 GSSI51600S Adjacent Profile Depth Progression Checkpoint

## What changed

- Reran adjacent profile pairs 0/1 and 2/3 with the current regularized 24-iteration AdamW settings.
- Compared adjacent pairs against overlapping profile subsets 0/2 and 1/3.
- Built and bundled an adjacent-profile depth-progression card.

## Key numbers

- Profiles 0/1:
  - cover depth: `0.09768731147050858 m`
  - x: `0.5128870606422424 m`
  - field L1 loss: `1.000873327255249`
  - diameter: `17.556559294462204 mm`
  - length: `0.1856800615787506 m`
- Profiles 0/2:
  - cover depth: `0.096347875893116 m`
  - x: `0.5242039561271667 m`
  - field L1 loss: `0.906975269317627`
  - diameter: `17.518799751996994 mm`
  - length: `0.18713364005088806 m`
- Profiles 1/3:
  - cover depth: `0.138297438621521 m`
  - x: `0.5013077855110168 m`
  - field L1 loss: `0.9583150744438171`
  - diameter: `17.418239265680313 mm`
  - length: `0.18566444516181946 m`
- Profiles 2/3:
  - cover depth: `0.16020938754081726 m`
  - x: `0.4724560081958771 m`
  - field L1 loss: `1.0447205305099487`
  - diameter: `17.55896955728531 mm`
  - length: `0.18643775582313538 m`
- Adjacent/overlap depth range: `0.096347875893116-0.16020938754081726 m`.
- Depth span: `0.06386151164770126 m`.
- Shallow subset labels: `profiles0_1`, `profiles0_2`.
- Deep subset labels: `profiles1_3`, `profiles2_3`.

## Current decision

Decision: `adjacent_profile_depth_progression_keep_3d_depth_conditioned`.

The current GSSI event window should not be forced into one cover-depth value across all profile subsets. The pattern is consistent with y-dependent target geometry or multiple nearby events, and it needs measured crossline geometry, a multi-target model, or an explicitly y-dependent 3D model before a single 3D rebar claim is promoted.

## What remains blocked

- A single x/y/z prediction remains conditioned because the depth changes systematically across profile subsets.
- The current finite-length model assumes one straight target with fixed depth; the data may need a sloped/curved target or multi-rebar/event formulation.
- Measured crossline profile coordinates would still be the highest-value external input.

## Validation and resource checks

- `python -m py_compile run_gssi51600s_adjacent_profile_depth_progression_card.py`
- `python -m pytest tests/test_gssi51600s_adjacent_profile_depth_progression_card.py -q`
- Result: `2 passed`.
- Bundle/query focused validation passed before regeneration: `14 passed`.
- Query smoke: `python run_field_prediction_current_query.py --dataset gssi51600s --format pretty`.
- Figure sanity checked for the depth-progression card and bundled copy: both PNGs are nonblank RGBA images with size `1804 x 1175`.

## Artifact paths

- Profiles 0/1 run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/512_gssi51600s_finite_length_3d_profiles0_1_uniform_y022_domainz070_adamw_prior_windows50_54_58_62_66_iter24`
- Profiles 2/3 run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/513_gssi51600s_finite_length_3d_profiles2_3_uniform_y022_domainz070_adamw_prior_windows50_54_58_62_66_iter24`
- Depth-progression card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/172_gssi51600s_adjacent_profile_depth_progression_card_current`
- Latest bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/173_gssi51600s_current_prediction_bundle_with_adjacent_profile_depth_progression`
- Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`

## Next defensible task

Prototype a y-dependent 3D target parameterization or a two-event hypothesis check, while keeping diameter, length, permittivity, conductivity, runtime, and field-fit metrics reportable through the same product query.

## Marathon status

The marathon request remains active. Continue with the next bounded GSSI-only product-improvement branch.
