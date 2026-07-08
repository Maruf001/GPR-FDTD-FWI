# 2026-07-04 GSSI 51600S Product Bundle Source-Receiver Context Checkpoint

## What changed

- Added source/receiver geometry context to the current GSSI 51600S prediction bundle generator.
- Added the same context to the live field-prediction query command so the product-facing output reports antenna-geometry caveats directly.
- Regenerated the GSSI current prediction bundle with updated source snapshots.

## Key numbers

- Current command-line prediction remains:
  - x: `0.413941 m`
  - assumed y: `0.16 m`
  - cover depth z: `0.120349 m`
  - length range: `0.183166-0.216163 m`
  - diameter range: `17.2954-17.8126 mm`
  - relative permittivity: `1.97913`
  - conductivity: `0.00266249 S/m`
- Source/receiver diagnostic now shown in the live query:
  - decision: `collocated_source_receiver_fits_better_current_objective_bistatic_diagnostic_only`
  - 60 mm bistatic field-L1 delta versus collocated, profiles 0-2: `+0.0169564486`
  - 60 mm bistatic field-L1 delta versus collocated, profiles 1-3: `+0.0173347592`

## Current decision

The product-facing GSSI output now reports both geometry caveats:

- Crossline profile spacing remains the main blocker for collapsing the finite-length range to one value.
- The 60 mm source-receiver separation test is diagnostic-only because it worsens the current objective compared with the collocated assumption.

## What remains blocked

- Measured crossline profile coordinates are still required for a single release-style finite-length claim.
- Antenna phase-center/source-receiver geometry remains configurable rather than promoted as a fixed 60 mm assumption.

## Next defensible task

Move from reporting the geometry uncertainty to estimating it: add a bounded profile-position/spacing estimator that can fit crossline coordinates jointly with the rebar geometry, while keeping GSSI 51600S as the trusted rebar product dataset.

## Artifact paths

- Updated bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/111_gssi51600s_current_prediction_bundle_with_cli_source_receiver_context/`
- Source/receiver diagnostic input: `outputs/validation_exp_on_field_data/3d_geometry_inventory/456_gssi51600s_finite_length_3d_source_receiver_geometry_check_y022_profiles0_2_1_3_adamw/`
- Updated scripts:
  - `run_field_prediction_current_query.py`
  - `run_gssi51600s_current_prediction_bundle.py`

## Validation/resource checks

- `python -m py_compile run_field_prediction_current_query.py run_gssi51600s_current_prediction_bundle.py`
- `python -m pytest tests/test_field_prediction_current_query.py tests/test_gssi51600s_current_prediction_bundle.py -q`
- Focused broader validation is pending after this checkpoint.
- The local marathon request remains active.
