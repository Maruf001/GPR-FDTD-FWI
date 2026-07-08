# 443 2026-07-05 GSSI51600S Event-Window Geometry Interaction Checkpoint

## What changed

- Reran the selected earlier event-window family under the current nonuniform crossline-coordinate hypothesis.
- Built an interaction card comparing uniform versus nonuniform geometry under mid and earlier event-window choices.
- Wired the interaction decision into the latest GSSI prediction bundle and public query output.

## Key numbers

- Nonuniform early-window profiles 0/2 run:
  - field L1 loss: `0.9145793914794922`
  - objective loss: `0.9405759572982788`
  - cover depth: `0.09918152540922165 m`
  - diameter: `17.51720905303955 mm`
  - length: `0.18713383376598358 m`
- Nonuniform early-window profiles 1/3 run:
  - field L1 loss: `0.9608709216117859`
  - objective loss: `0.9750060439109802`
  - cover depth: `0.1380164921283722 m`
  - diameter: `17.33890362083912 mm`
  - length: `0.18456555902957916 m`
- Uniform early-window cover-depth gap: `0.002047032117843628 m`.
- Nonuniform early-window cover-depth gap: `0.03883496671915054 m`.
- Nonuniform early-window mean field L1 delta versus nonuniform mid-window: `0.005282402038574219`.
- Nonuniform early-window diameter range: `17.33890362083912-17.51720905303955 mm`.
- Nonuniform early-window length range: `0.18456555902957916-0.18713383376598358 m`.

## Current decision

Decision: `event_window_xz_stabilization_not_geometry_stable_keep_timing_conditioned`.

The earlier event window almost eliminates the cover-depth split under uniform 0.22 m spacing, but it does not eliminate the split under the current nonuniform crossline coordinate hypothesis. This means timing and y geometry are coupled. The earlier event window remains a useful diagnostic candidate, not a release default.

## What remains blocked

- A single unconditioned x/cover-depth estimate is not yet defensible.
- Crossline y coordinates and source/event-time alignment need to be solved jointly or confirmed independently.
- The product query should continue to report the current estimates as conditioned 3D predictions.

## Validation and resource checks

- `python -m py_compile run_gssi51600s_event_window_geometry_interaction_card.py`
- `python -m pytest tests/test_gssi51600s_event_window_geometry_interaction_card.py -q`
- Result: `2 passed`.
- Bundle/query focused validation passed before regeneration: `14 passed`.
- Query smoke: `python run_field_prediction_current_query.py --dataset gssi51600s --format pretty`.
- Figure sanity checked for the interaction card and bundled copy: both PNGs are nonblank RGBA images with size `1889 x 1243`.

## Artifact paths

- Nonuniform earlier-window profiles 0/2 run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/506_gssi51600s_finite_length_3d_profiles0_2_best_nonuniform_a020_b020_domainz070_adamw_prior_stability_windows46_50_54_58_62_iter24`
- Nonuniform earlier-window profiles 1/3 run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/508_gssi51600s_finite_length_3d_profiles1_3_best_nonuniform_b020_c014_domainz070_adamw_prior_stability_windows46_50_54_58_62_iter24`
- Interaction card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/168_gssi51600s_event_window_geometry_interaction_card_current`
- Latest bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/169_gssi51600s_current_prediction_bundle_with_event_window_geometry_interaction`
- Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`

## Next defensible task

Move from fixed crossline geometry plus fixed event windows to a joint local alignment diagnostic: hold the regularized size/material objective, then search a small grid of nonuniform y offsets and event-window starts together to identify whether one paired geometry/timing choice stabilizes x/z without a larger waveform penalty.

## Marathon status

The marathon request remains active. Continue with the next bounded GSSI-only product-improvement branch.
