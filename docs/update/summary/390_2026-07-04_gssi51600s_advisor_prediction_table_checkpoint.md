# GSSI51600S Advisor Prediction Table Checkpoint

## What Changed

- Added `run_field_prediction_advisor_prediction_table.py`.
- Added tests for the advisor-facing strict-vs-assumption-conditioned table.
- Generated a compact prediction table with two rows:
  - `strict_default_blocked`.
  - `assumption_conditioned_candidate`.

## Key Numbers

- Artifact: `outputs/validation_exp_on_field_data/product_leaderboard/231_field_prediction_advisor_prediction_table_gssi51600s_detector_window_candidate/`.
- Strict card decision: `release_promotion_card_blocked`.
- Assumption-conditioned card decision: `range_release_candidate_card_ready`.
- Shared prediction values:
  - x: `0.414366 m`.
  - assumed y: `0.240000 m`.
  - cover depth: `0.120389 m`.
  - length range: `0.183144-0.183513 m`.
  - diameter range: `17.293125-17.296124 mm`.
  - top-margin relative permittivity range: `2.011180-2.046360`.
  - top-margin background conductivity range: `0.002658729-0.007476822 S/m`.
- Strict release failure: `crossline_y_geometry_confirmed`.

## Current Decision

The advisor-facing table is ready for communication: it cleanly separates the strict product status from the assumption-conditioned prediction. This gives a usable field-data estimate without hiding the crossline y-spacing assumption.

## Validation

- `python -m pytest tests/test_field_prediction_advisor_prediction_table.py tests/test_field_prediction_release_policy_variant.py tests/test_field_prediction_range_release_candidate_card.py -q` passed with `9 passed`.
- `python -m py_compile run_field_prediction_advisor_prediction_table.py run_field_prediction_release_policy_variant.py` passed.
- The generated CSV contains the expected strict and assumption-conditioned rows.

## Next Defensible Task

Run the full focused validation suite with the new advisor-table test included, then continue with either crossline-spacing provenance search or another GSSI detector-window stress test.

The local marathon request remains active.
