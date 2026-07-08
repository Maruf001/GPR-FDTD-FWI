# GSSI 51600S Surface B-Scan Antenna-Offset Sensitivity Checkpoint

## What changed

- Added `--receiver-offset-m` to the corrected surface B-scan Fast-GPR adapter and optimizer.
- Ran offset sensitivity with AdamW, `2 mm` diameter lower bound, and `48` iterations:
  - `8 cm`
  - `2 cm`
  - `1 cm`
  - `5 mm`
  - `1 mm`
- Updated `run_gssi51600s_surface_bscan_product_report.py` so the product report includes receiver-offset sensitivity and selects the best offset-aware run by field objective loss.
- Regenerated the corrected-surface product report.

## Key numbers

- Best offset-aware artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/028_gssi51600s_surface_bscan_geometry_optimizer_offset005_lower_bound_2mm`
- Offset-aware product report: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/030_gssi51600s_surface_bscan_product_report`
- best receiver offset: `0.005 m`
- near-tied receiver offset: `0.001 m`
- best loss: `0.863149`
- product x: `0.080952 m`
- product z/depth: `0.106567 m`
- product diameter proxy: `4.764 mm`
- near-best diameter range: `4.712-4.764 mm`
- product epsr: `2.767118`
- product background conductivity: `0.013688 S/m`
- source shift/polarity: `1.9 ns / -1`
- mean iteration runtime: `0.557 s`

Offset comparison:

| receiver offset | loss | x m | z m | diameter mm | epsr |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `0.080 m` | `0.949907` | `0.098214` | `0.118204` | `4.433` | `2.047658` |
| `0.040 m` | `0.884288` | `0.093608` | `0.081884` | `4.340` | `2.741540` |
| `0.020 m` | `0.881432` | `0.079171` | `0.112958` | `4.681` | `2.556596` |
| `0.010 m` | `0.876392` | `0.080292` | `0.111195` | `4.834` | `2.246324` |
| `0.005 m` | `0.863149` | `0.080952` | `0.106567` | `4.764` | `2.767118` |
| `0.001 m` | `0.863152` | `0.086337` | `0.114997` | `4.712` | `2.764233` |

## Current decision

The corrected surface B-scan product report should use the near-monostatic offset family, not the earlier `4 cm` default. The `5 mm` and `1 mm` offset cases are effectively tied, and both are much better than `4 cm` and `8 cm`.

Current offset-aware corrected-surface prediction:

- x: `0.080952 m`
- z/depth: `0.106567 m`
- diameter proxy: `4.764 mm`
- near-best diameter range: `4.712-4.764 mm`
- epsr: `2.767118`
- background conductivity: `0.013688 S/m`
- y/length: not estimated from current GSSI profiles

## Claim boundary

The result is stronger than the previous corrected-surface report because receiver offset is now tested. It remains provisional because the objective prefers a near-monostatic offset that is selected from the field fit, not confirmed from antenna metadata, and diameter remains in a small-diameter regime.

## Validation/resource checks

- Surface adapter/optimizer/product tests -> `11 passed`
- Expanded GSSI predictor suite -> `37 passed`
- Offset optimizer figures are nonblank, `2314 x 750`, RGB, channel range `0-255`.
- Offset-aware product figure is nonblank, `1957 x 750`, RGB, channel range `0-255`.
- `git diff --check` on the updated surface adapter/optimizer/product files was clean.
- Script snapshots were frozen under artifacts `025`, `026`, `027`, `028`, `029`, and `030`.

## Artifact paths

- Best offset optimizer summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/028_gssi51600s_surface_bscan_geometry_optimizer_offset005_lower_bound_2mm/data/gssi51600s_surface_bscan_geometry_optimizer_summary.json`
- Offset-aware product JSON: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/030_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_product_prediction.json`
- Offset-aware product CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/030_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_product_prediction.csv`
- Offset comparison CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/030_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_optimizer_comparison.csv`

## Next defensible task

Test the corrected surface B-scan adapter on the neighboring GSSI detector candidates or another DZT profile window. The key product question is whether the near-monostatic small-diameter prediction is stable across adjacent field events, or only fits one local window.

## Marathon status

The requested 20-hour local marathon is still active. Continue with adjacent-candidate/profile stability rather than stopping at this checkpoint.
