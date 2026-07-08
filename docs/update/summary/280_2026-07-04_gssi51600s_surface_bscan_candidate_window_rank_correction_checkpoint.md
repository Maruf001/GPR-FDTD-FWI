# GSSI 51600S Candidate-Window Rank Correction Checkpoint

## What changed

- Fixed `run_gssi51600s_surface_bscan_geometry_optimizer.py` so detector-rank runs use each candidate's own time window:
  - `sample_start = round((candidate_time_ns - pre_event_ns) / field_dt_ns)`
  - default `pre_event_ns = 0.5`
- Reran corrected-window detector-rank checks for ranks `3`, `5`, and `6`.
- Updated `run_gssi51600s_surface_bscan_product_report.py` to exclude stale detector-rank artifacts that reused rank-2's time window.
- Regenerated the corrected-window rank-aware surface product report.

## Key numbers

- Corrected rank-5 artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/038_gssi51600s_surface_bscan_geometry_optimizer_rank5_offset005_lower_bound_2mm_candidate_window`
- Corrected rank-3 artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/039_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_lower_bound_2mm_candidate_window`
- Corrected rank-6 artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/040_gssi51600s_surface_bscan_geometry_optimizer_rank6_offset005_lower_bound_2mm_candidate_window`
- Corrected-window product report: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/041_gssi51600s_surface_bscan_product_report`

Corrected-window comparison:

| detector rank | loss | optimized x m | z m | diameter mm | epsr | bg sigma S/m |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | `0.863149` | `0.080952` | `0.106567` | `4.764` | `2.767118` | `0.013688` |
| 3 | `0.848678` | `0.414366` | `0.126887` | `17.993` | `2.053892` | `0.006278` |
| 5 | `0.862440` | `0.404990` | `0.169589` | `4.897` | `2.047146` | `0.000951` |
| 6 | `0.898515` | `0.084289` | `0.160455` | `4.471` | `2.750752` | `0.014308` |

## Current decision

The previous rank-5 promotion was invalid because rank-5 had reused the rank-2 time-window start. With candidate-specific windows, detector rank 3 is now the best current corrected-surface candidate.

Current corrected-window product prediction:

- detector rank: `3`
- x: `0.414366 m`
- z/depth: `0.126887 m`
- diameter proxy: `17.993 mm`
- epsr: `2.053892`
- background conductivity: `0.006278 S/m`
- receiver offset: `0.005 m`
- y/length: not estimated from current GSSI profiles

## Claim boundary

This correction matters: the product report should not use stale rank artifacts. Rank 3 is the current best candidate under the corrected surface B-scan adapter, but it is still selected by normalized field-objective loss without ground-truth labels.

## Validation/resource checks

- Geometry rank-selection tests -> `4 passed`
- Product/geometry tests -> `7 passed`
- Expanded GSSI predictor suite -> `38 passed`
- Corrected-window product figure is nonblank, `1957 x 750`, RGB, channel range `0-255`.
- `git diff --check` on updated surface optimizer/product files was clean.
- Script snapshots were frozen under artifacts `038`, `039`, `040`, and `041`.

## Artifact paths

- Corrected-window product JSON: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/041_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_product_prediction.json`
- Corrected-window product CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/041_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_product_prediction.csv`
- Corrected-window comparison CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/041_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_optimizer_comparison.csv`
- Rank-3 optimizer summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/039_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_lower_bound_2mm_candidate_window/data/gssi51600s_surface_bscan_geometry_optimizer_summary.json`

## Next defensible task

Run rank-3 objective-window sensitivity: vary `pre_event_ns` and overlap samples around the current rank-3 candidate. The goal is to determine whether the `18 mm` diameter and x/z are stable to modest windowing changes.

## Marathon status

The requested 20-hour local marathon is still active. Continue with rank-3 window/overlap sensitivity rather than stopping at this checkpoint.
