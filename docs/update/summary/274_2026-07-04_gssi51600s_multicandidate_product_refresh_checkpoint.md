# GSSI 51600S Multi-Candidate Product Refresh Checkpoint

## What changed

- Added `run_gssi51600s_multicandidate_shallow_optimizer_scan.py`.
- Compared the top three shallow detector seeds with GSSI-specific observed windows, per-candidate time/polarity ladders, and shallow Fast-GPR optimizer fits.
- Updated `run_gssi51600s_predictor_product_report.py` so the product report can promote the best multi-candidate row instead of blindly using the first detector seed.
- Regenerated the GSSI product report with the multi-candidate winner.

## Key numbers

- Multi-candidate scan artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/011_gssi51600s_multicandidate_shallow_optimizer_scan`
- Refreshed GSSI product report: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/012_gssi51600s_predictor_product_report`
- candidates scanned: `3`
- iterations per candidate: `12`
- best detector rank: `2`
- best x: `0.109989 m`
- best z/depth: `0.105035 m`
- best epsr: `2.147511`
- best loss: `0.646795`
- best ladder shift: `1.6 ns`
- best ladder polarity: `-1`
- best background conductivity: `0.002980 S/m`
- best diameter proxy: `30.000 mm`

Candidate comparison:

| detector rank | x m | ladder shift ns | optimizer loss | epsr | depth m |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `0.703263` | `0.0` | `0.664463` | `2.216245` | `0.105035` |
| 2 | `0.109989` | `1.6` | `0.646795` | `2.147511` | `0.105035` |
| 3 | `0.403293` | `0.2` | `0.662864` | `2.154558` | `0.106999` |

## Current decision

The GSSI product-facing prediction should use detector rank 2, not the original top amplitude detector seed. The current GSSI prediction is:

- x: `0.109989 m`
- z/depth: `0.105035 m`
- epsr: `2.147511`
- background conductivity: `0.002980 S/m`
- diameter proxy: `30.000 mm`
- y/length: not estimated from current GSSI profiles
- fit loss: `0.646795`

## Claim boundary

The multi-candidate scan selects by normalized local Fast-GPR objective loss, not ground truth. It improves the GSSI product candidate, but diameter is still not uniquely identified and y/length remain unresolved.

## Validation/resource checks

- Initial multi-candidate run `009` failed only at plotting due a missing import after completing compute; it is superseded by successful artifacts `010` and `011`.
- `python -m py_compile run_gssi51600s_multicandidate_shallow_optimizer_scan.py tests/test_gssi51600s_multicandidate_shallow_optimizer_scan.py`
- `python -m pytest tests/test_gssi51600s_multicandidate_shallow_optimizer_scan.py -q` -> `2 passed`
- Updated GSSI product report plus multi-candidate tests -> `5 passed`
- Full GSSI predictor-focused suite -> `20 passed`
- Multi-candidate figure is nonblank, `1889 x 767`, RGBA, full channel extrema.
- Refreshed product-report figure is nonblank, `1855 x 750`, RGBA, full channel extrema.
- `git diff --check` on multi-candidate and product-report files was clean.
- Script snapshots were frozen under artifacts `011` and `012`.

## Artifact paths

- Multi-candidate summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/011_gssi51600s_multicandidate_shallow_optimizer_scan/data/gssi51600s_multicandidate_shallow_optimizer_scan_summary.json`
- Multi-candidate rows: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/011_gssi51600s_multicandidate_shallow_optimizer_scan/data/gssi51600s_multicandidate_shallow_optimizer_scan_candidates.csv`
- Refreshed product prediction JSON: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/012_gssi51600s_predictor_product_report/data/gssi51600s_predictor_product_prediction.json`
- Refreshed product prediction CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/012_gssi51600s_predictor_product_report/data/gssi51600s_predictor_product_prediction.csv`

## Next defensible task

Run a GSSI diameter/radius sensitivity check around the promoted rank-2 candidate. The goal is to report whether the 30 mm proxy is meaningful or just a weakly constrained upper-bound artifact.

## Marathon status

The requested 20-hour local marathon is still active. Continue with GSSI diameter/radius sensitivity rather than stopping at this checkpoint.
