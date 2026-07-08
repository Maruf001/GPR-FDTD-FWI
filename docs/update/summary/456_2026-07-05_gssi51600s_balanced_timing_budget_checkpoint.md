# 456 - 2026-07-05 - GSSI 51600S Balanced Timing Budget Checkpoint

## Purpose

Resolve a bias in the earlier joint timing-y local search: the apparent early-window field-fit gain came from 6-iteration fill runs, while parts of the reference timing evidence used 24-iteration stability runs. This branch reran the same mid-vs-early timing comparison at matched 24-iteration AdamW budget on the same nonuniform crossline-coordinate hypothesis.

## Field Runs

Matched 24-iteration runs:

- `531_gssi51600s_finite_length_3d_profiles0_2_refine_a021_b021_offsets_m021_0_021_domainz070_adamw_windows50_54_58_62_66_iter24`
  - Window: mid `50,54,58,62,66`
  - Objective: `0.9367484450340271`
  - Field L1: `0.913550853729248`
  - x: `0.5238146781921387` m
  - cover depth: `0.09731683135032654` m
  - length: `0.12790031731128693` m
  - diameter: `13.097324408590794` mm
- `532_gssi51600s_finite_length_3d_profiles1_3_refine_b021_c014_offsets_m021_0_014_domainz070_adamw_windows50_54_58_62_66_iter24`
  - Window: mid `50,54,58,62,66`
  - Objective: `0.9654792547225952`
  - Field L1: `0.9552609324455261`
  - x: `0.5001654624938965` m
  - cover depth: `0.12994687259197235` m
  - length: `0.15702702105045319` m
  - diameter: `13.567736372351646` mm
- `533_gssi51600s_finite_length_3d_profiles0_2_refine_a021_b021_offsets_m021_0_021_domainz070_adamw_windows46_50_54_58_62_iter24`
  - Window: early `46,50,54,58,62`
  - Objective: `0.9412761926651001`
  - Field L1: `0.9202333688735962`
  - x: `0.5210433006286621` m
  - cover depth: `0.10000470280647278` m
  - length: `0.12756063044071198` m
  - diameter: `13.128306716680527` mm
- `534_gssi51600s_finite_length_3d_profiles1_3_refine_b021_c014_offsets_m021_0_014_domainz070_adamw_windows46_50_54_58_62_iter24`
  - Window: early `46,50,54,58,62`
  - Objective: `0.9693251252174377`
  - Field L1: `0.9582932591438293`
  - x: `0.4920680522918701` m
  - cover depth: `0.13831670582294464` m
  - length: `0.16153891384601593` m
  - diameter: `13.521963730454445` mm

## Balanced Comparison

Mid-window pair:

- Mean objective: `0.9511138498783112`
- Mean field L1: `0.9344058930873871`
- x gap: `0.023649215698242188` m
- cover-depth gap: `0.03263004124164581` m
- length gap: `0.02912670373916626` m
- diameter gap: `0.4704119637608528` mm

Early-window pair:

- Mean objective: `0.9553006589412689`
- Mean field L1: `0.9392633140087128`
- x gap: `0.028975248336791992` m
- cover-depth gap: `0.03831200301647186` m
- length gap: `0.033978283405303955` m
- diameter gap: `0.39365701377391815` mm

Early-minus-mid deltas:

- Mean objective: `0.004186809062957764`
- Mean field L1: `0.004857420921325684`
- cover-depth gap: `0.00568196177482605` m
- x gap: `0.005326032638549805` m

## Current Decision

The early-window fit gain from the earlier short-budget card does not survive the matched 24-iteration comparison. At equal budget, the mid window fits better and is more consistent for x and cover depth.

Current gate decision:

`balanced_budget_mid_window_fits_better_and_is_more_consistent`

## Product Integration

- Balanced timing card:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/195_gssi51600s_balanced_timing_budget_card_current`
- Current GSSI prediction bundle:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/196_gssi51600s_current_prediction_bundle_with_balanced_timing_budget`
- Latest pointer:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- User-facing query:
  - `python run_field_prediction_current_query.py --dataset gssi51600s --format pretty`

The current product action is to keep the mid-window nonuniform timing as the source-time reference. The early-window diagnostic remains useful but is not promoted as the default timing estimate.

## Dataset Boundary

The current deliverable source remains `data/2026-06-09_GSSI_model_51600S`. The separate `data/2025-01-13_GPR_Dataset` archive remains out of the trusted GSSI rebar claim unless a future run explicitly targets and verifies one of its rebar branches.

## Validation

- Compile checks passed under `/home/lam002/miniforge3/bin/python`.
- Focused tests passed: `16 passed`.
- Broader GSSI/card suite passed: `164 passed`.
- `git diff --check` passed on touched files.
- Figure sanity:
  - Balanced timing card figure: `(1685, 1379)`, nonblank RGBA range `0-255`.
  - Bundle figure copy: `(1685, 1379)`, nonblank RGBA range `0-255`.
- Bundle script snapshot includes `run_gssi51600s_balanced_timing_budget_card.py`.

## Next Defensible Task

Move from event-window picking to a physical source-time or y-dependent target model. The equal-budget test says the early window should not be promoted; the remaining product gap is whether a compact source-time/wavelet model or profile-dependent geometry parameterization can reduce the depth disagreement while preserving the mid-window fit quality.

The marathon request remains active. Resumed active-session window: `2026-07-05 10:04 UTC` to approximately `2026-07-06 06:04 UTC`.
