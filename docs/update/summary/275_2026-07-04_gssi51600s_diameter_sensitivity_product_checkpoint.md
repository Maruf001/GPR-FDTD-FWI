# GSSI 51600S Diameter Sensitivity Product Checkpoint

## What changed

- Added `run_gssi51600s_diameter_sensitivity_scan.py`.
- Ran fixed-diameter Fast-GPR sensitivity on the promoted GSSI detector-rank-2 event.
- Updated `run_gssi51600s_predictor_product_report.py` so the product-facing diameter is only reported when the fixed-diameter scan supports a single value.
- Regenerated the GSSI product report with explicit diameter non-identifiability instead of a misleading 30 mm proxy.

## Key numbers

- Diameter scan artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/014_gssi51600s_diameter_sensitivity_scan`
- Refreshed product report: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/015_gssi51600s_predictor_product_report`
- scanned diameters: `8, 12, 16, 20, 24, 30 mm`
- best fixed-diameter row by loss: `8 mm`
- best loss: `0.646791`
- loss spread across all diameters: `0.0`
- near-best diameter range: `8-30 mm`
- diameter status: `not_identified_flat_loss_across_scanned_diameters`
- product x: `0.109989 m`
- product z/depth: `0.105035 m`
- product epsr: `2.147511`
- product background conductivity: `0.002980 S/m`
- product source shift/polarity: `1.6 ns / -1`

## Current decision

The current GSSI product report should not claim a single diameter. The optimizer's old smooth-cylinder proxy remains available as `optimizer_diameter_proxy_mm = 30.000 mm`, but the product-facing `diameter_proxy_mm` is now null because the 8-30 mm fixed-diameter scan is perfectly flat on this normalized local objective.

## Claim boundary

This is still useful progress toward a shippable predictor: x/z/material prediction is reported, while the diameter field is explicitly withheld when the objective does not identify it. The current GSSI profiles do not estimate y position or length.

## Validation/resource checks

- `python -m py_compile run_gssi51600s_diameter_sensitivity_scan.py tests/test_gssi51600s_diameter_sensitivity_scan.py`
- `python -m pytest tests/test_gssi51600s_diameter_sensitivity_scan.py -q` -> `5 passed`
- GSSI predictor-focused suite with diameter and product-report tests -> `26 passed`
- Diameter scan figure is nonblank, `1413 x 767`, RGB, channel range `0-255`.
- Refreshed product-report figure is nonblank, `1855 x 750`, RGB, channel range `0-255`.
- `git diff --check` on the updated GSSI diameter/product files was clean.
- Script snapshots were frozen under artifacts `014` and `015`.

## Artifact paths

- Diameter summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/014_gssi51600s_diameter_sensitivity_scan/data/gssi51600s_diameter_sensitivity_scan_summary.json`
- Diameter candidates: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/014_gssi51600s_diameter_sensitivity_scan/data/gssi51600s_diameter_sensitivity_scan_candidates.csv`
- Product prediction JSON: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/015_gssi51600s_predictor_product_report/data/gssi51600s_predictor_product_prediction.json`
- Product prediction CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/015_gssi51600s_predictor_product_report/data/gssi51600s_predictor_product_prediction.csv`

## Next defensible task

Diagnose and improve the GSSI geometry objective so radius affects the fit. The immediate candidate is a non-normalized or amplitude-aware residual/shape objective for the shallow event window, because the current normalized local objective lets background epsr/conductivity fit timing while completely suppressing diameter sensitivity.

## Marathon status

The requested 20-hour local marathon is still active. Continue with objective improvement rather than stopping at this checkpoint.
