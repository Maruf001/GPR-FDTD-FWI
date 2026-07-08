# GSSI 51600S Corrected Surface B-Scan Adapter Checkpoint

## What changed

- Added `run_gssi51600s_surface_bscan_forward_contrast.py`.
- Added `run_gssi51600s_surface_bscan_geometry_optimizer.py`.
- Added `run_gssi51600s_surface_bscan_product_report.py`.
- Corrected the GSSI Fast-GPR adapter from the earlier profile-as-source-step/trace-as-receiver layout to a surface B-scan layout:
  - local trace positions map to Fast-GPR source steps,
  - one common-offset receiver is used,
  - grid spacing is refined to `1 cm`, so `8-30 mm` diameters are represented by multiple sub-grid changes rather than disappearing under a `5 cm` grid.
- Compared Adam, AdamW, and Adamax on the corrected surface adapter.

## Key numbers

- Surface forward contrast artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/016_gssi51600s_surface_bscan_forward_contrast`
- Best corrected-surface optimizer artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/020_gssi51600s_surface_bscan_geometry_optimizer`
- Corrected-surface product report: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/022_gssi51600s_surface_bscan_product_report`
- surface forward contrast, `8 mm` to `30 mm`: relative prediction delta `0.010523`
- best optimizer: `AdamW`, weight decay `0.01`
- product x: `0.093258 m`
- product z/depth: `0.084884 m`
- product diameter proxy: `6.727 mm`
- diameter status: `provisional_near_lower_radius_bound`
- product epsr: `2.741512`
- product background conductivity: `0.014007 S/m`
- source shift/polarity: `1.9 ns / -1`
- best corrected-surface loss: `0.884291`
- mean optimizer iteration runtime: `0.583 s`

Optimizer comparison:

| optimizer | weight decay | loss | x m | z m | diameter mm | epsr | bg sigma S/m |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Adam | `0.0` | `0.884554` | `0.092891` | `0.079596` | `6.703` | `2.707641` | `0.013510` |
| AdamW | `0.01` | `0.884291` | `0.093258` | `0.084884` | `6.727` | `2.741512` | `0.014007` |
| Adamax | `0.0` | `0.886517` | `0.096906` | `0.091181` | `6.946` | `2.473517` | `0.009461` |

## Current decision

The older GSSI report remains useful for detector/stack compatibility, but the corrected surface B-scan adapter is the better product-facing path for diameter work. It is the first GSSI Fast-GPR path in this branch where diameter changes produce measurable forward-field contrast.

The current corrected-surface prediction is:

- x: `0.093258 m`
- z/depth: `0.084884 m`
- diameter proxy: `6.727 mm`
- epsr: `2.741512`
- background conductivity: `0.014007 S/m`
- y/length: not estimated from current GSSI profiles

## Claim boundary

The diameter is provisional because the optimizer prefers a small radius close to the configured `6 mm` diameter lower bound and no destructive ground-truth diameter label is available. The next scientific/product question is whether that small-diameter preference survives wider bounds, amplitude/source calibration, and neighboring GSSI events.

## Validation/resource checks

- `python -m py_compile` on the new surface scripts and tests.
- Surface adapter/optimizer/product tests -> `6 passed`, then expanded GSSI suite -> `35 passed`.
- Corrected-surface forward figure is nonblank, `1923 x 767`, RGB, channel range `0-255`.
- AdamW optimizer figure is nonblank, `2314 x 750`, RGB, channel range `0-255`.
- Corrected-surface product figure is nonblank, `1957 x 750`, RGB, channel range `0-255`.
- `git diff --check` on the updated GSSI scripts/tests/checkpoints was clean.
- Script snapshots were frozen under artifacts `016`, `017`, `018`, `019`, `020`, `021`, and `022`.

## Artifact paths

- Forward contrast summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/016_gssi51600s_surface_bscan_forward_contrast/data/gssi51600s_surface_bscan_forward_contrast_summary.json`
- AdamW optimizer summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/020_gssi51600s_surface_bscan_geometry_optimizer/data/gssi51600s_surface_bscan_geometry_optimizer_summary.json`
- Surface product prediction JSON: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/022_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_product_prediction.json`
- Surface product prediction CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/022_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_product_prediction.csv`
- Optimizer comparison CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/022_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_optimizer_comparison.csv`

## Next defensible task

Run a lower-bound sensitivity check for the corrected surface adapter. The goal is to determine whether the current `6.7 mm` diameter is a real local optimum or just the optimizer moving toward the smallest allowed diameter.

## Marathon status

The requested 20-hour local marathon is still active. Continue with lower-bound and source/amplitude calibration checks rather than stopping at this checkpoint.
