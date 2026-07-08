# GSSI 51600S Rank-3 Window Sensitivity Checkpoint

## What changed

- Ran rank-3 corrected surface B-scan sensitivity around the current product candidate:
  - `pre_event_ns = 0.3`
  - `pre_event_ns = 0.7`
  - overlap `81`
  - overlap `105`
- Updated `run_gssi51600s_surface_bscan_product_report.py` to include these window-sensitivity artifacts.
- Regenerated the product report with window-sensitive geometry status.

## Key numbers

- Baseline rank-3 artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/039_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_lower_bound_2mm_candidate_window`
- Window-aware product report: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/047_gssi51600s_surface_bscan_product_report`

Rank-3 window sensitivity:

| run | window start ns | overlap | loss | x m | z m | diameter mm | epsr |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | `0.569745` | `101` | `0.848678` | `0.414366` | `0.126887` | `17.993` | `2.053892` |
| pre-event `0.3 ns` | `0.766208` | `101` | `0.861197` | `0.400904` | `0.110109` | `13.001` | `2.051549` |
| pre-event `0.7 ns` | `0.373281` | `101` | `0.849398` | `0.390921` | `0.079356` | `8.109` | `2.038053` |
| overlap `81` | `0.569745` | `81` | `0.851761` | `0.418476` | `0.127090` | `19.303` | `2.068637` |
| overlap `105` | `0.569745` | `105` | `0.849739` | `0.414374` | `0.127925` | `18.738` | `2.047994` |

## Current decision

Rank 3 remains the best product candidate by loss, but its geometry is window-sensitive. The product report should not present the `17.993 mm` diameter as final; it should report the top fit and the near-best diameter range.

Current product report:

- detector rank: `3`
- x: `0.414366 m`
- z/depth: `0.126887 m`
- diameter proxy: `17.993 mm`
- near-best diameter range: `8.109-17.993 mm`
- epsr: `2.053892`
- background conductivity: `0.006278 S/m`
- status: `provisional_window_sensitive_geometry`

## Claim boundary

Overlap changes preserve the larger-diameter solution, but pre-event window changes can produce a near-tied smaller-diameter solution. This points to remaining time-window/source-wavelet sensitivity rather than a settled rebar diameter.

## Validation/resource checks

- Product/geometry/forward tests -> `12 passed`
- Expanded GSSI predictor suite -> `38 passed`
- Window sensitivity figures are nonblank, `2314 x 750`, RGB, channel range `0-255`.
- Product figure is nonblank, `1957 x 750`, RGB, channel range `0-255`.
- `git diff --check` on updated surface product/optimizer files was clean.
- Script snapshots were frozen under artifacts `042`, `043`, `044`, `046`, and `047`.

## Artifact paths

- Window-aware product JSON: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/047_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_product_prediction.json`
- Window-aware product CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/047_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_product_prediction.csv`
- Window-aware comparison CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/047_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_optimizer_comparison.csv`
- Baseline rank-3 summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/039_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_lower_bound_2mm_candidate_window/data/gssi51600s_surface_bscan_geometry_optimizer_summary.json`

## Next defensible task

Move from fixed time shift to continuous/source-time optimization for the corrected surface adapter. The strongest remaining instability is time-window/source alignment, so the next product improvement should optimize source time shift instead of locking shift at `95` samples.

## Marathon status

The requested 20-hour local marathon is still active. Continue with corrected-surface time-shift optimization rather than stopping at this checkpoint.
