# GSSI 51600S Optimizer-Family And Dataset-Scope Checkpoint

## What Changed

- Confirmed that the current product-facing rebar prediction path stays anchored on the trusted GSSI 51600S field scans.
- Rechecked the separate 2025 public GPR archive scope from local metadata: it is a mixed archive with tunnel, pipeline, and rebar branches, so it is now treated as auxiliary validation unless a run explicitly targets its rebar branch.
- Added an optimizer-family comparison card for the current GSSI 3D field objective across AdamW, Adamax, and Rectified Adam.
- Regenerated the latest GSSI prediction bundle so the stable latest pointer now includes the recommended optimizer, the GSSI-only dataset boundary, the runtime benchmark, and the packaged pretty prediction with optimizer context.
- Updated the live current-prediction query so the GSSI output reports `recommended_optimizer: adamw` and the dataset-scope note directly.
- Appended the Sunday daily update with the optimizer-family decision and data-provenance boundary.

## Key Numbers

- Recommended optimizer: AdamW.
- AdamW mean objective loss across the two GSSI profile subsets: 0.978138.
- AdamW mean field L1 loss: 0.958154.
- AdamW mean finite length estimate: 0.183363 m.
- AdamW mean diameter estimate: 17.305637 mm.
- Adamax mean objective loss: 0.985717, with mean length 0.214850 m.
- Rectified Adam mean objective loss: 0.999092, with mean length 0.200049 m.
- Current two-subset optimizer-loop runtime remains 41.675845 s.

## Current Decision

AdamW remains the current product optimizer for the trusted GSSI 51600S predictor. Adamax and Rectified Adam remain diagnostic alternatives because they did not improve the same GSSI field objective under the same profile subsets, windows, and iteration budget.

## What Remains Blocked

- Crossline profile coordinates are still not metadata-confirmed for the GSSI scans.
- The finite-length estimate remains geometry-conditioned until measured or explicitly optimized crossline coordinates are available.
- The 2025 archive should not be mixed into GSSI rebar claims without explicit branch-level target classification.

## Next Defensible Task

Use the current measured-geometry planner path to turn measured or explicitly optimized crossline profile coordinates into explicit GSSI 3D optimizer offsets, then rerun the predictor so y position and finite length are conditioned on confirmed geometry.

## Validation And Resource Checks

- `python -m pytest tests/test_field_prediction_current_query.py tests/test_gssi51600s_optimizer_family_card.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_runtime_benchmark_card.py tests/test_gssi51600s_nonuniform_geometry_run_planner.py -q`
- Result: 22 passed.
- `python -m py_compile run_field_prediction_current_query.py run_gssi51600s_optimizer_family_card.py run_gssi51600s_current_prediction_bundle.py`
- Result: passed.
- `git diff --check` on touched scripts, tests, and the daily update.
- Result: passed.

## Artifact Paths

- Optimizer-family card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/135_gssi51600s_optimizer_family_card_current`
- Latest corrected bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/138_gssi51600s_current_prediction_bundle_with_packaged_optimizer_scope`
- Stable latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- Daily update: `docs/update/daily_update/2026-06-29_to_2026-07-05_daily_update.md`

## Marathon Status

The marathon request is still active. Continue with the next product-improving GSSI field-data branch rather than stopping at this checkpoint.
