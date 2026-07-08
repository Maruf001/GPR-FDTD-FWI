# 2026-07-04 GSSI 51600S Measured Geometry Intake Checkpoint

## What changed

- Added `run_gssi51600s_measured_geometry_intake.py`.
- The command validates a measured profile-geometry CSV with `profile_index,y_m` columns.
- For uniform spacing, it feeds the measured spacing into the geometry-conditioned predictor.
- For nonuniform spacing, it refuses to collapse to one spacing and reports that an explicit profile-position optimizer is needed.
- Generated a measured-geometry template CSV.
- Added the measured-geometry intake command to the current product bundle source snapshots.

## Key numbers

- Template artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/119_gssi51600s_measured_geometry_intake_template/data/gssi51600s_measured_profile_geometry_template.csv`
- Current product bundle with geometry intake: `120_gssi51600s_current_prediction_bundle_with_geometry_intake`
- Template profile positions:
  - profile 0: `0.00 m`
  - profile 1: `0.22 m`
  - profile 2: `0.44 m`
  - profile 3: `0.66 m`
- Template intake status: `uniform_spacing_ready_for_conditioned_predictor`
- Template mean measured spacing: `0.22 m`
- Conditioned prediction from template:
  - selected spacing: `0.22 m`
  - branch state: `short_only`
  - length: `0.1833631247 m`
  - diameter: `17.30563678 mm`
  - relative permittivity: `2.042056620`
  - conductivity: `0.0026600763 S/m`

## Current decision

The product path now has a clean intake route for measured crossline geometry. If acquisition notes provide profile y positions, the predictor can validate the spacing and report the corresponding spacing-conditioned rebar estimate. If geometry is nonuniform, it will not silently average into a release claim.

## What remains blocked

- We still need the actual measured crossline profile positions for `data/2026-06-09_GSSI_model_51600S`.
- Nonuniform geometry still requires a profile-position optimizer rather than a single spacing-conditioned row.

## Next defensible task

Either locate the measured GSSI crossline profile positions and run the intake command, or implement the explicit nonuniform profile-position optimizer path that the intake command now points to.

## Validation/resource checks

- `python -m py_compile run_gssi51600s_current_prediction_bundle.py run_gssi51600s_measured_geometry_intake.py run_gssi51600s_geometry_conditioned_predictor.py`
- `python -m pytest tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_measured_geometry_intake.py tests/test_gssi51600s_geometry_conditioned_predictor.py -q`
- Template generation and intake smoke completed.
- Broader focused validation is pending after this checkpoint.
- The local marathon request remains active.
