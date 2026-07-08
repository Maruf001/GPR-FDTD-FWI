# GSSI 51600S Crossline Spacing Release Gate Checkpoint

## What Changed

- Added a release-gate card for the trusted GSSI 51600S crossline profile spacing estimate.
- The card reads the current joint spacing scan, fits a bounded continuous spacing diagnostic, detects length-branch transitions, and decides whether the optimizer-estimated spacing is strong enough to collapse y position and finite length.
- Regenerated the latest GSSI prediction bundle so the stable latest pointer now includes the crossline-spacing release-gate fields and figure.
- Updated the live current-prediction query so the GSSI output reports the release-gate decision directly.
- Updated the Sunday daily note with the release-gate result.

## Key Numbers

- Release-gate decision: `crossline_spacing_objective_flat_keep_geometry_conditioned`.
- Joint spacing MAP: `0.22 m`.
- Joint weighted spacing: `0.236095 m`.
- Continuous quadratic spacing minimum: `0.244543 m`.
- Near-minimum spacing range at the current tolerance: `0.20-0.28 m`.
- Near-minimum spacing width: `0.08 m`.
- Branch transition interval: `0.20-0.22 m`.
- Mean length span across spacing rows: `0.016915 m`.

## Current Decision

The optimizer-estimated spacing is useful for conditioning the current GSSI prediction, but it is not decisive enough to promote a single y position or finite length. The product output should keep reporting the geometry-conditioned length range until measured crossline coordinates or a stronger profile-position optimizer is available.

## What Remains Blocked

- Crossline coordinates are not present in the local GSSI sidecar metadata.
- The current field objective is nearly flat across several plausible crossline spacings.
- Length branch state changes near the current MAP spacing, so a single finite length would overstate the geometry evidence.

## Next Defensible Task

Move from scalar uniform spacing to explicit profile-position estimation: either supply measured profile y coordinates through the planner or test a bounded profile-position optimizer that can vary the individual profile offsets while preserving physically plausible ordering.

## Validation And Resource Checks

- `python -m pytest tests/test_field_prediction_current_query.py tests/test_gssi51600s_optimizer_family_card.py tests/test_gssi51600s_crossline_spacing_release_gate.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_runtime_benchmark_card.py tests/test_gssi51600s_nonuniform_geometry_run_planner.py -q`
- Result: 26 passed.
- `python -m py_compile run_field_prediction_current_query.py run_gssi51600s_optimizer_family_card.py run_gssi51600s_crossline_spacing_release_gate.py run_gssi51600s_current_prediction_bundle.py`
- Result: passed.
- `git diff --check` on touched scripts, tests, checkpoints, and daily update.
- Result: passed.

## Artifact Paths

- Crossline release gate: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/139_gssi51600s_crossline_spacing_release_gate_current`
- Latest bundle with release gate: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/140_gssi51600s_current_prediction_bundle_with_crossline_release_gate`
- Stable latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`

## Marathon Status

The marathon request is still active. Continue with the next product-improving GSSI field-data branch rather than stopping at this checkpoint.
