# GSSI Surface Optimizer Family Checkpoint

Date: 2026-07-04

## What Changed

- Ran matched optimizer-family tests on the real GSSI surface B-scan field window.
- Compared Adam, AdamW, and Adamax using the same detector/window/receiver-offset/time-shift setup:
  - detector rank `3`
  - receiver offset `0.005 m`
  - sigma/radius bounds `0.002-0.020 m`
  - diameter seeds `8, 12, 16, 20 mm`
  - eight iterations per seed
- Added `run_gssi51600s_surface_bscan_optimizer_family_synthesis.py`.
- Added focused tests for optimizer-family synthesis.
- Refreshed the GSSI product report to include optimizer-family evidence.
- Refreshed the field prediction product leaderboard to point to the new GSSI report.

## Key Numbers

- New optimizer-family runs:
  - Adam:
    - artifacts `060-063`
    - best loss `0.848470509052`
    - best diameter `18.795724958 mm`
    - near-best diameter range `8.082027547-18.795724958 mm`
    - mean iteration runtime `0.609852 s`
  - AdamW:
    - artifacts `054-057`
    - best loss `0.848468422890`
    - best diameter `18.799591810 mm`
    - near-best diameter range `8.095408790-18.799591810 mm`
    - mean iteration runtime `0.623444 s`
  - Adamax:
    - artifacts `064-067`
    - best loss `0.848474502563`
    - best diameter `18.889678642 mm`
    - near-best diameter range `8.139342070-18.889678642 mm`
    - mean iteration runtime `0.586477 s`
- Optimizer-family synthesis:
  - artifact `068_gssi51600s_surface_bscan_optimizer_family_synthesis`
  - decision `gssi_surface_optimizer_family_comparison_seed_sensitive`
  - best optimizer by loss `adamw`
  - best diameter `18.799591810 mm`
  - cross-optimizer near-best diameter range `8.082027547-18.889678642 mm`
  - diameter status `all_tested_optimizer_families_seed_sensitive`
- Refreshed GSSI product report:
  - artifact `069_gssi51600s_surface_bscan_product_report`
  - x `0.413941013248 m`
  - z `0.128718197346 m`
  - diameter proxy `18.586354330 mm`
  - product near-best diameter range `8.108957671-18.738288432 mm`
  - optimizer-family best optimizer `adamw`
  - optimizer-family range `8.082027547-18.889678642 mm`
  - optimizer-family diameter status `all_tested_optimizer_families_seed_sensitive`
  - epsr `2.044878721`
  - background conductivity `0.002187208273 S/m`
  - fit loss `0.848336815834`
- Refreshed product leaderboard:
  - artifact `013_field_prediction_product_leaderboard`
  - current best products:
    - `external_2025_pipe_0701:fastgpr_3d_stack_y_length_proxy`
    - `gssi51600s:fastgpr_corrected_surface_bscan`

## What Remains Blocked

- Adam, AdamW, and Adamax all reduce the real field objective, but none removes the broad diameter seed sensitivity.
- The current GSSI surface objective supports a provisional best diameter candidate plus a range, not a unique reliable diameter.
- GSSI still lacks y position and length because this branch uses a surface B-scan window rather than a measured crossline stack.
- The tested optimizer comparison does not yet include LBFGS or a staged AdamW-to-LBFGS polish.

## Current Decision

Optimizer choice alone is not enough to make the GSSI diameter uniquely identifiable. AdamW remains the best current product optimizer by loss, Adamax is slightly faster per iteration, and the predictor should continue reporting:

- best diameter candidate around `18.6-18.8 mm`,
- optimizer-family near-best range around `8.08-18.89 mm`,
- x/z/material estimates as provisional,
- no y/length claim for this GSSI surface branch.

This is still product progress because the product report now exposes the optimizer comparison and uncertainty directly.

## Next Defensible Task

Move from optimizer-family comparison to objective improvement:

- test a staged optimizer schedule on the same GSSI field window, such as longer AdamW from the best and low seeds, then optional local polish if supported,
- or add a geometry/material regularization or source/time alignment refinement that can sharpen diameter sensitivity without changing the field-data scope,
- promote only if it narrows the diameter range while preserving or improving the B-scan fit and runtime.

## Validation And Resources

- `python -m pytest tests/test_gssi51600s_surface_bscan_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_gssi51600s_surface_bscan_optimizer_family_synthesis.py tests/test_gssi51600s_surface_bscan_seed_synthesis.py tests/test_gssi51600s_surface_bscan_gradient_diagnostic_synthesis.py -q`
  - `14 passed`
- `python -m py_compile run_gssi51600s_surface_bscan_product_report.py run_field_prediction_product_leaderboard.py run_gssi51600s_surface_bscan_optimizer_family_synthesis.py run_gssi51600s_surface_bscan_seed_synthesis.py run_gssi51600s_surface_bscan_gradient_diagnostic_synthesis.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `068.../figures/gssi51600s_surface_bscan_optimizer_family_synthesis.png`: size `(2399, 767)`, min/max `(0, 255)`, stddev `66.96`
  - `069.../figures/gssi51600s_surface_bscan_product_report.png`: size `(1957, 750)`, min/max `(0, 255)`, stddev `58.93`
  - `013.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `64.79`

## Artifact Paths

- Optimizer-family synthesis:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/068_gssi51600s_surface_bscan_optimizer_family_synthesis`
- Refreshed GSSI product report:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/069_gssi51600s_surface_bscan_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/013_field_prediction_product_leaderboard`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
