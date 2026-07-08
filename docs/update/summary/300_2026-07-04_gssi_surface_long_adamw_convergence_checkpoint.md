# GSSI Surface Long AdamW Convergence Checkpoint

Date: 2026-07-04

## What Changed

- Ran longer AdamW convergence checks on the same real GSSI surface B-scan field window.
- Used the same product-compatible settings as the matched seed branch:
  - detector rank `3`
  - receiver offset `0.005 m`
  - sigma/radius bounds `0.002-0.020 m`
  - time-shift optimization enabled
  - AdamW with weight decay `0.01`
  - diameter seeds `8, 12, 16, 20 mm`
  - `24` iterations per seed
- Added `run_gssi51600s_surface_bscan_adamw_convergence_synthesis.py`.
- Added focused tests for the convergence synthesis.
- Refreshed the GSSI product report and global product leaderboard with long-AdamW convergence diagnostics.

## Key Numbers

- Long AdamW seed runs:
  - `070_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_adamw_seed08_long24_grad`
    - best diameter `10.630296543 mm`
    - best loss `0.848438918591`
  - `072_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_adamw_seed12_long24_grad`
    - best diameter `16.988623887 mm`
    - best loss `0.848416328430`
  - `073_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_adamw_seed16_long24_grad`
    - best diameter `19.515388533 mm`
    - best loss `0.848420619965`
  - `071_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_adamw_seed20_long24_grad`
    - best diameter `20.420663059 mm`
    - best loss `0.848424792290`
- Long AdamW convergence synthesis:
  - artifact `074_gssi51600s_surface_bscan_adamw_convergence_synthesis`
  - decision `gssi_surface_long_adamw_improves_loss_but_seed_sensitive`
  - long best diameter `16.988623887 mm`
  - long near-best diameter range `10.630296543-20.420663059 mm`
  - best loss improvement versus short AdamW seeds `5.209445953e-05`
- Refreshed GSSI product report:
  - artifact `075_gssi51600s_surface_bscan_product_report`
  - promoted product prediction remains:
    - x `0.413941013248 m`
    - z `0.128718197346 m`
    - diameter proxy `18.586354330 mm`
    - epsr `2.044878721`
    - background conductivity `0.002187208273 S/m`
    - fit loss `0.848336815834`
  - long AdamW diagnostic:
    - decision `gssi_surface_long_adamw_improves_loss_but_seed_sensitive`
    - long best diameter `16.988623887 mm`
    - long range `10.630296543-20.420663059 mm`
    - supersedes product loss `False`
- Refreshed product leaderboard:
  - artifact `014_field_prediction_product_leaderboard`
  - current best products remain:
    - `external_2025_pipe_0701:fastgpr_3d_stack_y_length_proxy`
    - `gssi51600s:fastgpr_corrected_surface_bscan`

## What Remains Blocked

- Longer AdamW improves the matched-seed objective, but it does not collapse diameter into a narrow range.
- The low seed moves upward from about `8.1 mm` to `10.6 mm`, while the other seeds cluster around `17-20.4 mm`.
- The long branch does not beat the currently promoted GSSI product loss, so it is diagnostic evidence rather than the active product prediction.
- GSSI still lacks y position and rebar length estimation in this surface B-scan branch.

## Current Decision

The current field-data product stance is:

- optimizer choice and longer AdamW help fit quality,
- diameter remains a reported candidate plus range, not a single confident measurement,
- the promoted GSSI product stays at `18.59 mm` diameter proxy because it has lower product loss,
- the long AdamW convergence diagnostic supports a plausible high-diameter region but keeps the uncertainty visible.

## Next Defensible Task

Shift back toward the user’s requested 3D deliverable:

- refresh the `2025-01-13` 0701 3D stack product with the same optimizer-family/convergence reporting discipline,
- or add a cross-dataset product card that compares which field dataset currently supports x/z, y/length, diameter, epsr, and conductivity,
- then choose the next real 3D/y-length improvement branch based on which parameter is most under-supported.

## Validation And Resources

- `python -m pytest tests/test_gssi51600s_surface_bscan_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_gssi51600s_surface_bscan_adamw_convergence_synthesis.py tests/test_gssi51600s_surface_bscan_optimizer_family_synthesis.py tests/test_gssi51600s_surface_bscan_seed_synthesis.py tests/test_gssi51600s_surface_bscan_gradient_diagnostic_synthesis.py -q`
  - `16 passed`
- `python -m py_compile run_gssi51600s_surface_bscan_product_report.py run_field_prediction_product_leaderboard.py run_gssi51600s_surface_bscan_adamw_convergence_synthesis.py run_gssi51600s_surface_bscan_optimizer_family_synthesis.py run_gssi51600s_surface_bscan_seed_synthesis.py run_gssi51600s_surface_bscan_gradient_diagnostic_synthesis.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `074.../figures/gssi51600s_surface_bscan_adamw_convergence.png`: size `(2399, 767)`, min/max `(0, 255)`, stddev `65.33`
  - `075.../figures/gssi51600s_surface_bscan_product_report.png`: size `(1957, 750)`, min/max `(0, 255)`, stddev `58.93`
  - `014.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `64.79`

## Artifact Paths

- Long AdamW convergence synthesis:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/074_gssi51600s_surface_bscan_adamw_convergence_synthesis`
- Refreshed GSSI product report:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/075_gssi51600s_surface_bscan_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/014_field_prediction_product_leaderboard`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
