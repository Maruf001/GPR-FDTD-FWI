# GSSI 51600S Surface B-Scan Detector-Rank Stability Checkpoint

## What changed

- Added `--detector-rank` to `run_gssi51600s_surface_bscan_geometry_optimizer.py`.
- Ran corrected surface B-scan Fast-GPR optimization on additional detector candidates with the current best settings:
  - AdamW
  - `5 mm` receiver offset
  - `2 mm` diameter lower bound
  - `48` iterations
- Updated `run_gssi51600s_surface_bscan_product_report.py` so product selection includes detector-rank stability artifacts.
- Regenerated the corrected-surface product report.

## Key numbers

- Rank-1 artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/031_gssi51600s_surface_bscan_geometry_optimizer_rank1_offset005_lower_bound_2mm`
- Rank-3 artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/032_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_lower_bound_2mm`
- Rank-5 artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/033_gssi51600s_surface_bscan_geometry_optimizer_rank5_offset005_lower_bound_2mm`
- Rank-4 artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/034_gssi51600s_surface_bscan_geometry_optimizer_rank4_offset005_lower_bound_2mm`
- Rank-6 artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/035_gssi51600s_surface_bscan_geometry_optimizer_rank6_offset005_lower_bound_2mm`
- Rank-aware product report: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/037_gssi51600s_surface_bscan_product_report`

Rank comparison:

| detector rank | detector x m | loss | optimized x m | z m | diameter mm | epsr |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `0.703263` | `0.926351` | `0.700205` | `0.104379` | `15.813` | `2.713975` |
| 2 | `0.109989` | `0.863149` | `0.080952` | `0.106567` | `4.764` | `2.767118` |
| 3 | `0.403293` | `0.847881` | `0.421517` | `0.126888` | `15.441` | `2.054616` |
| 4 | `0.703263` | `0.926296` | `0.693745` | `0.112958` | `16.780` | `2.722175` |
| 5 | `0.396627` | `0.842109` | `0.394374` | `0.139889` | `18.825` | `2.040689` |
| 6 | `0.109989` | `0.863146` | `0.099179` | `0.160902` | `4.571` | `2.764745` |

## Current decision

The corrected surface B-scan product report should promote detector rank 5, not the earlier rank 2. Rank 5 is the best among the tested detector ranks and corresponds to a later/deeper event near the same x neighborhood as rank 3.

Current rank-aware corrected-surface prediction:

- detector rank: `5`
- x: `0.394374 m`
- z/depth: `0.139889 m`
- diameter proxy: `18.825 mm`
- epsr: `2.040689`
- background conductivity: `0.000979 S/m`
- receiver offset: `0.005 m`
- y/length: not estimated from current GSSI profiles

## Claim boundary

This is a stronger product candidate than the rank-2 local event, but it is still provisional. The ranking is based on normalized local Fast-GPR objective loss, not destructive ground truth. The next stability question is whether rank 5 remains best under nearby time-window/overlap and source-frequency choices.

## Validation/resource checks

- Surface product/optimizer tests -> `12 passed`
- Expanded GSSI predictor suite -> `38 passed`
- Rank optimizer figures are nonblank, `2314 x 750`, RGB, channel range `0-255`.
- Rank-aware product figure is nonblank, `1957 x 750`, RGB, channel range `0-255`.
- `git diff --check` on updated surface optimizer/product files was clean.
- Script snapshots were frozen under artifacts `031`, `032`, `033`, `034`, `035`, and `037`.

## Artifact paths

- Rank-aware product JSON: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/037_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_product_prediction.json`
- Rank-aware product CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/037_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_product_prediction.csv`
- Rank comparison CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/037_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_optimizer_comparison.csv`
- Rank-5 optimizer summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/033_gssi51600s_surface_bscan_geometry_optimizer_rank5_offset005_lower_bound_2mm/data/gssi51600s_surface_bscan_geometry_optimizer_summary.json`

## Next defensible task

Run time-window/overlap sensitivity for rank 5. The product candidate should not be shipped as a best prediction until it survives small changes in the objective window.

## Marathon status

The requested 20-hour local marathon is still active. Continue with rank-5 window/overlap sensitivity rather than stopping at this checkpoint.
