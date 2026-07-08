# GSSI 51600S Shallow Predictor Product Report Checkpoint

## What changed

- Added `run_gssi51600s_fastgpr_shallow_geometry_optimizer.py`.
- Ran the first GSSI-specific shallow Fast-GPR geometry/material optimizer using the GSSI stack, detector top x window, and GSSI time/polarity ladder.
- Added `run_gssi51600s_predictor_product_report.py`.
- Generated a GSSI product-facing prediction report with x/z/material estimates and explicit y/length/diameter claim boundaries.

## Key numbers

- GSSI shallow optimizer artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/007_gssi51600s_fastgpr_shallow_geometry_optimizer`
- GSSI product report artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/008_gssi51600s_predictor_product_report`

Optimizer:

- initial loss: `0.664998`
- best loss: `0.664463`
- final loss: `0.665022`
- improvement over initial: `0.000535`
- best iteration: `3 / 12`
- mean iteration runtime: `0.203 s`
- finite outputs/gradients: `True`
- alignment source: polarity `-1`, shift `0 ns`

Product-facing GSSI prediction:

- dataset root: `data/2026-06-09_GSSI_model_51600S`
- x: `0.703263 m`
- y: not estimated; current GSSI files do not provide measured crossline geometry
- profile support: `4 / 4`
- profile window: `0-3`
- z/depth: `0.105035 m`
- detector depth under metadata epsr: `0.105035 m`
- event time: `1.051081 ns`
- diameter proxy: `30.000 mm`
- diameter supported range: `8-30 mm`
- diameter status: proxy upper bound, not unique
- length-y: not estimated from current GSSI profiles
- epsr Fast-GPR: `2.216245`
- epsr metadata: `2.25`
- background conductivity: `0.004354 S/m`
- anomaly conductivity: `0.050000 S/m`
- fit loss: `0.664463`

## Current decision

The GSSI branch now has a complete shallow real-field prediction artifact. It is less complete than the 0701 stack because y/length are not recoverable from the current GSSI profile geometry, but it does provide a real-data x/z/material prediction and fit score on a second dataset.

## Claim boundary

This is a GSSI-specific shallow Fast-GPR smooth-cylinder conductivity proxy. It reports x/z/material fit for a detected shallow event window. It does not identify y position, rebar length, or a unique diameter from the current GSSI profiles.

## What remains blocked

- The product report is based on the top amplitude detector seed only.
- No multi-candidate optimizer scan has confirmed whether a different detector seed fits better.
- Diameter remains pinned at the proxy upper bound and is not uniquely identified.
- GSSI y/length cannot be estimated without measured crossline geometry or a controlled multi-profile stack interpretation.
- Long-profile tails from DZT files `013` and `015` are not yet included in the cropped common stack.

## Validation/resource checks

- `python -m py_compile run_gssi51600s_fastgpr_shallow_geometry_optimizer.py tests/test_gssi51600s_fastgpr_shallow_geometry_optimizer.py`
- GSSI shallow optimizer plus ladder tests -> `3 passed`
- GSSI product report plus optimizer tests -> `3 passed`
- Full GSSI predictor-focused suite -> `17 passed`
- GSSI product report figure is nonblank, `1855 x 750`, RGBA, full channel extrema.
- `git diff --check` on GSSI predictor files was clean.
- Script snapshots were frozen under artifacts `007` and `008`.

## Artifact paths

- Optimizer summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/007_gssi51600s_fastgpr_shallow_geometry_optimizer/data/gssi51600s_fastgpr_shallow_geometry_optimizer_summary.json`
- Product prediction JSON: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/008_gssi51600s_predictor_product_report/data/gssi51600s_predictor_product_prediction.json`
- Product prediction CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/008_gssi51600s_predictor_product_report/data/gssi51600s_predictor_product_prediction.csv`
- Product report figure: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/008_gssi51600s_predictor_product_report/figures/gssi51600s_predictor_product_report.png`

## Next defensible task

Run a multi-candidate GSSI optimizer scan across the top detector seeds, keeping the same shallow Fast-GPR setup. This checks whether the product report should stay at x `0.703 m` or move to another detected event such as x `0.110 m` or x `0.403 m`.

## Marathon status

The requested 20-hour local marathon is still active. Continue with the GSSI multi-candidate optimizer scan rather than stopping at this checkpoint.
