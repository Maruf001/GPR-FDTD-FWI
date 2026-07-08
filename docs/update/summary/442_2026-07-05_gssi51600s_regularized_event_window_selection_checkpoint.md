# 442 2026-07-05 GSSI51600S Regularized Event-Window Selection Checkpoint

## What changed

- Ran an intermediate profiles 1/3 event-window test at sample starts `48,52,56,60,64`.
- Built an event-window selection card that compares mid/mid, early/early, and hybrid event-window pairings across the two overlapping GSSI profile subsets.
- Wired the selected event-window candidate into the current GSSI prediction bundle and public query output.

## Key numbers

- New intermediate profiles 1/3 run:
  - field L1 loss: `0.9867746233940125`
  - objective loss: `1.0089970827102661`
  - center x: `0.49870097637176514 m`
  - cover depth: `0.10205332189798355 m`
  - diameter: `17.232708632946014 mm`
  - length: `0.18371856212615967 m`
- Selected event-window candidate: `early_early`.
- Candidate field L1 delta versus mid/mid: `0.009881705045700073`.
- Candidate objective delta versus mid/mid: `0.013721853494644165`.
- Candidate cover-depth gap: `0.002047032117843628 m`.
- Candidate cover-depth gap delta versus mid/mid: `-0.03990253061056137 m`.
- Candidate diameter range: `17.217664048075676-17.517203465104103 mm`.
- Candidate length range: `0.18371789157390594-0.18713372945785522 m`.
- Candidate relative permittivity range: `2.1034798622131348-2.1142635345458984`.

## Current decision

Decision: `event_window_candidate_reduces_xz_gap_with_small_field_l1_cost`.

The all-earlier event-window pairing nearly removes the cover-depth split across the overlapping profile subsets, while increasing the mean field L1 loss by just under the `0.01` threshold used for this diagnostic. This is a useful source/time-alignment candidate, but it remains conditioned until a physical source-time or event-picking rule explains why this window should replace the mid-window default.

## What remains blocked

- The event-window candidate is empirically useful but not yet physically justified.
- Crossline profile coordinates are still unmeasured in the available GSSI metadata.
- The predictor should keep reporting conditioned x, y, z, length, diameter, permittivity, and conductivity until source/time-window and crossline geometry are both confirmed.

## Validation and resource checks

- `python -m py_compile run_gssi51600s_regularized_event_window_selection_card.py`
- `python -m pytest tests/test_gssi51600s_regularized_event_window_selection_card.py -q`
- Result: `2 passed`.
- Focused bundle/query validation passed before bundle regeneration: `14 passed`.
- Query smoke: `python run_field_prediction_current_query.py --dataset gssi51600s --format pretty`.
- Figure sanity checked for the event-window selection card and bundled copy: both PNGs are nonblank RGBA images with size `1974 x 1430`.

## Artifact paths

- Intermediate profiles 1/3 run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/505_gssi51600s_finite_length_3d_profiles1_3_uniform_y022_domainz070_adamw_prior_stability_windows48_52_56_60_64_iter24`
- Event-window selection card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/166_gssi51600s_regularized_event_window_selection_card_current`
- Latest bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/167_gssi51600s_current_prediction_bundle_with_regularized_event_window_selection`
- Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`

## Next defensible task

Test whether the selected earlier-window candidate remains stable when the crossline geometry changes from uniform 0.22 m to the current nonuniform coordinate hypothesis. If it remains stable, the next bundle can separate source/time-window conditioning from y-geometry conditioning more cleanly.

## Marathon status

The marathon request remains active. Continue with the next bounded GSSI-only product-improvement branch.
